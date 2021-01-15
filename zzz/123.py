import os
import pandas as pd
from PIL import Image

image = '/Users/qeqe/Downloads/Подпись_Алексея_Иванова.jpg'
path = '/Users/qeqe/Downloads/Регистрация.xlsx'

# excel = pd.read_excel(path, sheet_name='Регистрация').to_dict('index')
import numpy as np
import PIL
from PIL import Image

basewidth = 200
img = Image.open(image)
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
data = np.array(img)
r2, g2, b2, alpha2 = 255, 255, 255, 255  # Value that we want to replace it with

# red, green, blue, alpha = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
mask=0
data[:, :, :4][mask] = [r2, g2, b2, alpha2]

img = Image.fromarray(data)
img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
img.save('new.png')
