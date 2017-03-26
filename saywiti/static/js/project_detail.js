var map = L.map('map', {
  zoomControl: true
}).setView([-11.9700, -76.9990], 5);

var markers = L.markerClusterGroup();

L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy <a href="//osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function popupInfo(issue) {
  return '<a href=" ' + issue.detail_url + '">' + issue.title + '</a>';
}

$(document).on('ready', function () {
  $.getJSON('/api/v1/projects/' + project.slug + '/issues/', function (response) {
    response.data.forEach(function (issue) {
      var icon = L.icon({
        iconUrl: issue.category_icon,
        iconSize: [40, 40]
      });
      var marker = L.marker(issue.point.coordinates.reverse(), {
        icon: icon
      });
      marker.bindPopup(popupInfo(issue));
      markers.addLayer(marker);
    });
    // load the marker cluster
    map.addLayer(markers);
  });
});
