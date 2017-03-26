$(document).on('ready', function () {
  var map = L.map('map', {
    zoomControl: true
  }).setView([-11.9700, -76.9990], 15);
  // TODO: change to use a reference from project object
  var marker = null;
  var $point = $('#id_point');

  function setupMarker(lat, lng) {
    if (marker === null) {
      marker = L.marker([lat, lng]);
      map.addLayer(marker);
    } else {
      marker.setLatLng([lat, lng]);
    }
  }

  L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy <a href="//osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Check if exists a point in the hidden value
  if ($point.val()) {
    // TODO: use a regex
    var coords = $point.val().replace('POINT (', '').replace(')', '').split(' ').map(parseFloat);
    setupMarker(coords[1], coords[0]);
  }

  map.on('click', function (e) {
    setupMarker(e.latlng.lat, e.latlng.lng);
    $point.val('POINT (' + e.latlng.lng + ' ' + e.latlng.lat + ')');
  });
});
