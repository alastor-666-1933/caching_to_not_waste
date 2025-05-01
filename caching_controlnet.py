import os
import torch
import hashlib
import numpy as np
import folder_paths
from pathlib import Path
from typing import Iterable
from PIL import Image, ImageOps
from .config import CACHE_DIR
# from .caching_controller import GLOBAL_CACHING_CONTROLLER
from .functions import AlwaysEqualProxy, compare_revision

any_type     = AlwaysEqualProxy("*")
lazy_options = {"lazy": True} if compare_revision(2543) else {}

class caching_controlnet:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "identification": (["openpose", "depth", "lineart", "scribble", "mlsd", "seg", "normal", "shuffle"],),
                "original_image": ("IMAGE",),
                "executor": ("IMAGE", lazy_options),
                "force_recreate": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE",)
    RETURN_NAMES = ("original_image", "cached_controlnet_image",)
    FUNCTION     = "caching_controlnet"
    CATEGORY     = "caching_to_not_wast"



    def caching_controlnet(self, *args, **kwargs):
        os.makedirs(CACHE_DIR, exist_ok=True)

        image_path = caching_controlnet.reference_image_cache_hash(kwargs['original_image'], kwargs['identification'] + '_cn_')

        if os.path.exists(image_path) and not kwargs['force_recreate']:
            return caching_controlnet.return_cached_image(kwargs['original_image'], image_path)

        return caching_controlnet.execute(self, args, image_path, kwargs)

    def reference_image_cache_hash(original_image, identification):
        image_tensor = original_image[0]
        if isinstance(image_tensor, torch.Tensor):
            image_array = image_tensor.cpu().numpy()
        else:
            image_array = image_tensor

        image_bytes = image_array.tobytes()
        md5_hash    = hashlib.md5(image_bytes).hexdigest()
        filename    = f"{identification}_{md5_hash}.png"
        image       = os.path.join(CACHE_DIR, filename)

        return caching_controlnet._resolve_path(image)

    def _resolve_path(image) -> Path:
        image_path = Path(folder_paths.get_annotated_filepath(image))
        return image_path

    def return_cached_image(original_image, image_path):
        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (original_image, image)

    @classmethod
    def IS_CHANGED(self, original_image, executor, force_recreate, identification = None):
        image_path = caching_controlnet._resolve_path(original_image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    def check_lazy_status(self, identification, original_image, force_recreate, executor=None):
        image_path = caching_controlnet.reference_image_cache_hash(original_image, identification  + '_cn_')

        if os.path.exists(image_path) and not force_recreate:
            return caching_controlnet.return_cached_image(original_image, image_path)

        return ["executor"]

    def execute(self, args, image_path, kwargs):
        image = kwargs['executor']

        control_tensor = image[0]
        if isinstance(control_tensor, torch.Tensor):
            control_array = (control_tensor.cpu().numpy() * 255).astype(np.uint8)
        else:
            control_array = (control_tensor * 255).astype(np.uint8)

        # Corrige formato HWC para PIL
        if control_array.shape[0] == 3:
            control_array = np.transpose(control_array, (1, 2, 0))  # CHW -> HWC

        control_image_pil = Image.fromarray(control_array)
        control_image_pil.save(image_path)

        return (kwargs['original_image'], image,)
