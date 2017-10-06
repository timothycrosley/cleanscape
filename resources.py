import hug
from mapbox import Datasets


@hug.directive()
def datasets(*args, **kwargs):
    return Datasets()
