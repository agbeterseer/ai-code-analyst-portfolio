from pydantic import BaseModel
from typing import Dict, Any, Optional
from sqlalchemy import Column, Integer, Float, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ValidationRequest(BaseModel):
    prompt: str
    response: Dict[str, Any]  # ✅ Accept a JSON object, not a string
    expected_schema: Optional[Dict[str, Any]] = None

class ValidationResult(BaseModel):
    hallucination_score: float
    toxicity_score: float
    schema_score: float

class ToxicityRequest(BaseModel):
    text: str

class SchemaRequest(BaseModel):
    schema: Dict[str, Any]

class JsonRequest(BaseModel):
    json_data: Dict[str, Any]
    schema: Dict[str, Any]

class ValidationLog(Base):
    __tablename__ = "validation_logs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text)
    response = Column(Text)
    hallucination_score = Column(Float)
    toxicity_score = Column(Float)
    schema_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class PromptLog(Base):
    __tablename__ = "prompt_logs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    response = Column(String)
    scores = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
