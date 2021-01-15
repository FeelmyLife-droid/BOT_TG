import tempfile
import os
from data.config import BASE_DIR
from pdf2image import convert_from_path


async def pdf_to_tiff(file: str) -> str:
    file_pdf_dir = os.path.join(BASE_DIR, 'excel', file)
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(
            file_pdf_dir,
            output_folder=path,
            last_page=1,
            dpi=300,
            first_page=0,
            grayscale=True
        )
    base_filename = os.path.splitext(os.path.basename(file_pdf_dir))[0] + '.tiff'
    tiff_dir = os.path.join(BASE_DIR, 'excel', base_filename)
    for page in images_from_path:
        page.save(tiff_dir, 'JPEG')
    return tiff_dir
