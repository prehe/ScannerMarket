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
        // Clear the scanner to avoid multiple scans
        scanner.clear();
   
        $.ajax({
            url: "/getProductFromEan",
            type: "GET",
            data: { ean: result },
            success: function(response) {
                if (response.error) {
                    console.log(response.error);
                    // Show flash message and set timeout to hide it
                    window.location.href = response.redirect_url;
                }
                // Display the product details if data is valid
                if (!response.error) {
                    document.getElementById('result').style.display = "none";
                    document.getElementById('reader').style.display = 'block';
                    document.getElementById('scannerBack').style.display = 'block';
                    
                    window.productId = response.ID;
                    document.getElementById('result').style.display = "block";
                    document.getElementById('reader').style.display = 'none';
                    document.getElementById('scannerBack').style.display = 'none';
                    document.getElementById("manufacturer").innerText = response.Hersteller;
                    document.getElementById("product").innerText = response.Name;
                    document.getElementById("price").innerText = "Preis: " + response.Preis + "€";
                    document.getElementById("weight").innerText = "Menge/Volumen: " + response.Gewicht_Volumen;
                    document.getElementById("productimage").src = response.Bild;

                    try {
                        // Adjust scanner
                        const mainContainer = document.getElementById("main-container");
                        const availableHeight = mainContainer.offsetHeight;

                        const topContent = document.getElementById("title-scanner");
                        const topContentHeight = topContent.offsetHeight;

                        const btn_scanner_footer = document.getElementById("btn-scanner-footer");
                        const btn_scanner_footertHeight = btn_scanner_footer.offsetHeight;

                        const product_element = document.getElementById("product_element");
                        product_element.style.height = `${availableHeight - topContentHeight - btn_scanner_footertHeight - 110}px`;
                        // console.log("product_element.style.height: ", product_element.style.height);
                    } catch (e) {
                        console.error(e);
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error(error);
                alert("An error occurred while fetching the product.");
                // Redirect to scanner page
                window.location.href = '/scanner';
            }
        });
    }
    
    function error(err) {
        console.error(err);
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
                    window.location.href = response.redirect_url;document.addEventListener("DOMContentLoaded", function() {
                        let scanner;
                    
                        // Initialisiere den QR-Code Scanner
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
                    
                        // Funktion, die bei erfolgreichem QR-Code Scan aufgerufen wird
                        function success(result) {
                            // Lösche den Scanner, um Mehrfachscans zu vermeiden
                            scanner.clear();
                       
                            // Sende AJAX-Anfrage, um Produktinformationen anhand des gescannten EAN-Codes abzurufen
                            $.ajax({
                                url: "/getProductFromEan",
                                type: "GET",
                                data: { ean: result },
                                success: function(response) {
                                    if (response.error) {
                                        console.log(response.error);
                                        // Zeige Flash-Nachricht und leite weiter, wenn ein Fehler auftritt
                                        window.location.href = response.redirect_url;
                                    }
                                    // Zeige Produktdetails an, wenn die Daten gültig sind
                                    if (!response.error) {
                                        document.getElementById('result').style.display = "none";
                                        document.getElementById('reader').style.display = 'block';
                                        document.getElementById('scannerBack').style.display = 'block';
                                        
                                        window.productId = response.ID;
                                        document.getElementById('result').style.display = "block";
                                        document.getElementById('reader').style.display = 'none';
                                        document.getElementById('scannerBack').style.display = 'none';
                                        document.getElementById("manufacturer").innerText = response.Hersteller;
                                        document.getElementById("product").innerText = response.Name;
                                        document.getElementById("price").innerText = "Preis: " + response.Preis + "€";
                                        document.getElementById("weight").innerText = "Menge/Volumen: " + response.Gewicht_Volumen;
                                        document.getElementById("productimage").src = response.Bild;
                    
                                        try {
                                            // Passe die Höhe des Produktbereichs an
                                            const mainContainer = document.getElementById("main-container");
                                            const availableHeight = mainContainer.offsetHeight;
                    
                                            const topContent = document.getElementById("title-scanner");
                                            const topContentHeight = topContent.offsetHeight;
                    
                                            const btn_scanner_footer = document.getElementById("btn-scanner-footer");
                                            const btn_scanner_footertHeight = btn_scanner_footer.offsetHeight;
                    
                                            const product_element = document.getElementById("product_element");
                                            product_element.style.height = `${availableHeight - topContentHeight - btn_scanner_footertHeight - 110}px`;
                                            // console.log("product_element.style.height: ", product_element.style.height);
                                        } catch (e) {
                                            console.error(e);
                                        }
                                    }
                                },
                                error: function(xhr, status, error) {
                                    console.error(error);
                                    alert("Ein Fehler ist beim Abrufen des Produkts aufgetreten.");
                                    // Weiterleitung zur Scanner-Seite
                                    window.location.href = '/scanner';
                                }
                            });
                        }
                        
                        // Funktion, die bei einem Scanfehler aufgerufen wird
                        function error(err) {
                            // console.error(err);
                        }
                    
                        // Funktion, um den Scanvorgang erneut zu starten
                        function rescan() {
                            document.getElementById('result').style.display = "none";
                            document.getElementById('reader').style.display = 'block';
                            document.getElementById('scannerBack').style.display = 'block';
                            initializeScanner();
                        }
                    
                        // Funktion, um die Menge zu verringern
                        function decreaseQuantity() {
                            var quantityElement = document.getElementById("quantity");
                            var currentQuantity = parseInt(quantityElement.innerHTML);
                            if (currentQuantity > 1) {
                                quantityElement.innerHTML = currentQuantity - 1;
                            }
                        }
                    
                        // Funktion, um die Menge zu erhöhen
                        function increaseQuantity() {
                            var quantityElement = document.getElementById("quantity");
                            var currentQuantity = parseInt(quantityElement.innerHTML);
                            if (currentQuantity < 10) {
                                quantityElement.innerHTML = currentQuantity + 1;
                            }
                        }
                    
                        // Funktion, um ein Produkt zum Warenkorb hinzuzufügen
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
                                        // Weiterleitung zur angegebenen URL im Antwortobjekt
                                        window.location.href = response.redirect_url;
                                        flash("Produkt erfolgreich zum Einkauf hinzugefügt", "success");
                                    } else {
                                        // Fehlerbehandlung, falls nötig
                                        console.error(response.message);
                                        alert(response.message);
                                    }
                                },
                                error: function(xhr, status, error) {
                                    console.error(error);
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
                    
                        // Initialisiere den Scanner beim Laden der Seite
                        initializeScanner();
                        hideFlashMessage();
                    
                        // Mache Funktionen global verfügbar, damit sie aus dem HTML aufgerufen werden können
                        window.rescan = rescan;
                        window.decreaseQuantity = decreaseQuantity;
                        window.increaseQuantity = increaseQuantity;
                        window.addProdToBasket = addProdToBasket;
                        window.hideFlash = hideFlashMessage;
                    });
                    
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

    // Funktion zum Ausblenden der Flash-Nachricht nach einer Verzögerung
    function hideFlashMessage() {
        var alertContainer = document.querySelector('.alert-container');
        if (alertContainer) {
            setTimeout(function() {
                alertContainer.style.display = 'none';
            }, 3000); // Verzögerung von 3000 Millisekunden (3 Sekunden)
        }
    }

    // Initialize the scanner when the page loads
    initializeScanner();
    hideFlashMessage();

    // Expose functions to the global scope so they can be called from HTML
    window.rescan = rescan;
    window.decreaseQuantity = decreaseQuantity;
    window.increaseQuantity = increaseQuantity;
    window.addProdToBasket = addProdToBasket;
    window.hideFlash  = hideFlashMessage;
});

