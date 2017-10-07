import os
import cloudinary

MESSES_DATASET = 'cj7ybqrsp43352qo3rdy8gmvq'

cloudinary.config(cloud_name=os.environ['CLOUDINARY_NAME'], api_key=os.environ['CLOUDINARY_KEY'], api_secret=os.environ['CLOUDINARY_SECRET'])
