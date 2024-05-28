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

function purchase() {
    $.ajax({
        url: "/purchase",
        method: "POST",
        success: function(response) {
            if (response.success) {
                console.log("Operation successful");
            } else {
                console.log("Operation failed");
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}

function deleteItemFromList(shoppingcard_ID, product_ID){
    $.ajax({
        url: "/deleteItemFromList",
        method: "POST",
        data: {
            einkauf_id: shoppingcard_ID,
            produkt_id: product_ID
        },
        success: function(response) {   
            if (response.value == "removed") {
                var productRow = document.getElementById("product_row_" + product_ID);
                if (productRow) {
                    productRow.remove();

                    // Gesamtpreis anpassen nach Produktentfernung
                    var priceElement = document.getElementById("total-price");
                    var currentPrice = response.price;
                    currentPrice = currentPrice.toFixed(2);
                    
                    priceElement.innerText = currentPrice;
                }
            }
            
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}