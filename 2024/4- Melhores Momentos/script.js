
var channelId = "UCrwbYI0FtW9IsX2kDUt9vHg";
var channelPlaylistsUrl =
  "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=" +
  channelId +
  "&maxResults=1&key=AIzaSyBxgXlGbCXmjWDRKt0NSBU8kzSczRsgPUI";

var player;
var currentVideoTitle = "";

function onYouTubeIframeAPIReady() {
  player = new YT.Player("video", {
    height: "480",
    width: "854",
    events: {
      onReady: onPlayerReady,
    },
  });
}


function onPlayerReady(event) {
  fetch(channelPlaylistsUrl)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var playlistId = data.items[0].id;
      var playlistTitle = data.items[0].snippet.title;
      var playlistUrl =
        "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=" +
        playlistId +
        "&key=AIzaSyBxgXlGbCXmjWDRKt0NSBU8kzSczRsgPUI";

      fetch(playlistUrl)
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          var videoId = data.items[0].snippet.resourceId.videoId;
          var videoTitle = data.items[0].snippet.title;
          currentVideoTitle = videoTitle;
          updateVideo(videoId, videoTitle);

          var playlistElement = document.getElementById("playlist");
          var playlistItems = data.items;

          var playlistList = "<ul>";

          // Adicionando o primeiro vídeo manualmente à lista
          playlistList +=
            '<li><a href="#" onclick="handleClick(\'' +
            videoId +
            "', '" +
            videoTitle +
            "')\">" +
            videoTitle +
            "</a></li>";

          // Adicionando os demais vídeos da playlist
          playlistItems.slice(1).forEach(function (item) {
            var itemId = item.snippet.resourceId.videoId;
            var itemTitle = item.snippet.title;
            playlistList +=
              '<li><a href="#" onclick="handleClick(\'' +
              itemId +
              "', '" +
              itemTitle +
              "')\">" +
              itemTitle +
              "</a></li>";
          });
          playlistList += "</ul>";

          playlistElement.innerHTML =
            "<h3>" + playlistTitle + "</h3>" + playlistList;
        })
        .catch(function (error) {
          console.log("Ocorreu um erro: " + error);
        });
    })
    .catch(function (error) {
      console.log("Ocorreu um erro: " + error);
    });
}

function updateVideo(videoId, videoTitle) {
  player.loadVideoById(videoId);
  var videoElement = document.getElementById("video");
  videoElement.innerHTML = "<h2>" + videoTitle + "</h2>";
}

function handleClick(videoId, videoTitle) {
  updateVideo(videoId, videoTitle);
  currentVideoTitle = videoTitle;
}

function addStatisticToTable() {
  var currentTime = player.getCurrentTime();
  var formattedTime = formatTime(currentTime);
  var videoId = getVideoId();

  var table = $("#statsTable").DataTable();
  if (!table || !$.fn.DataTable.isDataTable('#statsTable')) {
      table = $("#statsTable").DataTable({
          "pageLength": 50
      });
  }

  table.row.add([currentVideoTitle, formattedTime]).draw(false);
}








function formatTime(time) {
  var minutes = Math.floor(time / 60);
  var seconds = Math.floor(time % 60);
  return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
}

document.getElementById("melhores_momentosButton").addEventListener("click", function () {
  addStatisticToTable("Melhores Momentos");
});

function getVideoId() {
    // Verifica se o player está definido
    if (typeof player !== "undefined") {
      // Obtém o ID do vídeo atual do player
      var videoId = player.getVideoData().video_id;
      return videoId;
    } else {
      console.error("O player do YouTube não está definido.");
      return null;
    }
  }
  

  function exportarParaExcel() {
    var workbook = XLSX.utils.book_new();
    var statsWorksheetData = [["Vídeo", "Tempo"]];

    var table = $("#statsTable").DataTable();
    var data = table.data().toArray();

    for (var i = 0; i < data.length; i++) {
        var video = data[i][0];
        var tempo = data[i][1];
        statsWorksheetData.push([video, tempo]);
    }

    var statsWorksheet = XLSX.utils.aoa_to_sheet(statsWorksheetData);
    XLSX.utils.book_append_sheet(workbook, statsWorksheet, "Estatísticas");

    var dateTime = new Date().toLocaleString().replace(/:/g, "-");
    var filename = "melhores-momentos_" + dateTime + ".xlsx";

    var wbout = XLSX.write(workbook, { bookType: "xlsx", type: "binary" });
    saveWorkbook(wbout, filename);
}

function saveWorkbook(wbout, filename) {
  function s2ab(s) {
    var buf = new ArrayBuffer(s.length);
    var view = new Uint8Array(buf);
    for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xff;
    return buf;
  }

  var blob = new Blob([s2ab(wbout)], {
    type: "application/octet-stream",
  });
  var url = URL.createObjectURL(blob);

  var a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();

  setTimeout(function () {
    URL.revokeObjectURL(url);
  }, 0);
}

function downloadVideo(videoId, currentTime) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/download", true); // Rota para o servidor
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = "blob";

    xhr.onload = function () {
        if (xhr.status === 200) {
            var blob = new Blob([xhr.response], { type: "video/mp4" });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = url;
            a.download = "video.mp4";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }
    };

    xhr.send(JSON.stringify({ videoId: videoId, currentTime: currentTime }));
}