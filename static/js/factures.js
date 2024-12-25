async function loadFactureTypes(logementId) {
    console.log("Loading facture types for logementId:", logementId);
    if (!logementId) {
        document.getElementById('factureTypeContainer').style.display = 'none';
        document.getElementById('graphContainer').style.display = 'none';
        document.getElementById('emptyFactureMsg').style.display = 'none';
        return;
    }

    try {
        const response = await fetch(`/get_facture_types?logement_id=${logementId}`);
        if (!response.ok) {
            console.error("Erreur serveur:", response.status);
            return;
        }
        const data = await response.json();
        console.log("Réponse reçue:", data);

        if (!data || !data.types) {
            console.error("data.types est introuvable dans la réponse.");
            return;
        }

        // Si la liste est vide, masque le conteneur et affiche le message
        if (data.types.length === 0) {
            document.getElementById('factureTypeContainer').style.display = 'none';
            document.getElementById('graphContainer').style.display = 'none';
            document.getElementById('emptyFactureMsg').textContent = "Ce logement n'a aucune facture.";
            document.getElementById('emptyFactureMsg').style.display = 'block';
            return;
        }

        // Sinon, efface le message éventuel et affiche le sélecteur
        document.getElementById('emptyFactureMsg').style.display = 'none';

        const select = document.getElementById('factureTypeSelect');
        select.innerHTML = '<option value="">Sélectionner un type de facture</option>';

        data.types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            select.appendChild(option);
        });

        document.getElementById('factureTypeContainer').style.display = 'block';
        document.getElementById('graphContainer').style.display = 'none';
    } catch (error) {
        console.error('Erreur:', error);
    }
}

//variable globale pour stocker l'instantiation du graphique
let myChart = null;
let barChart = null;

function loadGraph(factureTypeId) {
    if (!factureTypeId) {
        document.getElementById("graphContainer").style.display = "none";
        return;
    }

    fetch(`/get_facturesjson?facture_type_id=${factureTypeId}`)
        .then(response => response.json())
        .then(data => {
            // On détruit l'ancien graphique s’il existe
            if (myChart !== null) {
                myChart.destroy();
            }
            if (barChart !== null) {
                barChart.destroy();
            }

            const ctx = document.getElementById("graphMontant").getContext("2d");
            myChart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: "Montant",
                        data: data.montants,
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: "time",
                            time: {
                                unit: "month"
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Handle bar chart for comparison
            if (data.montants.length < 2) {
                document.getElementById("comparisonMsg").textContent = "Pas assez de factures existantes pour effectuer une comparaison.";
                document.getElementById("comparisonMsg").style.display = "block";
                document.getElementById("barChartTitle").style.display = "none";
            } else {
                document.getElementById("comparisonMsg").style.display = "none";
                const lastTwoDates = data.dates.slice(-2);
                const lastTwoMontants = data.montants.slice(-2);
                const difference = lastTwoMontants[1] - lastTwoMontants[0];

                document.getElementById("barChartTitle").textContent = `Économies réalisées depuis ${lastTwoDates[0]}`;
                document.getElementById("barChartTitle").style.display = "block";

                const barCtx = document.getElementById("barChart").getContext("2d");
                barChart = new Chart(barCtx, {
                    type: "bar",
                    data: {
                        labels: ["Économies"],
                        datasets: [{
                            label: "Différence",
                            data: [difference],
                            backgroundColor: difference >= 0 ? "rgba(75, 192, 192, 1)" : "rgba(255, 99, 132, 1)",
                            borderColor: difference >= 0 ? "rgba(75, 192, 192, 1)" : "rgba(255, 99, 132, 1)",
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }

            document.getElementById("graphContainer").style.display = "flex";
        });
}

function showForm(formId) {
    var form = document.getElementById(formId);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}