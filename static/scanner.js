const scanner = new Html5QrcodeScanner('reader', {
    qrbox: {
        width: 250,
        height: 250,
    },
    fps: 30,
});

scanner.render(success, error);

function success(result) {
    console.error(result);
    scanner.clear();
    document.getElementById('result').style.display = "block";
    document.getElementById('reader').style.display = 'none';
    result = "4013752019004"

    $.ajax({
        url: "https://127.0.0.1:5000/getProductFromEan",
        type: "POST",
        data: { ean: result },
        success: function(response) {
            console.log(response.values);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function error(err) {
    console.error(err);
}
