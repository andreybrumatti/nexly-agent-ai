import pandas as pd
from prophet import Prophet


class ForecastService:
    def __init__(self):
        self.map_tech = {
            "day": "D",
            "dia": "D",
            "week": "W",
            "semana": "W",
            "month": "MS",
            "mes": "MS",
            "mês": "MS",
            "year": "YS",
            "ano": "YS",
        }
        self.map_human = {"D": "dias", "MS": "meses", "YS": "anos", "W": "semanas"}

    def get_tech_freq(self, period_type: str) -> str:
        clean_input = period_type.lower().strip()
        return self.map_tech.get(clean_input, clean_input)

    def get_human_name(self, tech_freq: str) -> str:
        return self.map_human.get(tech_freq, "períodos")

    def run_prediction(
        self,
        df: pd.DataFrame,
        col_date: str,
        col_amount: str,
        period_type: str,
        period_amount: int,
    ):
        df_prophet = df[[col_date, col_amount]].copy()
        df_prophet.columns = ["ds", "y"]
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])

        tech_freq = self.get_tech_freq(period_type)

        if tech_freq != "D":
            df_prophet = (
                df_prophet.set_index("ds").resample(tech_freq).sum().reset_index()
            )

        model = Prophet()

        df_prophet["cap"] = df_prophet["y"].max() * 1.5
        df_prophet["floor"] = 0

        model = Prophet(growth="logistic")
        model.fit(df_prophet)

        future = model.make_future_dataframe(periods=period_amount, freq=tech_freq)
        future["cap"] = df_prophet["y"].max() * 1.5
        future["floor"] = 0

        forecast = model.predict(future)

        summary = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(
            period_amount
        )
        summary.columns = ["date", "estimate", "min_estimate", "max_estimate"]
        summary["date"] = summary["date"].dt.strftime("%Y-%m-%d")  # type: ignore

        return summary.to_dict(orient="records"), tech_freq  # type: ignore
