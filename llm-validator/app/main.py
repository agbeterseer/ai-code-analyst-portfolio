from fastapi import FastAPI
from app.routes import router
from app.db import Base, engine
from app.models import prompt_log


app = FastAPI(title="LLM Output Validator API")
app.include_router(router)
Base.metadata.create_all(bind=engine)