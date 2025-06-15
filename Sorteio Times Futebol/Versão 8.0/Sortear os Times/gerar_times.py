# gerar_times.py
"""
Sorteia 5 times equilibrados (6 jogadores cada) garantindo:

1. **Composição fixa** 2‑2‑2 (zagueiro, meia, atacante) — primária preferida, secundária de craques como fallback.
2. **Balanceamento de estrelas**, **rotatividade** de duplas e 1 Top 5 + 1 Bottom 5 por time.
3. **Times são exibidos do menor para o maior total de estrelas** (Time 1 é o “mais fraco”, Time 5 o mais forte), evitando que o time com menos habilidade ainda jogue por último.
4. Histórico salvo em `./historico/YYYY-MM-DD.json` após confirmação.

Rodar:
```bash
python gerar_times.py
```
"""
from __future__ import annotations

import datetime as dt
import itertools as it
import json
import os
import random as rnd
import statistics as stats
from typing import Dict, List, Tuple

# =====================
# Configurações gerais
# =====================
NUM_TEAMS = 5
TEAM_SIZE = 6
TARGET = {"zagueiro": 2, "meia": 2, "atacante": 2}

W_BALANCE = 5      # peso equilíbrio de estrelas
W_ROTATION = 1     # peso duplas repetidas
W_COMPOSITION = 30 # peso 2-2-2
W_EXTREME = 100    # peso top/bottom rule
ITER = 15000
HISTORY_DIR = "historico"

# ==========
# Dados base
# ==========
try:
    from lista_jogadores import lista_jogadores  # type: ignore
except ImportError:
    raise SystemExit("Erro: criar lista_jogadores.py com variável lista_jogadores.")

if len(lista_jogadores) != NUM_TEAMS * TEAM_SIZE:
    raise SystemExit(f"Esperado {NUM_TEAMS*TEAM_SIZE} jogadores, recebi {len(lista_jogadores)}.")

_sorted = sorted(lista_jogadores, key=lambda p: p["habilidade"])
BOTTOM = {p["nome"] for p in _sorted[:NUM_TEAMS]}
TOP = {p["nome"] for p in _sorted[-NUM_TEAMS:]}

# =================
# Histórico helpers
# =================

def _ensure_dir() -> None:
    os.makedirs(HISTORY_DIR, exist_ok=True)


def _load_history() -> List[List[List[str]]]:
    _ensure_dir()
    hist: List[List[List[str]]] = []
    for fn in sorted(os.listdir(HISTORY_DIR)):
        if fn.endswith(".json"):
            with open(os.path.join(HISTORY_DIR, fn), "r", encoding="utf-8") as fp:
                hist.append(json.load(fp))
    return hist


def _pair_counts(hist: List[List[List[str]]]) -> Dict[Tuple[str, str], int]:
    pairs: Dict[Tuple[str, str], int] = {}
    for rodada in hist:
        for team in rodada:
            for a, b in it.combinations(sorted(team), 2):
                pairs[(a, b)] = pairs.get((a, b), 0) + 1
    return pairs

# =================================
# Atribuição interna 2‑2‑2 por time
# =================================

def _pos_options(p: dict) -> List[str]:
    opts = [p["posicao_primaria"]]
    if p["posicao_secundaria"] != "nenhum":
        opts.append(p["posicao_secundaria"])
    return opts[:2]


def _assignment_penalty(choice: Tuple[str, ...], team: List[dict]) -> float:
    comp: Dict[str, List[int]] = {k: [] for k in TARGET}
    flex_pen = 0.0
    for slot, (pos_taken, player) in enumerate(zip(choice, team)):
        rating = player["habilidade"]
        primary = player["posicao_primaria"]
        if pos_taken not in TARGET:
            pos_taken = "atacante"
        comp[pos_taken].append(slot)
        if pos_taken != primary:
            flex_pen += (5 - rating)
    comp_pen = sum(abs(len(comp[k]) - TARGET[k]) for k in TARGET)
    return comp_pen * 100 + flex_pen


