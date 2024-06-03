const analysenDropdown = document.getElementById("dropdownMenuButton");

analysenDropdown.addEventListener('change', () => {
    if (analysenDropdown.value === 'Analysen') {
        document.getElementById("Analysen-Feld").src = "/Umsatz";
    }    
    else if (analysenDropdown.value === 'Produktkategorien'){
        document.getElementById("Analysen-Feld").src = "/Produktkategorien";
    }
    else if (analysenDropdown.value === 'Produkte'){
        document.getElementById("Analysen-Feld").src = "/Produkte";
    }
    else if (analysenDropdown.value === 'Einkaufe'){
        document.getElementById("Analysen-Feld").src = "/Einkauf";
    }
    else if (analysenDropdown.value === 'Warenkorb'){
        document.getElementById("Analysen-Feld").src = "/Warenkorb";
    }
    else if (analysenDropdown.value === 'Kunden'){
        document.getElementById("Analysen-Feld").src = "/Kunden";
    }
});