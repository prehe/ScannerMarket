function adjustHeight() {
    // Get the height and width of the viewport
    const displayHeight = window.innerHeight;
    const displayWidth = window.innerWidth;

    // Get the main container element and its height navbar
    const mainContainer = document.getElementById("main-container");
    const navbar = document.getElementById("navbar");
    const navbarHeight = navbar ? navbar.offsetHeight : 0;
    const footer = document.getElementById("footer");
    const footerHeight = footer ? footer.offsetHeight : 0;

    // Calculate the available height for the main container
    const availableHeight = displayHeight - footerHeight - navbarHeight;

    // console.log("Display height: ", displayHeight);
    // console.log("Available height: ", availableHeight);
    // console.log("Main-container height: ", mainContainer.offsetHeight);

    const tooMuchSize = mainContainer.offsetHeight - availableHeight;

    // console.log("Too much size: ", tooMuchSize);

    mainContainer.style.height = `${availableHeight}px`;

    // Get all images in the main container

    // const gridElement = document.getElementById("main-grid");
    // const gridHeight = gridElement.offsetHeight;
    // console.log("Grid height: ", gridHeight);

    // if (gridHeight > availableHeight) {
    //     gridElement.style.height = `${availableHeight}px`;
    // }

    const images = document.querySelectorAll("#main-container .category-item");
    
    if (displayWidth > 768) {   
        var maxHeight = availableHeight/3 - 5; // Set your desired maximum height
    } else{
        var maxHeight = availableHeight/5 - 5; // Set your desired maximum height
    }


    // // Apply the calculated dimensions to all images
    images.forEach(image => {
        image.style.height = `${maxHeight}px`;
        image.style.objectFit = 'cover'; // Ensure images maintain aspect ratio and fit within the specified dimensions
        console.log("Adjusted image size: ", image.offsetWidth, image.offsetHeight);
    });
}

// Call the function on window resize and load
window.addEventListener('resize', adjustHeight);
window.addEventListener('load', adjustHeight);
