import os
from datetime import datetime

from mistralai import Mistral

from src.core.config import settings


class MistralClient:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY") or ""
        self.agent_id = os.getenv("AGENT_ID") or ""
        self.client = Mistral(api_key=self.api_key)

    def get_business_insight(
        self, data: list, period_name: str, description_business: str, amount: int
    ):
        days_pt = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }

        date_now = datetime.now(settings.TZ_INFO).strftime("%d/%m/%Y")
        day_of_week_en = datetime.now(settings.TZ_INFO).strftime("%A")
        day_of_week_pt = days_pt.get(day_of_week_en, day_of_week_en)

        context_sales = f"""
        [PERFIL DO NEGÓCIO]
        Empresa: {description_business}

        [CONTEXTO TEMPORAL]
        Data de Referência da Análise: {date_now} ({day_of_week_pt})
        Localização: Brasil (Considere feriados e datas comemorativas brasileiras)

        [DADOS DE ENTRADA DO NEXLY]
        Tipo de Intervalo: {period_name}
        Quantidade: {amount}
        Valores: {data}

        [INSTRUÇÕES DE PERSONALIZAÇÃO]
        1. Especialização: Use o 'PERFIL DO NEGÓCIO' para adaptar sua linguagem. Se for um comércio de produtos, fale em 'estoque' e 'giro'. Se for serviço, fale em 'agenda' e 'horas técnicas'.
        2. Vocabulário: Substitua termos genéricos por itens relacionados ao produto/serviço descrito. 
        3. Ações Segmentadas: Sugira estratégias de marketing e vendas que façam sentido especificamente para esse tipo de empresa.

        [DIRETRIZES DE RESPOSTA]
        - O usuário quer saber o que fazer com esses números. 
        - Não retorne nomes de variáveis ou campos técnicos (ex: min_estimate). Use termos como "pior cenário", "margem de segurança" ou "previsão otimista".
        - Lembre-se: Se o intervalo for 'semanas' ou 'meses', os valores são a SOMA TOTAL do período (faturamento acumulado).
        """
        response = self.client.agents.complete(
            agent_id=self.agent_id,
            messages=[{"role": "user", "content": context_sales}],
        )
        return response.choices[0].message.content
