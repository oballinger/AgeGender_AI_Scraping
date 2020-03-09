import cv2
from pyagender import PyAgender
import numpy as np
from tensorflow.keras import backend
import os
import tensorflow as tf
from PIL import Image
import requests
import urllib.request

from io import BytesIO
from bs4 import BeautifulSoup, SoupStrainer
import re
import math
import statistics
import pandas as pd
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
gnum=[]
ages=[]
urls=[]

path="/Users/ABC/Downloads/"
image=path+"filename.jpg"


url="https://en.wikipedia.org/wiki/Brad_Pitt"

## define image extraction functions

def scrape(x):
    response = requests.get(x, headers=headers)
    return BeautifulSoup(response.text, "html.parser")

def is_absolute(url):
    """
    Determines whether a `url` is absolute.
    """
    #print(url, bool(urlparse(url).netloc))
    return bool(urlparse(url).netloc)

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    srcs=[]
    images = scrape(url).find_all('img', {'src':re.compile('.jpg')})

    for image in images: 
        img=image['src']
        srcs.append(img)

    for i in srcs:
        if not is_absolute(i):
            # if img has relative URL, make it absolute by joining
            i = urljoin(url, i)
        if i[0:2]=="//":
            i="http:"+i
        if is_valid(i):
            urls.append(i)
    return urls 

## commence scraping

agender = PyAgender() 

for i in get_all_images(url):
    response = urllib.request.Request(i, headers=headers)

    try:
        with urllib.request.urlopen(response) as url:
            with open('temp.jpg', 'wb') as f:
                f.write(url.read())
    except:
        print("Error: image not read")
        pass

    try:
        faces = agender.detect_genders_ages(cv2.imread("temp.jpg"))
    except:
        b=get_all_images(i)
        print("no face detected")
        
    try:
        for data in faces:
            for key in data:
                if(key=='gender' or key == 'age'):
                    if key=='gender':
                        gen=data[key]
                    if key=='age':
                        age=data[key]
        gnum.append(gen)
        ages.append(age)
        print("Male" if gen<0.5 else "Female", '%.4s' % age, i)
    except: 
        print("estimation failed for url:", i)
        pass

