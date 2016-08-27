var categoryGroups = {};

var map = L.map('map', {
  zoomControl: false
}).setView([-11.9700, -76.9990], 6);
// Perú position

var zoom = new L.Control.Zoom({
  position: 'topright'
}).addTo(map);

var sidebar = L.control.sidebar('sidebar').addTo(map);

// Open settings panel at startup
sidebar.open('settings');

L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.control.locate({
  position: 'topright'
}).addTo(map);

function getPostInfo(post) {
  $.getJSON(post.url, function (response) {
    var $home = $('#home');
    $home.find('.title').html(response.data.name);
    $home.find('.content').html(response.data.content);
    sidebar.open('home');
  });
}

$(document).on('ready', function () {
  $.ajax({
    url: '/api/v1/posts/',
    method: 'get',
    dataType: 'json',
    success: function (response) {
      response.data.forEach(function (post) {
        var icon = L.icon({
          iconUrl: post.icon,
          iconSize: [40, 40]
        });
        var marker = L.marker([post.latitude, post.longitude], {
          icon: icon
        });
        var key = post.category_id;
        marker.on('click', function () {
          getPostInfo(post);
          map.setView(marker.getLatLng(), 15);
        });
        if (typeof categoryGroups[key] === 'undefined') {
          categoryGroups[key] = new L.LayerGroup();
        }
        categoryGroups[key].addLayer(marker);
      });
      // Add group layers to map
      Object.keys(categoryGroups).forEach(function (key) {
        categoryGroups[key].addTo(map);
      });
    }
  });
  $('.toggle-category').on('change', function () {
    var $this = $(this);
    var key = $this.data('category-id');
    if ($this.is(':checked')) {
      categoryGroups[key].addTo(map);
    } else {
      map.removeLayer(categoryGroups[key]);
    }
  });
});
