import asyncio
import os

from PIL import Image
from data.config import BASE_DIR


async def _to_tiff(file: str):
    file_tiff = f'{file.split(".")[0]}.tiff'
    file_tiff_dir = os.path.join(BASE_DIR, 'excel', file_tiff)
    im = Image.open(os.path.join(BASE_DIR, 'excel', file))
    s = im.convert('L')
    s.save(file_tiff_dir, 'JPEG', quality=100, dpi=[300, 300])
    print(file_tiff_dir)
    return file_tiff_dir

