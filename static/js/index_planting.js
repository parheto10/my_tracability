const icon = L.icon({
  iconSize: [25, 41],
  iconAnchor: [10, 41],
  popupAnchor: [2, -40],
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png"
});

Promise.all([
  fetch("http://127.0.0.1:8000/api/details_plantings"),
  fetch("http://127.0.0.1:8000/api/details_plantings?format=json")
]).then(async ([response1, response2]) => {
  const responseData1 = await response1.json();
  const responseData2 = await response2.json();

  const data1 = responseData1;
  const data2 = responseData2;

  const plantings = L.featureGroup().addTo(map);

data1.forEach(({planting, espece, nb_plante, id }) => {
    plantings.addLayer(
      L.marker([planting.parcelle.latitude, planting.parcelle.longitude], { icon }).bindPopup(
        `
          <table class="table table-striped table-bordered">
            <thead style="align-items: center">
                <tr>
                  <th scope="col" class="center">ID</th>
                  <th scope="col" class="center">INFORMATIONS</th>
                </tr>
            </thead>
            <tbody style="align-items: center">
                <tr>
                    <th scope="col"><b>CAMPAGNE :</b></th>
                    <td class="text-uppercase"><strong>${planting.campagne}</strong></td>
                </tr>
                <tr>
                    <th scope="col"><b>PROJET :</b></th>
                    <td class="text-uppercase"><strong>${planting.projet.accronyme} - ${planting.projet.titre}</strong></td>
                </tr>
                <tr>
                    <th scope="col"><b>CODE PARCELLE :</b></th>
                    <td class="text-uppercase"><strong>${planting.parcelle.code}</strong></td>
                </tr>
                <tr>
                    <th scope="col"><b>COOPERATIVE :</b></th>
                    <td class="text-uppercase"><strong>${planting.parcelle.producteur.section.cooperative.sigle}</strong></td>
                </tr>
                <tr>
                    <th scope="col"><b>PRODUCTEUR :</b></th>
                    <td class="text-uppercase"><strong>${planting.parcelle.producteur.nom} ${planting.parcelle.producteur.prenoms}</strong></td>
                </tr>
                <tr>
                    <th scope="col"><b>CODE PRODUCTEUR :</b></th>
                    <td class="text-uppercase"><strong>${planting.parcelle.producteur.code}</strong></td>
                </tr>
                <tr>
                    <th scope="col"><b>COORDONNEES :</b></th>
                    <td class="text-uppercase">${planting.parcelle.latitude}, ${planting.parcelle.longitude}</td>
                </tr>
                <tr>
                    <th scope="col"><b>CERTIFICATION : </b></th>
                    <td class="text-uppercase">${planting.parcelle.certification}</td>
                </tr>
                <tr>
                    <th scope="col"><b>CULTURE :</b></th>
                    <td class="text-uppercase">${planting.parcelle.culture}</td>
                </tr>
                <tr>
                    <th scope="col"><b>SUPERFICIE</b></th>
                    <td class="text-uppercase">${planting.parcelle.superficie} (Ha)</td>
                </tr>
                <tr>
                    <th scope="col"><b>PLANTS RECUS</b></th>
                    <td class="text-uppercase">${planting.plant_recus}</td>
                </tr>
                <tr>
                    <th scope="col"><b>ESPECES</b></th>
                    <td class="text-uppercase">(${espece.libelle}==>${nb_plante})</td>
                </tr>
            </tbody>
          </table>
        `
      )
    );
  });

//  map.fitBounds(plantings.getBounds());
});

//Initialisation de la Map
var map = L.map('map').setView([7.539989, -5.547080], 7);
map.zoomControl.setPosition('topright');

var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
 maxZoom: 22,
 attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors - @Copyright - Agro-Map CI'
}).addTo(map);

//map Climat
var climat = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
 maxZoom: 22,
 attribution: '@Copyright - Agro-Map CI - Plantings'
});


// Ajouter Popup de Marquage
var singleMarker = L.marker([5.349390, -4.017050])
 .bindPopup("Bienvenus en .<br> Côte d'Ivoire.")
 .openPopup();

// Ajouter Calcul de Distance
L.control.scale().addTo(map);

//Afficher les Coordonnées sur la carte
map.on('mousemove', function (e) {
 //console.log(e);
 $('.coordinates').html(`lat: ${e.latlng.lat}, lng: ${e.latlng.lng}`)
});


//Charger les Villes sur la Carte
//L.geoJSON(data).addTo(map);
var marker = L.markerClusterGroup();
marker.addTo(map);

// Laeflet Layer control
var baseMaps = {
 'ROUTE': osm,
 'COUVERT FORESTIER': climat,
}

var markers = L.markerClusterGroup({
	spiderfyShapePositions: function(count, centerPt) {
        var distanceFromCenter = 35,
            markerDistance = 45,
            lineLength = markerDistance * (count - 1),
            lineStart = centerPt.y - lineLength / 2,
            res = [],
            i;

        res.length = count;

        for (i = count - 1; i >= 0; i--) {
            res[i] = new Point(centerPt.x + distanceFromCenter, lineStart + markerDistance * i);
        }

        return res;
    }
});

var overLayMaps = {
 // 'VILLES' : marker,
 // 'ABIDJAN': singleMarker
}
L.control.layers(baseMaps, overLayMaps, {collapse :false, position: 'topleft'}).addTo(map);




