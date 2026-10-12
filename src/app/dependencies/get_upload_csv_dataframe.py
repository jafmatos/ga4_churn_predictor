import pandas
from fastapi import status
from fastapi import HTTPException
from fastapi import UploadFile


async def get_upload_csv_dataframe(upload_file: UploadFile):
    if (
        not upload_file.content_type == "text/csv"
        or not upload_file.filename.endswith(".csv")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo enviado deve ser do tipo CSV",
        )

    try:
        dataframe = pandas.read_csv(upload_file.file)

        if dataframe.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O arquivo enviado não pode estar vazio",
            )

        yield dataframe
    except pandas.errors.ParserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo enviado está corrompido ou mal formado",
        )
    finally:
        await upload_file.close()
