from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_nexly_data(days=360):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    data = []
    base_sales = 1000

    for i, date in enumerate(date_range):
        trend = i * 5

        weekday_multiplier = 1.5 if date.weekday() >= 4 else 1.0

        noise = np.random.uniform(0.8, 1.2)

        faturamento = (base_sales + trend) * weekday_multiplier * noise

        data.append(
            {
                "id_transacao": f"TX{1000 + i}",
                "dia_registro": date.strftime("%Y-%m-%d"),
                "faturamento_bruto": round(faturamento, 2),
                "metodo_pagamento": np.random.choice(["pix", "cartao", "dinheiro"]),
                "vendedor": np.random.choice(["Andrey", "Porto", "Brumatti"]),
                "unidade_estoque": np.random.randint(5, 50),
            }
        )

    df = pd.DataFrame(data)

    df.to_csv("vendas_mock_12_meses.csv", index=False)
    df.to_excel("vendas_mock_12_meses.xlsx", index=False)


if __name__ == "__main__":
    generate_nexly_data()
