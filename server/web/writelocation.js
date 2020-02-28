function writeLocation() {
    let locelement = document.getElementById("location")
    locelement.innerText = locelement.innerText.replace("0.0.0.0/", window.location.href)
}