import os
import time
from datetime import datetime, timedelta
from server import PromptServer
from aiohttp import web
from .config import CACHE_DIR

routes = PromptServer.instance.routes

@routes.post('/caching_clear')
async def caching_clear(request):
    the_data = await request.post()

    try:
        older_than_days = int(the_data.get("message", "0"))
    except ValueError:
        return web.json_response({
            "error": "Invalid value for 'message'"
        }, status=400)

    if not os.path.exists(CACHE_DIR):
        return web.json_response({"error": "CACHE_DIR not found"}, status=404)

    cutoff = time.time() - (older_than_days * 86400)

    deleted_files = []
    kept_files = []

    for root, dirs, files in os.walk(CACHE_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                file_mtime = os.path.getmtime(full_path)
                if file_mtime < cutoff:
                    os.remove(full_path)
                    deleted_files.append(full_path)
                else:
                    kept_files.append(full_path)
            except Exception as e:
                print(f"Error when processing file {full_path}: {e}")

    return web.json_response({
        "message": f"Clean cache for files with more than {older_than_days} days.",
        "deleted": deleted_files,
        "kept": kept_files
    })

