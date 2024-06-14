function adjustHeight() {
    // Hole die Höhe und Breite des Viewports
    const displayHeight = window.innerHeight;
    const displayWidth = window.innerWidth;

    // Hole die Hauptelemente und ihre Höhen, sowie die Höhe der Navigationsleiste
    const mainContainer = document.getElementById("main-container");
    const navbar = document.getElementById("navbar");
    const navbarHeight = navbar ? navbar.offsetHeight : 0;
    const footer = document.getElementById("footer");
    const footerHeight = footer ? footer.offsetHeight : 0;

    // Berechne die verfügbare Höhe für den Hauptcontainer
    const availableHeight = displayHeight - footerHeight - navbarHeight;

    // Setze die Höhe des Hauptcontainers
    mainContainer.style.height = `${availableHeight}px`;

    // Hole alle Bilder innerhalb des Hauptcontainers, die die Klasse "category-item" haben
    const images = document.querySelectorAll("#main-container .category-item");
    
    // Bestimme die maximale Höhe für die Bilder basierend auf der Breite des Viewports
    if (displayWidth > 768) {   
        var maxHeight = availableHeight / 3 - 5; // Setze die gewünschte maximale Höhe (Desktop-Ansicht)
    } else {
        var maxHeight = availableHeight / 5 - 5; // Setze die gewünschte maximale Höhe (Mobile-Ansicht)
    }

    // Wende die berechneten Abmessungen auf alle Bilder an
    images.forEach(image => {
        image.style.height = `${maxHeight}px`;
        image.style.objectFit = 'cover'; // Stelle sicher, dass die Bilder das Seitenverhältnis beibehalten und innerhalb der angegebenen Abmessungen passen
        // console.log("Angepasste Bildgröße: ", image.offsetWidth, image.offsetHeight); // Ausgabe der angepassten Bildgröße zur Überprüfung
    });
}

// Rufe die Funktion beim Ändern der Fenstergröße und beim Laden der Seite auf
window.addEventListener('resize', adjustHeight);
window.addEventListener('load', adjustHeight);
