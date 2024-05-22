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
            console.log("Quantity increased successfully");
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
            console.log(response)
            var spanElement = document.getElementById("quantity_" + productId);
            var currentAmount = parseInt(spanElement.innerText);
            spanElement.innerText = currentAmount - 1;
            // console.log("Quantity decreased successfully");
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(error);
        }
    });
}

