function adjustHeight() {
    // Hole die Höhe und Breite des Viewports
    const displayHeight = window.innerHeight;
    const displayWidth = window.innerWidth;

    // Hole die Hauptelemente und ihre Höhen, sowie die Höhe der Navigationsleiste
    const mainContainer = document.getElementById("main-container");
    const navbar = document.getElementById("navbar");
    const navbarHeight = navbar ? navbar.offsetHeight : 0;
    const basicContainer = document.getElementById("container-fluid");
    const footer = document.getElementById("footer");
    const footerHeight = footer ? footer.offsetHeight : 0;

    // Berechne die verfügbare Höhe für den Hauptcontainer
    const availableHeight = displayHeight - footerHeight - navbarHeight - 30;

    // Setze die Höhe des Hauptcontainers
    try {
        if (mainContainer) {
            mainContainer.style.height = `${availableHeight}px`;
        }
    } catch (e) {
        console.error("Fehler beim Setzen der Höhe des Hauptcontainers: ", e);
    }

    // Stelle sicher, dass der Footer die korrekte Breite hat
    try {
        if (footer) {
            footer.style.width = `${displayWidth}px`;
        }
    } catch (e) {
        console.error("Fehler beim Setzen der Breite des Footers: ", e);
    }
}

// Rufe die Funktion beim Ändern der Fenstergröße und beim Laden der Seite auf
window.addEventListener('resize', adjustHeight);
window.addEventListener('load', adjustHeight);
