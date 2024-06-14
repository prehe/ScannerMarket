function generateQR() {
    $.ajax({
        url: "/generateQR", 
        type: "GET", 
        success: function(response) {
            // Erfolgreiche Antwort vom Server erhalten
            const qrcodeoutput = document.getElementById('qrcodeoutput'); 
            const outputElementWidth = qrcodeoutput.offsetWidth; 

            const displayHeight = window.innerHeight; 
            const navbar = document.getElementById("navbar").offsetHeight; 
            const footer = document.getElementById("footer").offsetHeight; 

            // Berechne die maximale Höhe für den QR-Code
            var height1 = displayHeight - navbar - footer - 120;
            if (height1 < outputElementWidth) {
                outputHeight = height1; // Setze die Höhe, wenn die berechnete Höhe kleiner ist als die Breite des Ausgabe-Elements
            } else {
                outputHeight = outputElementWidth; // Andernfalls setze die Breite des Ausgabe-Elements als Höhe
            }

            qrcodeoutput.innerHTML = ""; // Lösche den vorherigen QR-Code

            // Erstelle einen neuen QR-Code mit den gegebenen Parametern
            new QRCode(qrcodeoutput, {
                text: response, // Textinhalt des QR-Codes (vom Server erhalten)
                width: outputHeight, 
                height: outputHeight, 
                colorDark: '#000',
                colorLight: '#fff'
            });
        },
        error: function(xhr, status, error) {
            console.error(error); // Ausgabe des Fehlers in der Konsole
        }
    });
}

// Rufe die generateQR-Funktion auf, sobald das Dokument vollständig geladen ist
document.addEventListener("DOMContentLoaded", function() {
    generateQR();
});
