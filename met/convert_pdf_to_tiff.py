from asyncio.tasks import shield
from loader import bot
import os
from data.config import BASE_DIR
from pdf2image import convert_from_path


async def pdf_to_tiff(file: str) -> str:
    file_pdf_dir = os.path.join(BASE_DIR, 'excel', file)
    pages = convert_from_path(
        file_pdf_dir,
        dpi=300,
        grayscale=True,
        output_folder=os.path.join(BASE_DIR, 'TEMP')
    )
    for n, page in enumerate(pages):
        base_filename = os.path.splitext(os.path.basename(file_pdf_dir))[0] + f'{n}.tiff'
        tiff_dir = os.path.join(BASE_DIR, 'excel', base_filename)
        page.save(tiff_dir, 'JPEG')
        doc = open(tiff_dir, 'rb')
        await shield(bot.send_document(doc))
    # with tempfile.TemporaryDirectory() as path:
    #     images_from_path = convert_from_path(
    #         file_pdf_dir,
    #         output_folder=os.path.join(BASE_DIR, 'TEMP'),
    #         last_page=None,
    #         dpi=300,
    #         first_page=0,
    #         grayscale=True
    #     )
    # base_filename = os.path.splitext(os.path.basename(file_pdf_dir))[0] + '.tiff'
    # tiff_dir = os.path.join(BASE_DIR, 'excel', base_filename)
    # for page in images_from_path:
    #     page.save(tiff_dir, 'JPEG')
    # return tiff_dir
