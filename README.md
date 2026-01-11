# AutoRetention Agents

Sistema multi-agente para retención automática de clientes basado en churn prediction, con integración real a herramientas de negocio (Calendar, Email, Chat, Sheets) y ejecución vía API.

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


✅ uso real de Google APIs
✅ automatización de decisiones
✅ generación de canales de comunicación
✅ arquitectura multi-agente
✅ FastAPI + batch + real-world integrations

Para churn alto:

📅 Evento en Google Calendar + 🎥 Google Meet generado + correo de auditoria + 📊 Registro de la acción en Google Sheets

✉️ Email automático con el link



Todo disparado desde un solo execute_action().

✅ Test por tipo de acción

Solo email

Email + Meet

Telegram

No action

✅ Test FastAPI
POST /run-batch

✅ Test con scheduler

Simular corrida diaria

✅ Test con error controlado

Token vencido

Sheet inexistente

Telegram caído