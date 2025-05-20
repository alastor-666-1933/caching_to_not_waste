import os
import torch
import hashlib
import numpy as np
import folder_paths
from pathlib import Path
from .config import CACHE_DIR
from .functions import AlwaysEqualProxy, compare_revision

any_type     = AlwaysEqualProxy("*")
lazy_options = {"lazy": True} if compare_revision(2543) else {}

class caching_condition:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "identification": ("STRING", {"default": "conditioning"}),
                "original_text": ("STRING", {"multiline": True}),
                "conditioning": ("CONDITIONING", lazy_options),
                "force_recreate": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    RETURN_NAMES = ("conditioning", "original_text",)
    FUNCTION     = "caching_condition"
    CATEGORY     = "caching_to_not_waste"

    def caching_condition(self, identification, original_text, conditioning, force_recreate):
        os.makedirs(CACHE_DIR, exist_ok=True)

        file_path = self.reference_cache_path(original_text, identification)

        if os.path.exists(file_path) and not force_recreate:
            return self.return_cached_conditioning(file_path, original_text)

        return self.execute(conditioning, file_path, original_text)

    def reference_cache_path(self, original_text, identification):
        md5_hash = hashlib.md5(original_text.encode('utf-8')).hexdigest()
        filename = f"{identification}_{md5_hash}.pt"
        file_path = os.path.join(CACHE_DIR, filename)
        return self._resolve_path(file_path)

    def _resolve_path(self, path_str) -> Path:
        return Path(folder_paths.get_annotated_filepath(path_str))

    def return_cached_conditioning(self, file_path, original_text):
        cached_tensor = torch.load(file_path, map_location='cpu')
        return (cached_tensor, original_text)

    def execute(self, conditioning, file_path, original_text):
        print("\n\n[CachingCondition] Saving conditioning to cache...\n")
        torch.save(conditioning, file_path)
        return (conditioning, original_text)

    @classmethod
    def IS_CHANGED(cls, original_text, conditioning, force_recreate, identification=None):
        return hashlib.sha256(original_text.encode('utf-8')).hexdigest()

    def check_lazy_status(self, identification, original_text, conditioning, force_recreate):
        file_path = self.reference_cache_path(original_text, identification)

        if os.path.exists(file_path) and not force_recreate:
            return self.return_cached_conditioning(file_path, original_text)

        return ["conditioning"]

