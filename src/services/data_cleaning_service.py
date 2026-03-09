import pandas as pd


class DataCleaningService:
    @staticmethod
    def clean_sales_data(
        df: pd.DataFrame, col_date: str, col_amount: str
    ) -> pd.DataFrame:
        df_clean = df.copy()

        if df_clean[col_amount].dtype == object:
            df_clean[col_amount] = (
                df_clean[col_amount]
                .astype(str)
                .str.replace(r"[R\$\s\.]", "", regex=True)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

        df_clean[col_amount] = pd.to_numeric(df_clean[col_amount], errors="coerce")

        df_clean[col_date] = pd.to_datetime(df_clean[col_date], errors="coerce")

        df_clean = df_clean.dropna(subset=[col_date, col_amount])

        df_clean = df_clean[df_clean[col_amount] >= 0]

        df_clean = df_clean.sort_values(by=col_date)  # type: ignore

        return df_clean
