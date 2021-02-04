import asyncio
import os
from asyncio.tasks import shield
from loader import bot
from data.config import BASE_DIR
from .convert_pdf_to_tiff import pdf_to_tiff


async def run(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        shell=True,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    if stderr:
        print(stderr.decode())


async def _to_pdf(file: str):

    file_pdf = f'{file.split(".")[0]}.pdf'
    file_pdf_dir = f'{os.path.join(BASE_DIR, "excel",file)}'
    await shield(run(f'unoconv -f pdf {file_pdf_dir}'))
    return file_pdf


async def to_tiff(file: str):
    pdf_file = await shield(_to_pdf(file))
    tiff_file = await shield(pdf_to_tiff(pdf_file))


    return tiff_file
