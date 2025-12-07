from fastapi import FastAPI
from routers.analytics_router import router as analytics_router
from routers.message_router import router as message_router
from routers.system import router as system_router
from routers.sentiment_router import router as sentiment_router

app = FastAPI(title="Front Analytics Backend")

app.include_router(system_router)
app.include_router(analytics_router)
app.include_router(message_router)
app.include_router(sentiment_router)


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)
