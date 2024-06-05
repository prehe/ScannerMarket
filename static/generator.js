
function generateQR() {
    $.ajax({
        url: "/generateQR",
        type: "GET",
        success: function(response) {
            const qrcodeoutput = document.getElementById('qrcodeoutput');
            const outputElementWidth = qrcodeoutput.offsetWidth;

            const displayHeight = window.innerHeight;
            const navbar = document.getElementById("navbar").offsetHeight;
            const footer = document.getElementById("footer").offsetHeight;

            var height1 = displayHeight - navbar - footer - 120;
            if (height1 < outputElementWidth) {
                outputHeight = height1;
                console.log("outputHeight height 1:", outputHeight);  // Debugging line
            } else {
                outputHeight = outputElementWidth;
                console.log("outputHeight:", outputHeight);  // Debugging line
            }

            // const mainContainer = document.getElementById('main-container');
            // const mainContainerHeight = mainContainer.offsetWidth;

            // const top = document.getElementById('title-basket-list');
            // const topHeight = top.offsetHeight;

            // const bottom = document.getElementById('backToMenuBtn');
            // const bottomHeight = bottom.offsetHeight;

            // var outputSize = mainContainerHeight - topHeight - bottomHeight;

            // console.log("mainContainerHeight:", mainContainerHeight);  // Debugging line
            // console.log("topHeight:", topHeight);  // Debugging line
            // console.log("bottomHeight:", bottomHeight);  // Debugging line

            qrcodeoutput.innerHTML = "";  // Clear the previous QR code
            
            new QRCode(qrcodeoutput, {
                text: response,
                width: outputHeight,
                height: outputHeight,
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
