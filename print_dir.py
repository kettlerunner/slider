import cv2
import numpy as np
import glob
import os
import random
import requests
import json
import urllib

url = "https://dancrouse.com/slider"
local_base = "images/"
image_locations = "https://dancrouse.com/static/img/slider/"
framename = "slideshow"
path = "images/"

filenames = glob.glob(os.path.join(path, "*"))

for filename in filenames:
  print(filename)
