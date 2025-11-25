AWS Bedrock FastAPI Application

FastAPI application exposing REST endpoints that interact with AWS Bedrock foundation models (Anthropic Claude by default).

Quick links:
- Deployment guide (local and AWS): see DEPLOYMENT.md
- HTTP request samples: test_main.http

Overview

This service lets you:
- Invoke AWS Bedrock models with system and user prompts
- Stream or retrieve responses in JSON

Tech stack
- FastAPI + Uvicorn (Gunicorn in production)
- boto3 (AWS SDK)

Prerequisites
- Python 3.10+ recommended
- AWS account with Bedrock access enabled in your region
- AWS credentials configured (AWS CLI, environment variables, or instance role)

Quickstart (local)
1) Create and activate a virtualenv, then install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2) Ensure AWS credentials are available (for example via `aws configure`). The application uses the default AWS credential/provider chain.

3) Run the API with auto-reload:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4) Open the docs:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

Production run (simple)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

Configuration and environment
- AWS credentials: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` (or use AWS CLI profiles or instance roles)
- Model and region used by the Bedrock client are currently defined in code in `services/ai.py`:
  - Region: `eu-west-2`
  - Model: `anthropic.claude-3-7-sonnet-20250219-v1:0`
  If you need to change these, update `services/ai.py` or extend it to read from environment variables.

API Endpoints (selected)
- `POST /api/bedrock` — Invoke AWS Bedrock models with prompts

Example `POST /api/bedrock` request body:
```json
{
  "model_id": "anthropic.claude-3-7-sonnet-20250219-v1:0",
  "system_prompt": "You are a helpful AI assistant.",
  "user_prompt": "What are the key features of AWS Bedrock?"
}
```

Project structure (top-level)
- `main.py` — FastAPI app and route definitions
- `controllers/` — AI controllers
- `services/` — Bedrock and prompt services
- `models/` — Pydantic models for request/response schemas
- `deploy.sh` — Utility script to copy project files to a remote host via SSH
- `requirements.txt` — Python dependencies
- `test_main.http` — Handy REST client samples
