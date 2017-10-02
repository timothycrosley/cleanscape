import hug
import piexif
from cloudinary import uploader
from uuid import uuid4 as generate_id
from .config import MESSES_DATASET
from .resources import datasets
import reverse_geocoder
from mapbox import Uploader


@hug.get()
def messes(datasets: datasets):
    """Returns a list of all known messes, their GPS coordinates and bounty"""
    return datasets.list_features(MESSES_DATASET).json()['features']


@hug.post('/mess')
def report_mess(datasets: datasets, lat: hug.types.float_number, lon: hug.types.float_number,
                image, name: hug.types.text="", description: hug.types.text=""):
    """Report a mess at a specific lat/lon optionally with a bounty attached"""
    if reverse_geocoder.search((lat, lon))[0]['name'].lower() not in ['seattle', 'shoreline']:
        raise ValueError('Cleanscape is currently only for the Seattle area')

    mess_id = str(generate_id())
    mess = {'type': 'Feature', 'id': mess_id, 'properties': {'name': name, 'description': description,
                                                             'image': uploader.upload(image)['url']},
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]}}
    return datasets.update_feature(MESSES_DATASET, mess_id, mess).json()


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
def add_bounty(datasets: datasets, mess_id: hug.types.text(), email, amount=""):
    """Adds a bounty to the specified mess"""


@hug.post()
def report_cleaned(datasets: datasets, id: hug.types.text, email):
    mess = datasets.read_feature(id)
    for email, amount in mess.get('properties', {}).get('bounties', {}).items():
        venmo.request_money(
