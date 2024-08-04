from pytube import YouTube

def download_video(url):
    try:
        # Instancia um objeto YouTube com a URL do vídeo
        video = YouTube(url)

        # Filtra os streams disponíveis para encontrar um em FullHD (1080p)
        stream = video.streams.filter(res="1080p").first()

        if not stream:
            print("Não foi possível encontrar um vídeo em FullHD.")
            return

        # Baixa o vídeo
        print(f"Baixando: {video.title}...")
        stream.download()
        print("Download concluído!")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # URL do vídeo do YouTube
    url = input("Digite a URL do vídeo do YouTube: ")
    download_video(url)