def _best_assignment(team: List[dict]) -> Tuple[int, Dict[str, List[dict]]]:
    options = [_pos_options(p) or ["atacante"] for p in team]
    best_score = float("inf")
    best_map: Dict[str, List[dict]] | None = None
    for choice in it.product(*options):
        score = _assignment_penalty(choice, team)
        if score < best_score:
            best_score = score
            m: Dict[str, List[dict]] = {k: [] for k in TARGET}
            for pos, player in zip(choice, team):
                if pos not in TARGET:
                    pos = "atacante"
                m[pos].append(player)
            for pos in m:
                m[pos].sort(key=lambda x: x["habilidade"], reverse=True)
            best_map = m
            if best_score == 0:
                break
    assert best_map is not None
    comp_pen = int(best_score // 100)
    return comp_pen, best_map

# =========================
# Avaliação de uma solução
# =========================

def _eval_solution(teams: List[List[dict]], pairs: Dict[Tuple[str, str], int]) -> float:
    totals = [sum(p["habilidade"] for p in t) for t in teams]
    balance_pen = stats.pvariance(totals)

    rot_pen = sum(
        pairs.get((a, b), 0)
        for team in teams
        for a, b in it.combinations(sorted(p["nome"] for p in team), 2)
    )

    comp_pen = sum(_best_assignment(t)[0] for t in teams)

    extreme_pen = sum(
        abs(1 - len({p["nome"] for p in t} & TOP)) + abs(1 - len({p["nome"] for p in t} & BOTTOM))
        for t in teams
    )

    return (
        W_BALANCE * balance_pen
        + W_ROTATION * rot_pen
        + W_COMPOSITION * comp_pen
        + W_EXTREME * extreme_pen
    )

# ======================
# Sorteio / otimização
# ======================

def _random_partition(players: List[dict]) -> List[List[dict]]:
    temp = players[:]
    rnd.shuffle(temp)
    return [temp[i * TEAM_SIZE:(i + 1) * TEAM_SIZE] for i in range(NUM_TEAMS)]


def gerar_times() -> Tuple[List[List[dict]], float]:
    hist = _load_history()
    pairs = _pair_counts(hist)
    best: List[List[dict]] | None = None
    best_cost = float("inf")
    for _ in range(ITER):
        cand = _random_partition(lista_jogadores)
        cost = _eval_solution(cand, pairs)
        if cost < best_cost:
            best, best_cost = cand, cost
            if best_cost == 0:
                break
    assert best is not None
    return best, best_cost

# ==============
# Rank por total
# ==============

def _rank_by_total(teams: List[List[dict]]) -> List[List[dict]]:
    """Ordena times pelo total de estrelas (ASC)."""
    return sorted(teams, key=lambda t: sum(int(p["habilidade"] * 2) for p in t))

# ======================
# Impressão amigável
# ======================

POSITION_LABELS = [("ZAGUEIROS", "zagueiro"), ("MEIAS", "meia"), ("ATACANTES", "atacante")]


def _print_team(idx: int, team: List[dict]) -> None:
    total = sum(p["habilidade"] for p in team)
    _ , mapping = _best_assignment(team)  # comp_pen não exibido
    print(f"TIME {idx} | TOTAL: {total:.1f}")
    print("-" * 30)
    for label, key in POSITION_LABELS:
        print(label + ":")
        for i, p in enumerate(mapping[key], 1):
            print(f" {i}- {p['nome']} ({p['habilidade']})")
        if not mapping[key]:
            print(" (nenhum)")
        print()


def _print_times(teams: List[List[dict]]) -> None:
    ordered = _rank_by_total(teams)
    for i, t in enumerate(ordered, 1):
        _print_team(i, t)
        print()

# ===============
# Histórico I/O
# ===============

def _save_history(teams: List[List[dict]]) -> None:
    _ensure_dir()
    fname = f"{dt.date.today():%Y-%m-%d}.json"
    with open(os.path.join(HISTORY_DIR, fname), "w", encoding="utf-8") as fp:
        json.dump([[p["nome"] for p in t] for t in teams], fp, ensure_ascii=False, indent=2)
    print(f"Histórico salvo em {HISTORY_DIR}/{fname}\n")

# ============
# Main loop
# ============

def main() -> None:
    while True:
        teams, cost = gerar_times()
        _print_times(teams)  # já exibe rankeados
        print(f"Custo total (↓ melhor): {cost:.2f}\n")
        if input("Confirmar este sorteio? [y/n]: ").strip().lower().startswith("y"):
            _save_history(teams)
            break
        print("Gerando novo sorteio...\n")


if __name__ == "__main__":
    main()
