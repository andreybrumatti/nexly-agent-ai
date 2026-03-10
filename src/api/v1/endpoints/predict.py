from fastapi import APIRouter, File, Form, UploadFile

from src.core.config import settings
from src.integrations.mistral_client import MistralClient
from src.services.data_cleaning_service import DataCleaningService
from src.services.forecast_service import ForecastService
from src.utils.file_helper import FileHelper

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
    description_business: str = Form(...),
):
    df_raw = await FileHelper.parse_to_dataframe(file)

    df_clean = DataCleaningService.clean_sales_data(df_raw, col_date, col_amount)

    data_final, tech_freq = forecast_service.run_prediction(
        df_clean, col_date, col_amount, period_type, period_amount
    )

    for row in data_final:
        row["min_estimate"] = max(0, row["min_estimate"])

    period_human_name = settings.MAP_HUMAN.get(tech_freq, "períodos")
    insight = ai_client.get_business_insight(
        data_final, period_human_name, description_business, period_amount
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
