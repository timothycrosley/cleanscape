import hug
import piexif
from cloudinary import uploader
from uuid import uuid4 as generate_id
from config import MESSES_DATASET
from resources import datasets
import controllers
import reverse_geocoder
from functools import partial
from mapbox import Uploader
from multipart import MultipartParser

app = hug.get(output=hug.output_format.suffix({'/js': hug.output_format.json},
                                              hug.output_format.html)).suffixes('/js')
html = partial(hug.transform.suffix, {'/js': None})


@hug.default_input_format('multipart/form-data')
def multipart(body, **header_params):
    """Converts multipart form data into native Python objects"""
    
    if header_params and 'boundary' in header_params:
        if type(header_params['boundary']) is str:
            header_params['boundary'] = header_params['boundary'].encode()
    parser = MultipartParser(stream=body,boundary=header_params['boundary'],disk_limit=17179869184)
    form = dict(zip([p.name for p in parser.parts()],\
        [(p.filename,p.file) if p.filename else p.file.read().decode() for p in parser.parts()]))
    return form


@hug.static('/static')
def my_static_dirs():
    return ('media', 'client_side/js')


@app.transform(html(controllers.explore))
def messes(datasets: datasets):
    """Returns a list of all known messes, their GPS coordinates and bounty"""
    return datasets.list_features(MESSES_DATASET).json()['features']


@app.transform(html(controllers.report))
def mess():
    return


@app.transform(html(controllers.report), accept='POST')
def mess(datasets: datasets, lat: hug.types.float_number, lon: hug.types.float_number, name: hug.types.length(1, 120),
         description: hug.types.length(1, 1000), image):
    """Report a mess at a specific lat/lon optionally with a bounty attached"""
    if reverse_geocoder.search((lat, lon))[0]['name'].lower() not in ['seattle', 'shoreline']:
        raise ValueError('Cleanscape is currently only for the Seattle area')

    mess_id = str(generate_id())
    mess = {'type': 'Feature', 'id': mess_id, 'properties': {'name': name, 'description': description,
                                                             'image': uploader.upload(image[1])['url']},
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]}}
    result = datasets.update_feature(MESSES_DATASET, mess_id, mess).json()
    refresh()
    return result
    

@hug.post()
def refresh():
    uploader = Uploader()
    uri = 'mapbox://datasets/timothycrosley/{}'.format(MESSES_DATASET)
    return uploader.create(uri, 'messes').json()


@hug.delete('/mess')
def delete_mess(datasets: datasets, id: hug.types.text):
    """Deletes an individual feature"""
    return datasets.delete_feature(MESSES_DATASET, id).json()


@hug.post()
def add_bounty(datasets: datasets, mess_id: hug.types.text, email, amount=""):
    """Adds a bounty to the specified mess"""
    

@hug.post()
def report_cleaned(datasets: datasets, id: hug.types.text, email):
    mess = datasets.read_feature(id)
    for email, amount in mess.get('properties', {}).get('bounties', {}).items():
        # venmo.request_money(
        pass


@app.transform(html(controllers.about))
def about():
    return
