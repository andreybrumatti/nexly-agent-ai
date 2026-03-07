import io

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.core.config import settings
from src.integrations.mistral_client import MistralClient
from src.services.forecast_service import ForecastService

router = APIRouter()
forecast_service = ForecastService()
ai_client = MistralClient()


@router.post("/predict")
async def predict_sales(
    file: UploadFile = File(...),
    col_date: str = Form(...),
    col_amount: str = Form(...),
    period_type: str = Form(...),
    period_amount: int = Form(...),
):
    content = await file.read()
    filename = file.filename or ""

    try:
        df = (
            pd.read_csv(io.BytesIO(content))
            if filename.endswith(".csv")
            else pd.read_excel(io.BytesIO(content))
        )
        df.columns = df.columns.str.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Erro ao processar arquivo: {str(e)}"
        )

    try:
        data_final, tech_freq = forecast_service.run_prediction(
            df, col_date, col_amount, period_type, period_amount
        )
    except KeyError:
        return {
            "error": "Colunas não encontradas no arquivo",
            "disponivel": df.columns.tolist(),
        }

    period_human_name = settings.MAP_HUMAN.get(tech_freq, "períodos")
    insight = ai_client.get_business_insight(
        data_final, period_human_name, period_amount
    )

    return {
        "status": "success",
        "configuration": {
            "type": period_type,
            "amount": period_amount,
            "tech_freq": tech_freq,
        },
        "forecast": data_final,
        "insight_ia": insight,
    }
