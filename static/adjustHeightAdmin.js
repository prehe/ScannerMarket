function adjustHeight() {
    // Get the height and width of the viewport
    const displayHeight = window.innerHeight;
    const displayWidth = window.innerWidth;

    // Get the main container element and its height navbar
    const mainContainer = document.getElementById("main-container");
    const navbar = document.getElementById("navbar");
    const navbarHeight = navbar ? navbar.offsetHeight : 0;
    const basicContainer = document.getElementById("container-fluid");
    const footer = document.getElementById("footer");
    const footerHeight = footer ? footer.offsetHeight : 0;

    console.log("displayHeight: ", displayHeight);
    console.log("footerHeight: ", footerHeight);
    console.log("navbar: ", navbarHeight);

    // Calculate the available height for the main container
    const availableHeight = displayHeight - footerHeight - navbarHeight - 30;

    console.log("availableHeight: ", availableHeight);

    // Set the height and width of the main container
    try {
        mainContainer.style.height = `${availableHeight}px`;
    } catch (e) {
    }


    // Ensure footer and basicContainer have the correct width
    try {
        footer.style.width = `${displayWidth}px`;
    } catch (e) {
    }
}

// Call the function on window resize and load
window.addEventListener('resize', adjustHeight);
window.addEventListener('load', adjustHeight);
