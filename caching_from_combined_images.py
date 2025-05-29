import os
import torch
import hashlib
import numpy as np
import folder_paths
from pathlib import Path
from PIL import Image, ImageOps
from .config import CACHE_DIR
from .functions import AlwaysEqualProxy, compare_revision

any_type     = AlwaysEqualProxy("*")
lazy_options = {"lazy": True} if compare_revision(2543) else {}

class caching_from_combined_images:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "identification": ("STRING", {"default": "image"}),
                "original_image_1": ("IMAGE",),
                "original_image_2": ("IMAGE",),
                "executor": ("IMAGE", lazy_options),
                "force_recreate": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE",)
    RETURN_NAMES = ("original_image_1", "original_image_2", "cached_image",)
    FUNCTION     = "caching_from_combined_images"
    CATEGORY     = "caching_to_not_wast"



    def caching_from_combined_images(self, *args, **kwargs):
        os.makedirs(CACHE_DIR, exist_ok=True)

        image_path = self.reference_image_cache_hash(kwargs['original_image_1'], kwargs['original_image_2'], kwargs['identification'] + '_combined_img_')

        if os.path.exists(image_path) and not kwargs['force_recreate']:
            return self.return_cached_image(kwargs['original_image_1'], kwargs['original_image_2'], image_path)

        return self.execute(args, image_path, kwargs)

    def reference_image_cache_hash(self, original_image_1, original_image_2, identification):
        def to_numpy(image):
            if isinstance(image, torch.Tensor):
                return image.cpu().numpy()
            return image

        image_tensor_1 = original_image_1[0]
        image_tensor_2 = original_image_2[0]

        image_array_1 = to_numpy(image_tensor_1)
        image_array_2 = to_numpy(image_tensor_2)

        image_bytes = image_array_1.tobytes() + image_array_2.tobytes()
        md5_hash    = hashlib.md5(image_bytes).hexdigest()
        filename    = f"{identification}_{md5_hash}.png"
        image       = os.path.join(CACHE_DIR, filename)

        return self._resolve_path(image)

    @staticmethod
    def _resolve_path(image) -> Path:
        image_path = Path(folder_paths.get_annotated_filepath(image))
        return image_path

    def return_cached_image(self, original_image_1, original_image_2, image_path):
        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (original_image_1, original_image_2, image)

    @classmethod
    def IS_CHANGED(self, original_image_1, original_image_2, executor, force_recreate, identification=None):
        image_path = self._resolve_path(
            self.reference_image_cache_hash(original_image_1, original_image_2, identification)
        )

        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    def check_lazy_status(self, identification, original_image_1, original_image_2, force_recreate, executor=None):
        image_path = self.reference_image_cache_hash(original_image_1, original_image_2, identification  + '_combined_img_')

        if os.path.exists(image_path) and not force_recreate:
            return self.return_cached_image(original_image_1, original_image_2, image_path)

        return ["executor"]

    def execute(self, args, image_path, kwargs):
        image = kwargs['executor']

        control_tensor = image[0]
        if isinstance(control_tensor, torch.Tensor):
            control_array = (control_tensor.cpu().numpy() * 255).astype(np.uint8)
        else:
            control_array = (control_tensor * 255).astype(np.uint8)

        if control_array.shape[0] == 3:
            control_array = np.transpose(control_array, (1, 2, 0))  # CHW -> HWC

        control_image_pil = Image.fromarray(control_array)
        control_image_pil.save(image_path)

        return (kwargs['original_image_1'], kwargs['original_image_2'], image,)
