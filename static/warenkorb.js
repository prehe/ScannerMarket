// WARENKORB ############################################################################################
// Funktion, die beim Klicken auf den "+"-Button aufgerufen wird
function increaseAmount(einkaufId, productId) {
    $.ajax({
        url: "/increase_cart_amount",
        type: "POST",
        data: {
            einkauf_id: einkaufId,
            produkt_id: productId
        },
        success: function(response) {
            if (response.success == "increased"){
                var spanElement = document.getElementById("quantity_" + productId);
                var currentAmount = parseInt(spanElement.innerText);
                spanElement.innerText = currentAmount + 1;

                var priceElement = document.getElementById("total-price");
                var currentPrice = parseFloat(priceElement.innerText);
                currentPrice += response['price'];
                currentPrice = currentPrice.toFixed(2);

                priceElement.innerText = currentPrice;
            }
            window.location.href = response.redirect_url;
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(error);
        }
    });
}

// Funktion, die beim Klicken auf den "-"-Button aufgerufen wird
function decreaseAmount(einkaufId, productId) {
    $.ajax({
        url: "/decrease_cart_amount",
        type: "POST",
        data: {
            einkauf_id: einkaufId,
            produkt_id: productId
        },
        success: function(response) {
            // Handle success, update the quantity display
            var spanElement = document.getElementById("quantity_" + productId);
            var currentAmount = parseInt(spanElement.innerText);
            if (currentAmount >  1){
                spanElement.innerText = currentAmount - 1;
                var priceElement = document.getElementById("total-price");
                var currentPrice = parseFloat(priceElement.innerText);
                currentPrice -= response['price'];
                currentPrice = currentPrice.toFixed(2);
                
                priceElement.innerText = currentPrice;
            }
            window.location.href = response.redirect_url;
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(error);
        }
    });
}

let currentDeleteProductId = null;
let currentShoppingCardId = null;
let currentProdName = null;

function confirmDelete(shoppingCardId, productId, hersteller, productName) {
    currentDeleteProductId = productId;
    currentShoppingCardId = shoppingCardId;
    // Get product name from the hidden input field
    var productNameInput = document.getElementById("productName_" + productId);
    if (productNameInput) {
        var currentProdName = hersteller + " " + productName;
        productNameInput.value = currentProdName;
        // Optionally, display the product name in the modal
        document.getElementById("productNameDisplay").innerText = currentProdName;
    }
}


function deleteItemFromList() {
    $.ajax({
        url: "/deleteItemFromList",
        method: "POST",
        data: {
            einkauf_id: currentShoppingCardId,
            produkt_id: currentDeleteProductId
        },
        success: function(response) {
            if (response.value == "removed") {
                var deleteModal = document.getElementById('deleteConfirmationModal');
                deleteModal.setAttribute('aria-hidden', 'true');
                console.log(response.redirect_url);
                window.location.href = response.redirect_url;
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}

function purchase() {
    // var preisElement= document.getElementById("total-price");
    // var preis = preisElement.parseInt(preisElement.innerText);
    $.ajax({
        url: "/purchase",
        method: "POST",
        // data: {
        //     preis: preis
        // },
        success: function(response) {
            console.log(response.success)
            console.log(response.redirect_url)
            if (response.success) {
                var purchaseModal = document.getElementById('purchaseConfirmationModal');
                purchaseModal.setAttribute('aria-hidden', 'true');
                console.log(response.redirect_url);
                window.location.href = response.redirect_url;
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}


// Funktion zum Ausblenden der Flash-Nachricht nach einer Verzögerung
function hideFlashMessage() {
    var alertContainer = document.querySelector('.alert-container');
    if (alertContainer) {
        setTimeout(function() {
            alertContainer.style.display = 'none';
        }, 3000); // Verzögerung von 5000 Millisekunden (5 Sekunden)
    }
}

// Rufen Sie die Funktion zum Ausblenden der Flash-Nachricht auf, wenn die Seite geladen ist
document.addEventListener("DOMContentLoaded", function() {
    hideFlashMessage();
});


// temporäre Funktion   //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function addProductInstant(){
    $.ajax({
        url: "/addProdToBasket",
        type: "POST",
        data: {
            productId: 5,
            quantity: 3
        },
        success: function(response) {
            if (response.success) {
                // Redirect to the URL provided in the response
                window.location.href = response.redirect_url;
            } else {
                // Handle the error case, if needed
                console.error(response.message);
                alert(response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////