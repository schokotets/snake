var connection = new WebSocket('ws://localhost:8090/players')

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
  data = e.data.split(" ")
  canvas = document.getElementById('canvas')
  context2d = canvas.getContext('2d')
  context2d.clearRect(0,0,canvas.width, canvas.height)
  context2d.beginPath()
  context2d.moveTo(128, 128)
  context2d.lineTo(128+parseInt(data[1], 10), 128+parseInt(data[2], 10))
  context2d.closePath()
  context2d.stroke()
};
