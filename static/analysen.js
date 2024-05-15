const analysenDropdown = document.getElementById("dropdownMenuButton");

analysenDropdown.addEventListener('change', () => {
    if (analysenDropdown.value === 'Umsatz') {
        document.getElementById("Analysen-Feld").src = "/Umsatz";
        
    } else if (analysenDropdown.value === 'Neukunden'){
        document.getElementById("Analysen-Feld").src = "/Neukunden";
    }
    else if (analysenDropdown.value === 'Produktkategorien'){
        document.getElementById("Analysen-Feld").src = "/Produktkategorien";
    }
    else if (analysenDropdown.value === 'Produkte'){
        document.getElementById("Analysen-Feld").src = "/Produkte";
    }
    else if (analysenDropdown.value === 'Einkauf'){
        document.getElementById("Analysen-Feld").src = "/Einkauf";
    }
    else if (analysenDropdown.value === 'Warenkorb'){
        document.getElementById("Analysen-Feld").src = "/Warenkorb";
    }
    else if (analysenDropdown.value === 'Kunden'){
        document.getElementById("Analysen-Feld").src = "/Kunden";
    }
    else if (analysenDropdown.value === 'Bezahlmöglichkeiten'){
        document.getElementById("Analysen-Feld").src = "/Bezahlmöglichkeiten";
    }
    else if (analysenDropdown.value === 'Bezahlung'){
        document.getElementById("Analysen-Feld").src = "/Bezahlung";
    }

});