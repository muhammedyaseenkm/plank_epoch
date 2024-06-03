import os
import shutil
import uuid
from fastapi import UploadFile
from typing import Union
from redis import Redis


async def save_document_to_file_system(file:UploadFile, redis_client:Redis) -> str:
    try:
        unique_filename = str(uuid.uuid4())+os.path.splitext(file.filename)[1]
        save_directory = "/path/to/save"
        os.makedirs(save_directory, exist_ok=True)
        file_path = os.path.join(save_directory, unique_filename)
        with open(file_path,'wb') as f:
            while chunk := await file.read():
                f.write(chunk)
        if redis_client:
            redis_client.hmset(f"document:{unique_filename}", {"filename": file.filename, "file_path": file_path})
        return file_path

    except IOError as e:
        raise IOError(f"Failed to save document: {str(e)}")