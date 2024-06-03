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

    // Calculate the available height for the main container
    const availableHeight = displayHeight - footerHeight - navbarHeight;

    // Set the height and width of the main container
    mainContainer.style.height = `${availableHeight}px`;
    mainContainer.style.maxHeight = `${availableHeight}px`;
    mainContainer.style.width = `${displayWidth}px`;
    mainContainer.style.maxWidth = `${displayWidth}px`;
    basicContainer.style.width = `${displayWidth}px`;

    // Ensure footer and basicContainer have the correct width
    try {
        footer.style.width = `${displayWidth}px`;
    } catch (e) {
        console.log(e);
    }

    // // Ensure no element exceeds the intended width
    const elements = [mainContainer, footer, basicContainer];
    elements.forEach(element => {
        if (element.offsetWidth > displayWidth) {
            element.style.width = `${displayWidth}px`;
        }
    });
}

// Call the function on window resize and load
window.addEventListener('resize', adjustHeight);
window.addEventListener('load', adjustHeight);
