from email import message
import os
from io import BytesIO
from flask import Flask, request, send_from_directory, send_file, jsonify, request
from flask_pymongo import PyMongo
from PIL import Image
import numpy as np
import glob
import json
from bson.json_util import dumps
import skimage
import zipfile
from datetime import datetime

app = Flask(__name__, static_url_path='/static', static_folder = "./frontend/public")

app.config['MONGO_URI'] = "mongodb://%s:27017/main" % (os.environ.get('DB_PORT_27017_TCP_ADDR', 'db'))

mongo = PyMongo(app)

db = mongo.db

def display_array(arr):
    """
    Display an image represented as an array
    """
    img = Image.fromarray(arr.astype(np.uint8))
    bytesIO = BytesIO()
    img.save(bytesIO, 'PNG')
    bytesIO.seek(0)
    return bytesIO

def convert_to_array(path):
    """
    Converts an image file to an array for later processing
    """
    image_file = Image.open(path).convert("RGB")
    image_array = np.array(image_file)
    return image_array

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def base(path):
  return send_from_directory('frontend/public', 'index.html')

images = []
"""
populate_database() : reads all the PNG files in /app/assets, extract the values, store it to the main table in the db.
Arguments: None
Return: Success or Faliure Message
"""
@app.route('/api/populate_database')
def populate_database():
  try:
    for filename in glob.glob('assets/*.png'): 
      im = Image.open(filename)
      width, height = im.size
      area = width * height
      sizeBytes = os.stat(filename).st_size
      imageName = filename.split('/')[1]
      record = {
        'file_name' : imageName,
        'width' : width,
        'height' : height,
        'area' : area,
        'size' : sizeBytes
      }
      db.main.insert_one(record)
  except:
    jsonify(message="Failed")
    
  return jsonify(message="Success")

"""
all() : reads all the data in the db, returns it in JSON format.
Arguments: None
Return: dictionary of images or Faliure Message
"""
@app.route('/api/all')
def all():
  try:
    imgs = db.main.find()
    dictImgs = {}
    for img in imgs:
      img.pop('_id')
      dictImgs[img['file_name']] = img
  except:
    return jsonify(message="Failed")
  
  return json.loads(dumps(dictImgs))
"""
query() : finds images with: 
          width <= max_width,
          area >= min_area,
          size <= max_size_bytes
Arguments: max_width, min_area, max_size_bytes as query values, default values = 0
Return: dictionary of images or Faliure Message
TEST ROUTE: http://0.0.0.0:5000/api/query?max_width=999999&min_area=5&max_size_bytes=9999999
"""
@app.route('/api/query')
def query():
  args = request.args
  max_width = args.get('max_width',default=0, type=int)
  min_area = args.get('min_area', default=0, type=float)
  max_size_bytes = args.get('max_size_bytes', default=0, type=int)

  try:
    imgs = db.main.find({"$and" : [{"width" : {"$lte" : max_width}}, 
    {"area" : {"$gte" : min_area}}, 
    {"size" : {"$lte" : max_size_bytes}}]})
    dictImgs = {}
    for img in imgs:
      img.pop('_id')
      dictImgs[img['file_name']] = img
  except:
    return jsonify(message="Failed")
  
  return json.loads(dumps(dictImgs))

@app.route('/api/filter/<imagename>/<filtertype>')
def filter(imagename, filtertype):
  args = request.args
  value = args.get('value', default=0, type=int)

  img = db.main.find_one({"file_name" : imagename})
  img_name = img['file_name']
  img_path = os.path.join(os.getcwd(), "assets", img_name)
  print(img_path)
  if(os.path.exists(img_path)):

    im_arr = convert_to_array(img_path)

    if(filtertype == 'original'):
      return send_file(display_array(im_arr), mimetype='image/PNG')
    elif(filtertype == 'grayscale'):
      grey_img = np.mean(im_arr, axis=2)
      return send_file(display_array(grey_img), mimetype='image/PNG')
    elif(filtertype == 'downsample'):
      downsampled = skimage.transform.downscale_local_mean(im_arr, (value, value, value))
      return send_file(display_array(downsampled), mimetype='image/PNG')

  return jsonify(message="Filter Error.")


"""
query() : Creates a ZIP file backup from all the images in /app/assets
Arguments: None
Return: Success or Faliure Message
"""
@app.route('/api/backup')
def backup():
  try:
      
    now = datetime.now()
    zf = zipfile.ZipFile("backups/backup"+str(now), "w")
    for dirname, subdirs, files in os.walk("assets"):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

    return jsonify(message="Backup created successfully.")
  except:
    return jsonify(message="Faliure")






if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

