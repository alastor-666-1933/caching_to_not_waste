import os
import torch
import hashlib
import numpy as np
import folder_paths
from pathlib import Path
from typing import Iterable
from PIL import Image, ImageOps
from .config import CACHE_DIR
from .functions import AlwaysEqualProxy, compare_revision

any_type     = AlwaysEqualProxy("*")
lazy_options = {"lazy": True} if compare_revision(2543) else {}

class caching_text:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "identification": ("STRING", {"default": "text"}),
                "original_image": ("IMAGE",),
                "executor": ("STRING", lazy_options),
                "force_recreate": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("original_image", "cached_text",)
    FUNCTION     = "caching_text"
    CATEGORY     = "caching_to_not_wast"



    def caching_text(self, *args, **kwargs):
        os.makedirs(CACHE_DIR, exist_ok=True)

        text_path = caching_text.reference_text_cache_hash(kwargs['original_image'], kwargs['identification'] + '_txt_')

        if os.path.exists(text_path) and not kwargs['force_recreate']:
            return caching_text.return_cached_text(kwargs['original_image'], text_path)

        return caching_text.execute(self, args, text_path, kwargs)

    def reference_text_cache_hash(original_image, identification):
        image_tensor = original_image[0]
        if isinstance(image_tensor, torch.Tensor):
            image_array = image_tensor.cpu().numpy()
        else:
            image_array = image_tensor

        image_bytes = image_array.tobytes()
        md5_hash    = hashlib.md5(image_bytes).hexdigest()
        filename    = f"{identification}_{md5_hash}.txt"
        text        = os.path.join(CACHE_DIR, filename)

        return caching_text._resolve_path(text)

    def _resolve_path(text) -> Path:
        text_path = Path(folder_paths.get_annotated_filepath(text))
        return text_path

    def return_cached_text(original_image, text_path):
        with open(text_path, 'r', encoding='utf-8') as f:
            cached_text = f.read()
        return (original_image, cached_text)

    @classmethod
    def IS_CHANGED(self, original_image, executor, force_recreate, identification = None):
        image_path = caching_text._resolve_path(original_image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    def check_lazy_status(self, identification, original_image, force_recreate, executor=None):
        text_path = caching_text.reference_text_cache_hash(original_image, identification  + '_txt_')

        if os.path.exists(text_path) and not force_recreate:
            return caching_text.return_cached_text(original_image, text_path)

        return ["executor"]

    def execute(self, args, text_path, kwargs):
        print("\n\n Passou aqui!!!\n")

        text = kwargs['executor']
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)

        return (kwargs['original_image'], text)
