var map = L.map('map', {
  zoomControl: false
}).setView([-11.9700, -76.9990], 6);
// Perú position

var zoom = new L.Control.Zoom({
  position: 'topright'
}).addTo(map);

var sidebar = L.control.sidebar('sidebar').addTo(map);

L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.control.locate({
  position: 'topright'
}).addTo(map);

function postMarkerClicked(post) {
  return function () {
    $.getJSON(post.url, function (response) {
      var $home = $('#home');
      $home.find('.title').html(response.data.name);
      $home.find('.content').html(response.data.content);
      sidebar.open('home');
    });
  };
}

$(document).on('ready', function () {
  $.ajax({
    url: '/api/v1/posts/',
    method: 'get',
    dataType: 'json',
    success: function (response) {
      var layers = [];
      response.data.forEach(function (post) {
        var icon = L.icon({
          iconUrl: post.icon,
          iconSize: [40, 40]
        });
        var marker = L.marker([post.latitude, post.longitude], {
          icon: icon
        });
        marker.on('click', postMarkerClicked(post));
        layers.push(marker);
      });
      // TODO: remove this assignment
      window.posts = L.layerGroup(layers);
      window.posts.addTo(map);
    }
  });
});
