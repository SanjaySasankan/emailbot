# SASBot FastAPI Server

Install dependencies:

```
pip install -r requirements.txt
```

Run (PowerShell):

```powershell
python main.py
```

Or run with uvicorn directly:

```powershell
uvicorn app:app --reload
```

Health check:

```
GET http://127.0.0.1:8000/health
```
