document.addEventListener('DOMContentLoaded', function () {

var map = L.map('map').setView([27.9928478,84.5296624], 7.5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
    {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}        
        ).addTo(map)

        
  var latitudeInput = document.getElementById('latitude');
  var longitudeInput = document.getElementById('longitude');
  var locationForm = document.getElementById('locationForm');

  map.on('click', function (e) {
    var lat = e.latlng.lat.toFixed(6);
    var lng = e.latlng.lng.toFixed(6);

    latitudeInput.value = lat;
    longitudeInput.value = lng;
  });

  locationForm.addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Form submitted!\nLatitude: ' + latitudeInput.value + '\nLongitude: ' + longitudeInput.value);

    locationForm.submit();
});    
});
        