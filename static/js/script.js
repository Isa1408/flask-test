function rechercheDeuxDates() {
    const du = document.getElementById("du").value;
    const au = document.getElementById("au").value;
    const etablissement = document.getElementById("etablissement-deroulant").value;

    let route = `/api/contrevenants?du=${du}&au=${au}`;
    if (etablissement) {
        route += `&etablissement-deroulant=`+etablissement;
    }
        fetch(route)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0 || data.error) {
                    resultat.innerHTML = `<p>${data.error}</p>`;
                    document.getElementById("tableau-resultat").style.display = "none";
                    return;
                }

                // Compter le nombre de contraventions par établissement
                const manipulerData = {};
                data.forEach(item => {
                    if (!manipulerData[item.etablissement]) {
                        manipulerData[item.etablissement] = 0;
                    }
                    manipulerData[item.etablissement] += 1;
                });

                const lignes = document.getElementById("tableau-resultat").querySelector("tbody");
                resultat.innerHTML = "";
                lignes.innerHTML = ""; 

                // Afficher les résultats
                Object.entries(manipulerData).forEach(([etablissement, nombre]) => {
                    const ligne = document.createElement("tr");
                    ligne.innerHTML = 
                    `
                        <td>${etablissement}</td>
                        <td>${nombre}</td>
                    `;
                    lignes.appendChild(ligne);
                });
                // On affiche le tableau
                document.getElementById("tableau-resultat").style.display = "table";
            })
            .catch(erreur => {
                console.log("Une erreur interne s'est produite : ", erreur);
                document.getElementById("tableau-resultat").style.display = "none";
            });  
}
document.getElementById("rechercher").addEventListener("click", rechercheDeuxDates);
// document.addEventListener("DOMContentLoaded", rechercheDeuxDates);

function filterEtablissement() {
    const du = document.getElementById("du").value;
    const au = document.getElementById("au").value;
    const deroulant = document.getElementById("etablissement-deroulant");

    if (du && au) {
        fetch(`/api/filtre_etablissements?du=${du}&au=${au}`)
            .then(response => response.json())
            .then(data => {
                deroulant.innerHTML = '<option value="" disabled selected>Choisissez un établissement</option>';

                if (data.error) {
                    console.error(data.error);
                    return;
                }

                data.forEach(etablissement => {
                    const choix = document.createElement('option');
                    choix.value = etablissement;
                    choix.textContent = etablissement;
                    deroulant.appendChild(choix);
                });
            })
            .catch(erreur => console.log("Une erreur interne s'est produite : ", erreur));
    }
};
document.getElementById("du").addEventListener("change", filterEtablissement);
document.getElementById("au").addEventListener("change", filterEtablissement);