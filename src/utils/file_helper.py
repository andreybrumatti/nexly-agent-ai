import io

import pandas as pd
from fastapi import HTTPException, UploadFile


class FileHelper:
    @staticmethod
    async def parse_to_dataframe(file: UploadFile) -> pd.DataFrame:
        content = await file.read()
        filename = file.filename or ""

        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(
                    io.BytesIO(content),
                    sep=None,
                    engine="python",
                    quotechar='"',
                    on_bad_lines="skip",
                )
            elif filename.endswith((".xlsx", ".xls")):
                df = pd.read_excel(io.BytesIO(content))
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de arquivo inválido. Use .csv ou .xlsx",
                )

            df.columns = df.columns.str.strip()
            return df

        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Erro ao processar a estrutura do arquivo: {str(e)}",
            )
