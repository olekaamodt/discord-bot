import os
from instalooter.looters import ProfileLooter
import random
from PIL import Image
looter = ProfileLooter("marvelous_mikee")
looter.download('./Pictures', media_count=1)

def get_random_picture():
    path = os.path.dirname(os.path.abspath(__file__))
    return random.choice(os.listdir(path + "\Pictures"))
    
