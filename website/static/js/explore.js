mapboxgl.accessToken = 'pk.eyJ1IjoidGltb3RoeWNyb3NsZXkiLCJhIjoiY2o3d3lkaGkzNWhwcDJ3dDZqd2hqdDIzdCJ9.hVbXFoGCYADmX-M6K9gn7w';
map = new mapboxgl.Map({'container': 'map', 'style': 'mapbox://styles/timothycrosley/cj8467x570gjd2rqivp8u35ye'});


function handle_map_click(event) {
    features = map.queryRenderedFeatures(event.point, {'layers': ['messes']});
    if (!features.length) {
        return;
    }
    var feature = features[0];
    popup = new mapboxgl.Popup({'offset': [0, -15] }).setLngLat(feature.geometry.coordinates).setHTML('<h3>' +
                feature.properties.name + '</h3><p>' + feature.properties.description + '</p><img src="' +
                feature.properties.image +
                '" height="200" width="200">').setLngLat(feature.geometry.coordinates).addTo(map);
}

map.on('click', handle_map_click);
