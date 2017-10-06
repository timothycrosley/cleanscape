STARTING_POINT = [-122.349358, 47.620422]  # Space Needle
points = {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'Point',
                                                                                     'coordinates': STARTING_POINT}}]}

mapboxgl.accessToken = 'pk.eyJ1IjoidGltb3RoeWNyb3NsZXkiLCJhIjoiY2o3d3lkaGkzNWhwcDJ3dDZqd2hqdDIzdCJ9.hVbXFoGCYADmX-M6K9gn7w'
map = new mapboxgl.Map({'container': 'map', 'style': 'mapbox://styles/mapbox/streets-v9', 'center': STARTING_POINT,
                        'zoom': 10})
canvas = map.getCanvasContainer()


def mouse_down(event):
    var coords = event.lngLat
    points.features[0].geometry.coordinates = [coords.lng, coords.lat]
    map.getSource('point').setData(points)


def init_map():
    map.addSource('point', {'type': 'geojson', 'data': points})
    map.addLayer({'id': 'point', 'type': 'circle', 'source': 'point', 'paint': {'circle-radius': 10,
                                                                                'circle-color': '#3887be'}})
    map.on('mousedown', mouse_down)


map.on('load', init_map)
