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
    const availableHeight = displayHeight - footerHeight - navbarHeight;

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

    // // Ensure no element exceeds the intended width
    try {
        const elements = [mainContainer, footer, basicContainer];
        elements.forEach(element => {
            if (element.offsetWidth > displayWidth) {
                element.style.width = `${displayWidth}px`;
            }
        });
    } catch (e) {
    }




    try {
        // WARENKORB BUTTONS AM ENDE DES WARENKORBES
        const bottomContent = document.getElementById("bottom-content");
        var bottomContentHeight = bottomContent.offsetHeight;   

        const shoppinglist_title = document.getElementById("shoppinglist_title");
        var shoppinglist_titleHeight = shoppinglist_title.offsetHeight;

        const item_shopping_list_content = document.getElementById("item-shopping-list-content");
        item_shopping_list_content.style.height = `${availableHeight - shoppinglist_titleHeight - bottomContentHeight}px`;
    } catch (e) {
    }

    try {
        //Scanner anpassen
        const topContent = document.getElementById("title-scanner");
        var topContentHeight = topContent.offsetHeight;   

        const bottomContent = document.getElementById("scannerBack");
        var bottomContentHeight = bottomContent.offsetHeight;
                
        const reader = document.getElementById("reader");
        reader.style.height = `${availableHeight - bottomContentHeight -topContentHeight-50}px`;
    } catch (e) {
    }
}

// Call the function on window resize and load
window.addEventListener('resize', adjustHeight);
window.addEventListener('load', adjustHeight);
