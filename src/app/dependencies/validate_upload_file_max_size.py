from fastapi import status
from fastapi import HTTPException
from fastapi import UploadFile


def get_upload_file_max_size(max_size_in_mb: int):
    async def validate_upload_file_max_size(upload_file: UploadFile):
        if upload_file.size > max_size_in_mb * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O arquivo enviado deve ter no máximo {max_size_in_mb:.2f} MB de tamanho. Atual: {(upload_file.size / (1024 ** 2)):.2f} MB",
            )

        yield upload_file

        await upload_file.close()

    return validate_upload_file_max_size
