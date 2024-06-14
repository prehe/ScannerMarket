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
            var spanElement = document.getElementById("quantity_" + productId);
            var currentAmount = parseInt(spanElement.innerText);
            if (currentAmount > 1){
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
            console.error(error);
        }
    });
}

let currentDeleteProductId = null;
let currentShoppingCardId = null;
let currentProdName = null;

// Funktion zur Bestätigung der Löschung eines Produkts aus dem Warenkorb
function confirmDelete(shoppingCardId, productId, hersteller, productName) {
    currentDeleteProductId = productId;
    currentShoppingCardId = shoppingCardId;
    // Hole den Produktnamen aus dem versteckten Eingabefeld
    var productNameInput = document.getElementById("productName_" + productId);
    if (productNameInput) {
        var currentProdName = hersteller + " " + productName;
        productNameInput.value = currentProdName;
        // Zeige optional den Produktnamen im Modal an
        document.getElementById("productNameDisplay").innerText = currentProdName;
    }
}

// Funktion zum Löschen eines Produkts aus der Liste
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

// Funktion zum Abschluss des Kaufs
function purchase() {
    $.ajax({
        url: "/purchase",
        method: "POST",
        success: function(response) {
            // Bei Erfolg, schließe das Modal und leite weiter
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
        }, 3000); // Verzögerung von 3000 Millisekunden (3 Sekunden)
    }
}

// Rufe die Funktion zum Ausblenden der Flash-Nachricht auf, wenn die Seite geladen ist
document.addEventListener("DOMContentLoaded", function() {
    hideFlashMessage();
});

// Entwicklungsfunktion zum Testen des Warenkorbs (zum Testen in der Entwicklungsumgebung verwendet)    //////////////////////////////////////////////////////////////////////////////////
function addProductInstant(){
    // Sende AJAX-Anfrage, um ein Produkt sofort zum Warenkorb hinzuzufügen
    $.ajax({
        url: "/addProdToBasket",
        type: "POST",
        data: {
            productId: 5,
            quantity: 3
        },
        success: function(response) {
            // Bei Erfolg, leite zur angegebenen URL weiter
            if (response.success) {
                window.location.href = response.redirect_url;
            } else {
                // Fehlerbehandlung, falls nötig
                console.error(response.message);
                alert(response.message);
            }
        },
        error: function(xhr, status, error) {
            // Fehlerbehandlung
            console.error(error);
        }
    });
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////