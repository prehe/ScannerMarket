const scanner = new Html5QrcodeScanner('reader', {
    qrbox: {
        width: 250,
        height: 250,
    },
    fps: 30,
});

scanner.render(success, error);

function success(result) {
    console.error(result);
    scanner.clear();
    document.getElementById('result').style.display = "block";
    document.getElementById('reader').style.display = 'none';
    result = "4061458042918";

    $.ajax({
        url: "https://127.0.0.1:5000/getProductFromEan",
        type: "POST",
        data: { ean: result },
        success: function(response) {
            document.getElementById("manufacturer").innerText = response.manufacturer;
            document.getElementById("product").innerText = response.productName;
            document.getElementById("price").innerText = "Preis: " + response.price + "€";
            document.getElementById("weight").innerText = "Menge/Volumen: " + response.weight;
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function error(err) {
    console.error(err);
}



// Function to decrease quantity
function decreaseQuantity() {
    var quantityElement = document.getElementById("quantity");
    var currentQuantity = parseInt(quantityElement.innerHTML);
    if (currentQuantity > 1) {
        quantityElement.innerHTML = currentQuantity - 1;
    }
}

// Function to increase quantity
function increaseQuantity() {
    var quantityElement = document.getElementById("quantity");
    var currentQuantity = parseInt(quantityElement.innerHTML);
    if (currentQuantity < 10) {
        quantityElement.innerHTML = currentQuantity + 1;
    }
}




