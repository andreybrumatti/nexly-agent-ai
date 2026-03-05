import io

import google.generativeai as genai
import pandas as pd
from fastapi import FastAPI, File, Form, UploadFile
from prophet import Prophet

app = FastAPI()
genai.configure(api_key="")
model_gemini = genai.GenerativeModel("gemini-2.0-flash-lite")


@app.post("/predict")
async def predict(
    file: UploadFile = File(...), col_date: str = Form(...), col_amount: str = Form(...)
):
    content = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
    else:
        df = pd.read_excel(io.BytesIO(content))

    try:
        df_prophet = df[[col_date, col_amount]].copy()
        df_prophet.columns = ["ds", "y"]
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])
    except KeyError:
        return {
            "error": "Colunas não encontradas",
            "recebido": {"data": col_date, "valor": col_amount},
            "disponivel": df.columns.tolist(),
        }

    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    resumo = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(7)
    resumo["ds"] = resumo["ds"].dt.strftime("%Y-%m-%d")
    dados_resumo = resumo.to_dict(orient="records")

    prompt = f"""
    Como um consultor de negócios especialista em análise de dados, analise as seguintes previsões de vendas para a próxima semana:
    {dados_resumo}
    
    Escreva um parágrafo curto e humanizado para o dono da empresa, destacando:
    1. Qual será o melhor dia de vendas.
    2. Uma dica prática baseada na tendência (ex: estoque ou equipe).
    Seja direto e não use emojis.
    """

    response_gemini = model_gemini.generate_content(prompt)

    return {
        "status": "success",
        "previsoes": dados_resumo,
        "insight_ia": response_gemini.text,
    }
