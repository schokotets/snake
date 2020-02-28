function handleMessage(data) {
    let canvas = document.getElementById('canvas');
    if(!canvas) return
    let context2d = canvas.getContext('2d');
    context2d.clearRect(0,0,canvas.width, canvas.height);

    let colors = ["red", "green", "blue", "pink", "cyan"]

    let lines = data.split("\n");
    let wh = lines[0].split("x");
    let width = wh[0];
    let height = wh[1];
    let ch = Math.floor(canvas.height / height);
    let cw = Math.floor(canvas.width / width);

    for (let y = 1; y < lines.length; y++) {
        let line = lines[y].split(';')
        for (let x = 0; x < line.length; x++) {
            context2d.beginPath();
            context2d.rect(x*cw, y*ch, cw, ch)
            let id = line[x]
            if (id == '0') {
                context2d.strokeStyle = "lightgray"
                context2d.stroke();
            } else {
                context2d.fillStyle = colors[parseInt(id, 10)%colors.length]
                context2d.fill();
            }
            context2d.closePath();
        }
    }


    context2d.moveTo(128, 128);
    context2d.closePath();
}
