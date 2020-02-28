let url = window.location.href
url = url.replace("http", "ws").split("8080")[0]+"8090/"

var connection = new WebSocket(url)

id = -1

// When the connection is open, send some data to the server
connection.onopen = function () {
  if(join) {
    connection.send("join");
  }
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
connection.onmessage = function (e) {
  console.debug('Server: ' + e.data);
  if(id == -1) {
    id = parseInt(e.data, 10)
    console.log('Setting ID to ' + e.data)
  } else {
    if(handleMessage) {
      handleMessage(e.data);
    }
  }
};

function sendData(data) {
  connection.send(data);
}