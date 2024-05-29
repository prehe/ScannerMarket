document.addEventListener("DOMContentLoaded", function() {
    let scanner;

    function initializeScanner() {
        scanner = new Html5QrcodeScanner('reader', {
            qrbox: {
                width: 250,
                height: 250,
            },
            fps: 30,
        });

        scanner.render(success, error);
    }

    function success(result) {
        // console.log(result);
        scanner.clear();
        document.getElementById('result').style.display = "block";
        document.getElementById('reader').style.display = 'none';
        document.getElementById('scannerBack').style.display = 'none';

        // Mock result for testing purposes
        result = "4061458042918"; // This line should be removed in production

        $.ajax({
            url: "/getProductFromEan",
            type: "GET",
            data: { ean: result },
            success: function(response) {
                // console.log(response);
                window.productId = response.ID;  // Corrected line
                document.getElementById("manufacturer").innerText = response.Hersteller;
                document.getElementById("product").innerText = response.Name;
                document.getElementById("price").innerText = "Preis: " + response.Preis + "€";
                document.getElementById("weight").innerText = "Menge/Volumen: " + response.Gewicht_Volumen;
                document.getElementById("productimage").src = response.Bild;
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }

    function error(err) {
        // console.error(err);
    }

    function rescan() {
        document.getElementById('result').style.display = "none";
        document.getElementById('reader').style.display = 'block';
        document.getElementById('scannerBack').style.display = 'block';
        initializeScanner();
    }

    function decreaseQuantity() {
        var quantityElement = document.getElementById("quantity");
        var currentQuantity = parseInt(quantityElement.innerHTML);
        if (currentQuantity > 1) {
            quantityElement.innerHTML = currentQuantity - 1;
        }
    }

    function increaseQuantity() {
        var quantityElement = document.getElementById("quantity");
        var currentQuantity = parseInt(quantityElement.innerHTML);
        if (currentQuantity < 10) {
            quantityElement.innerHTML = currentQuantity + 1;
        }
    }

    function addProdToBasket() {
        $.ajax({
            url: "/addProdToBasket",
            type: "POST",
            data: {
                productId: window.productId,
                quantity: parseInt(document.getElementById("quantity").innerText)
            },
            success: function(response) {
                if (response.success) {
                    // Redirect to the URL provided in the response
                    window.location.href = response.redirect_url;
                    flash("Produkt erfolgreich zum Einkauf hinzugefügt", "success");
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
    

    // Initialize the scanner when the page loads
    initializeScanner();

    // Expose functions to the global scope so they can be called from HTML
    window.rescan = rescan;
    window.decreaseQuantity = decreaseQuantity;
    window.increaseQuantity = increaseQuantity;
    window.addProdToBasket = addProdToBasket;
});
