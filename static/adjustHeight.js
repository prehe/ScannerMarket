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

    // console.log("displayHeight: ", displayHeight);
    // console.log("footerHeight: ", footerHeight);
    // console.log("navbar: ", navbarHeight);

    // Calculate the available height for the main container
    const availableHeight = displayHeight - footerHeight - navbarHeight;

    // console.log("availableHeight: ", availableHeight);

    // Set the height and width of the main container
    if (mainContainer) {
        mainContainer.style.height = `${availableHeight}px`;
    }

    // Ensure footer and basicContainer have the correct width
    if (footer) {
        footer.style.width = `${displayWidth}px`;
    }

    // Ensure no element exceeds the intended width
    [mainContainer, footer, basicContainer].forEach(element => {
        if (element && element.offsetWidth > displayWidth) {
            element.style.width = `${displayWidth}px`;
        }
    });

    try {
        // WARENKORB BUTTONS AM ENDE DES WARENKORBES
        const bottomContent = document.getElementById("bottom-content");
        const bottomContentHeight = bottomContent ? bottomContent.offsetHeight : 0;

        const shoppinglistTitle = document.getElementById("shoppinglist_title");
        const shoppinglistTitleHeight = shoppinglistTitle ? shoppinglistTitle.offsetHeight : 0;

        const itemShoppingListContent = document.getElementById("item-shopping-list-content");
        if (itemShoppingListContent) {
            itemShoppingListContent.style.height = `${availableHeight - shoppinglistTitleHeight - bottomContentHeight}px`;
        }
    } catch (e) {
        console.log(e);
    }

    try {
        // Scanner anpassen
        const topContent = document.getElementById("title-scanner");
        const topContentHeight = topContent ? topContent.offsetHeight : 0;

        const scannerBack = document.getElementById("scannerBack");
        const bottomContentHeight = scannerBack ? scannerBack.offsetHeight : 0;

        var alertContainer = document.querySelector('.alert-container');
        const alertContainerHeight = alertContainer ? alertContainer.offsetHeight : 0;

        const reader = document.getElementById("reader");
        if (reader) {
            reader.style.height = `${availableHeight - bottomContentHeight - topContentHeight - alertContainerHeight - 50}px`;
        }
    } catch (e) {
        console.log(e);
    }

    try {
        // ADMIN - Analyse
        const navigationContent = document.getElementById("analysis-navigation");
        const navigationContentHeight = navigationContent ? navigationContent.offsetHeight : 0;

        const buttons = document.getElementById("analysis-button-line");
        const buttonsHeight = buttons ? buttons.offsetHeight : 0;

        const analysis = document.getElementById("analysis-container");
        if (analysis) {
            analysis.style.height = `${availableHeight - navigationContentHeight - buttonsHeight}px`;
        }
    } catch (e) {
        console.log(e);
    }
}

// Call the function on window resize and load
window.addEventListener('resize', adjustHeight);
window.addEventListener('load', adjustHeight);

// Ensure the DOM is fully loaded before calling adjustHeight
document.addEventListener("DOMContentLoaded", adjustHeight);
