function handleMessage(data) {
    canvas = document.getElementById('canvas');
    if(!canvas) return
    context2d = canvas.getContext('2d');
    context2d.clearRect(0,0,canvas.width, canvas.height);
    context2d.beginPath();
    context2d.moveTo(128, 128);
    context2d.lineTo(128+parseInt(data[1], 10), 128+parseInt(data[2], 10));
    context2d.closePath();
    context2d.stroke();
}
