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



function generator(value) {
    const qrcodeoutput = document.getElementById('qrcodeoutput');
    const mainContainer = document.getElementById("main-container");

    console.log(mainContainer);  // Debugging line
    if (!mainContainer) {
        console.error("Element with ID 'main-container' not found.");
        return;
    }

    const mainContainerWidth = mainContainer.offsetWidth;
    console.log("Main container width:", mainContainerWidth);  // Debugging line

    qrcodeoutput.innerHTML = "";  // Clear the previous QR code

    value="Einkauf_ID=123";
    
    new QRCode(qrcodeoutput, {
        text: value,
        width: mainContainerWidth,
        height: mainContainerWidth,
        colorDark: '#000',
        colorLight: '#fff'
    });
}