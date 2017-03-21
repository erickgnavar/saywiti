var map = L.map('map', {
  zoomControl: true
}).setView(issue.point, 15);

L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy <a href="//osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var marker = L.marker(issue.point);

map.addLayer(marker);
