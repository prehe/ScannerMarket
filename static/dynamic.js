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