function handleMessage(data) {
    let canvas = document.getElementById('canvas');
    if(!canvas) return
    let context2d = canvas.getContext('2d');
    context2d.clearRect(0,0,canvas.width, canvas.height);

    let colors = ["#009e73", "#56b4e9", "#0072b2", "#00ced1", "#ffb000"]

    let lines = data.split("\n");
    let wh = lines[0].split("x");
    let width = wh[0];
    let height = wh[1];
    let ch = Math.floor(canvas.height / height);
    let cw = Math.floor(canvas.width / width);

    for (let y = 0; y < lines.length-1; y++) {
        let line = lines[y+1].split(';')
        for (let x = 0; x < line.length; x++) {
            context2d.beginPath();
            context2d.rect(x*cw, y*ch, cw, ch)
            let id = line[x]
            if (id == '0') {
                context2d.strokeStyle = "darkgray"
                context2d.stroke()
            } else if (id == '-1') {
                context2d.fillStyle = "#dc267f"
                context2d.fill();
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
