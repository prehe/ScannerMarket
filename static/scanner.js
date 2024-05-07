const scanner = new Html5QrcodeScanner('reader', {
    qrbox: {
        width: 250,
        height: 250,
    },
    fps: 30,
});

scanner.render(success, error);

function success(result) {
    document.getElementById('result').innerHTML = `
    <h2>Erfolgreich gescannt</h2>
    <p><a href="${result}">${result}</a></p>
    <br><br>
    <a href="">nochmal scannen</a>
    `;
    scanner.clear();
    document.getElementById('reader').remove();
}

function error(err) {
    // console.error(err);
}
