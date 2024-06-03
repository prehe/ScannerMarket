// function generator(value) {
//     const qrcodeoutput = document.getElementById('qrcodeoutput');
//     const mainContainerWidth = document.getElementById("main-container").width;

//     qrcodeoutput.innerHTML = "";

//     new QRCode(qrcodeoutput, {
//         text: value,
//         width: 250,
//         height: 250,
//         colorDark: '#000',
//         colorLight: '#fff'
//     });
// }

// document.addEventListener("DOMContentLoaded", function() {
//     generator("Einkauf_ID=123");
// });



function generateQR() {
    $.ajax({
        url: "/generateQR",
        type: "GET",
        success: function(response) {
            const qrcodeoutput = document.getElementById('qrcodeoutput');
            const outputElementWidth = qrcodeoutput.offsetWidth;
            console.log("outputElementWidth:", outputElementWidth);  // Debugging line

            qrcodeoutput.innerHTML = "";  // Clear the previous QR code
            
            new QRCode(qrcodeoutput, {
                text: response,
                width: outputElementWidth,
                height: outputElementWidth,
                colorDark: '#000',
                colorLight: '#fff'
            });
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    generateQR();
});
