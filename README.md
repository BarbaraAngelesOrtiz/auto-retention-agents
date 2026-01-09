# AutoRetention Agents

FastAPI app para simular decisiones de retención de clientes usando un churn score.

## Requisitos
- Python 3.12+
- Pandas
- FastAPI
- Uvicorn

## Cómo usar
1. Crear y activar venv
2. Instalar dependencias: `pip install -r requirements.txt`
3. Levantar server: `python -m uvicorn app:app --reload`
4. Acceder a endpoints:
   - `/` para status
   - `/customer_ids` para primeros IDs
   - `/simulate_decision/<customer_id>` para simular churn
5. Ver Swagger en `/docs`

FastAPI

Dataset real

Simulación de churn

Agentes

Telegram real

Microsoft Graph real

Feature flags

Fallbacks


* Próximo salto:

Agregar Teams meeting link

Agente de auditoría / logging

Orquestador multi-agente

Scheduler automático
