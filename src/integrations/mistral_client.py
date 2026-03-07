import os

from mistralai import Mistral


class MistralClient:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY") or ""
        self.agent_id = os.getenv("AGENT_ID") or ""
        self.client = Mistral(api_key=self.api_key)

    def get_business_insight(self, data: list, period_name: str, amount: int):
        context_sales = f"""
        [DADOS DE ENTRADA DO NEXLY]
        Tipo de Intervalo: {period_name}
        Quantidade: {amount}
        Valores: {data}

        Instrução Adicional: O usuário quer saber o que fazer com esses números. 
        Lembre-se: Se for 'semanas' ou 'meses', o valor é a SOMA total do período.
        """

        response = self.client.agents.complete(
            agent_id=self.agent_id,
            messages=[{"role": "user", "content": context_sales}],
        )
        return response.choices[0].message.content
