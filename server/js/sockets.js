var connection = new WebSocket('ws://localhost:8090/')

id = -1

// When the connection is open, send some data to the server
connection.onopen = function () {
  //connection.send('Ping'); // Send the message 'Ping' to the server
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
connection.onmessage = function (e) {
  console.log('Server: ' + e.data);
  if(id == -1) {
    id = parseInt(e.data, 10)
    console.log('Setting ID to ' + e.data)
  } else {
    handleMessage(e.data);
  }
};

function sendData(data) {
  connection.send(data);
}