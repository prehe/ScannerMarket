// REGISTIERUNG ###################################################################################################
const zahlungsartDropdown = document.getElementById('bezahlmethode');
const paypalDetails = document.getElementById('paypal-details');
const kreditkarteDetails = document.getElementById('kreditkarte-details');
const paypalEmail = document.getElementById('paypal-email');
const kreditkarteNummer = document.getElementById('kreditkarte-nummer');
const kreditkarteGültigBis = document.getElementById('kreditkarte-gültig-bis');
const kreditkarteCvv = document.getElementById('kreditkarte-cvv');

zahlungsartDropdown.addEventListener('change', () => {
    if (zahlungsartDropdown.value === 'paypal') {
        paypalDetails.style.display = 'block';
        kreditkarteDetails.style.display = 'none';
        paypalEmail.required = true;
        kreditkarteNummer.required = false;
        kreditkarteGültigBis.required = false;
        kreditkarteCvv.required = false;
    } else if (zahlungsartDropdown.value === 'kreditkarte') {
        paypalDetails.style.display = 'none';
        kreditkarteDetails.style.display = 'block';
        paypalEmail.required = false;
        kreditkarteNummer.required = true;
        kreditkarteGültigBis.required = true;
        kreditkarteCvv.required = true;
    } else {
        paypalDetails.style.display = 'none';
        kreditkarteDetails.style.display = 'none';
        paypalEmail.required = false;
        kreditkarteNummer.required = false;
        kreditkarteGültigBis.required = false;
        kreditkarteCvv.required = false;
    }
});


// SCANNER ##########################################################################################

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
    result = "4013752019004"

    $.ajax({
        url: "https://127.0.0.1:5000/getProductFromEan",
        type: "POST",
        data: { ean: result },
        success: function(response) {
            console.log(response.values);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function error(err) {
    console.error(err);
}



// WARENKORB ############################################################################################
// Funktion, die beim Klicken auf den "+"-Button aufgerufen wird
function increaseAmount(einkaufId, productId) {
    var product = getProductById(einkaufId, productId);
    product.amount += 1;
    updateAmountDisplay(productId, product.amount);
}

// Funktion, die beim Klicken auf den "-"-Button aufgerufen wird
function decreaseAmount(einkaufId, productId) {
    var product = getProductById(einkaufId, productId);
    if (product.amount > 0) {
        product.amount -= 1;
        updateAmountDisplay(productId, product.amount);
    } else {
        removeProductRow(productId);
    }
}

// Funktion zum Aktualisieren des angezeigten Werts
function updateAmountDisplay(productId, newAmount) {
    var amountElement = document.getElementById("amount-" + productId);
    amountElement.innerText = newAmount;
}

// Funktion zum Entfernen der Produktzeile
function removeProductRow(productId) {
    var productRow = document.getElementById("product-" + productId);
    productRow.remove();
}
