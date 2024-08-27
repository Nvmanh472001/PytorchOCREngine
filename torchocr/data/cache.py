import os
import shutil
import traceback
from pathlib import Path
from torchocr.utils.logging import get_logger

def cache(image_path, cache_dir, force_cache=False):
    if isinstance(image_path, Path):
        image_path = str(image_path)

    image = None
    img_save_path = f'{cache_dir}/{image_path}'

    if os.path.exists(img_save_path):
        return img_save_path

    os.makedirs(os.path.split(img_save_path)[0], exist_ok=True)

    if force_cache or not os.path.exists(img_save_path):
        shutil.copy2(image_path, img_save_path)

    if os.path.exists(img_save_path):
        return img_save_path
    else:
        logger = get_logger()
        logger.error(f'Failed to cache image {image_path}')
        return image_path