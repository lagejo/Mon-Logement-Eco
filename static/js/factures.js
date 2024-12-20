function loadFactureTypes(logementId) {
    if (logementId === "") {
        document.getElementById("factureTypeContainer").style.display = "none";
        document.getElementById("graphContainer").style.display = "none";
        return;
    }

    fetch(`/get_facture_types?logement_id=${logementId}`)
        .then(response => response.json())
        .then(data => {
            const factureTypeSelect = document.getElementById("factureTypeSelect");
            factureTypeSelect.innerHTML = '<option value="">Sélectionner un type de facture</option>';
            data.facture_types.forEach(type => {
                const option = document.createElement("option");
                option.value = type.id;
                option.textContent = type.nom;
                factureTypeSelect.appendChild(option);
            });
            document.getElementById("factureTypeContainer").style.display = "block";
        });
}

function loadGraph(factureTypeId) {
    if (factureTypeId === "") {
        document.getElementById("graphContainer").style.display = "none";
        return;
    }

    fetch(`/get_factures?facture_type_id=${factureTypeId}`)
        .then(response => response.json())
        .then(data => {
            const graphMontantCtx = document.getElementById("graphMontant").getContext("2d");

            const dates = data.factures.map(f => f.date);
            const montants = data.factures.map(f => f.montant);

            new Chart(graphMontantCtx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Montant',
                        data: montants,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        x: { type: 'time', time: { unit: 'month' } },
                        y: { beginAtZero: true }
                    }
                }
            });

            document.getElementById("graphContainer").style.display = "block";
        });
}