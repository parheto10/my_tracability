const icon = L.icon({
  iconSize: [25, 41],
  iconAnchor: [10, 41],
  popupAnchor: [2, -40],
  iconUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-shadow.png"
});

Promise.all([
  fetch(
    // "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
    "http://127.0.0.1:8000/api/parcelles"
  ),
  fetch("http://127.0.0.1:8000/api/parcelles?format=json")
]).then(async ([response1, response2]) => {
  const responseData1 = await response1.json();
  const responseData2 = await response2.json();

  const data1 = responseData1;
  const data2 = responseData2;

  const parcelles = L.featureGroup().addTo(map);

  data1.forEach(({cooperative, code, producteur, sous_section, acquisition, latitude, longitude, culture, certification, superficie  }) => {
    parcelles.addLayer(
      L.marker([latitude, longitude], { icon }).bindPopup(
        `
          <table class="table table-striped table-bordered">
            <thead>
                <tr>           
                  <th scope="col" class="center">ID</th>
                  <th scope="col" class="center">INFORMATIONS</th>                  
                </tr>
            </thead>
            <tbody>            
                <tr>
                    <th scope="col"><b>COOPERATIVE :</b></th>
                    <td>${cooperative}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>PRODUCTEUR :</b></th>
                    <td>${producteur}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>CODE PARCELLE :</b></th>
                    <td>${code}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>SECTION :</b></th>
                    <td>${sous_section}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>MODE D'ACQUISITION :</b></th>
                    <td>${acquisition}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>CERTIFICATION : </b></th>
                    <td>${certification}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>CULTURE :</b></th>
                    <td>${culture}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>SUPERFICIE</b></th>
                    <td>${superficie}</td>                    
                </tr>
            </tbody>
          </table>    
        `
      )
    );
  });

  map.fitBounds(parcelles.getBounds());
});

 //Initialisation de la Map
 var map = L.map('map').setView([7.539989, -5.547080], 7);
 map.zoomControl.setPosition('topright');

 var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     maxZoom: 20,
     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors - @Copyright - Agro-Map CI'
 }).addTo(map);

 //map Climat
 var climat = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
     maxZoom: 20,
     attribution: '@Copyright - Agro-Map CI - Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
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

 var overLayMaps = {
     // 'VILLES' : marker,
     // 'ABIDJAN': singleMarker
 }
 L.control.layers(baseMaps, overLayMaps, {collapse :false, position: 'topleft'}).addTo(map);



