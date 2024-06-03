function adjustHeight() {
    // Get the height of the viewport
    const displayHeight = window.innerHeight;

    // Get the main container element and its height navbar
    const mainContainer = document.getElementById("main-container");
    const mainContainerHeight = mainContainer ? mainContainer.offsetHeight : 0;

    const navbar = document.getElementById("navbar");
    const navbarHeight = mainContainer ? navbar.offsetHeight : 0;

    const basicContainer = document.getElementById("container-fluid");

    // Get the footer element and its height
    const footer = document.getElementById("footer");
    const footerHeight = footer ? footer.offsetHeight : 0;

    // Print the heights to the console for debugging
    console.log('Display Height:', displayHeight);
    if (mainContainer) {
        console.log('Main Container Height:', mainContainerHeight);
    } else {
        console.log('Main container element not found.');
    }
    if (footer) {
        console.log('Footer Height:', footerHeight);
    } else {
        console.log('Footer element not found.');
    }

    // Example: Adjust the height of the main container     container-fluid
    mainContainer.style.height = `${displayHeight - footerHeight - navbarHeight}px`;
    footer.style.width = `${window.innerWidth}px`;
    basicContainer.style.width = `${window.innerWidth}px`;
}

// Call the function to adjust the height when the page is loaded
document.addEventListener("DOMContentLoaded", function() {
    adjustHeight();
});

// Optionally, adjust the height again if the window is resized
window.addEventListener("resize", adjustHeight);
