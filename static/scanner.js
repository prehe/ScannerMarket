const scanner = new Html5QrcodeScanner('reader', {
    qrbox: {
        width: 250,
        height: 250,
    },
    fps: 30,
});

scanner.render(success, error);

function success(result) {
    document.getElementById('result').style.display = "block";
    scanner.clear();
    document.getElementById('reader').style.display = 'none';
}

function error(err) {
    // console.error(err);
}
