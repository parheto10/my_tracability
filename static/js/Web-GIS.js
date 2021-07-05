 // Ajouter Mode plein Ecran
 var mapId = document.getElementById('map');
 function fullScreenView(){
     if(document.fullscreenElement){
         document.exitFullscreen();
     } else {
        mapId.requestFullscreen();
     }
    
 }
 
 //leaflet Browser impression
 L.control.browserPrint({position:'topright'}).addTo(map);

  //Recherche Leaflet
  L.Control.geocoder().addTo(map);

  
 //Ajouter Fonction de Calcul de Distance
 L.control.measure({ 
    primaryLengthUnit: 'kilometers',
    secondaryLengthUnit: 'meters',
    primaryAreaUnit: 'hectares',
    secondaryAreaUnit: 'sqmeeters'
}).addTo(map);


   //Zoom Avant
 $('.zoom').click(function() {
    map.setView([7.539989, -5.547080], 7);
});