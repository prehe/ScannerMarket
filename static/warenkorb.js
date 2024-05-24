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
            var spanElement = document.getElementById("quantity_" + productId);
            var currentAmount = parseInt(spanElement.innerText);
            spanElement.innerText = currentAmount + 1;
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
            }
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(error);
        }
    });
}

