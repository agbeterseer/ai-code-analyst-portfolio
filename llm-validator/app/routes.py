import json
from fastapi import APIRouter
from app.models import ValidationRequest, ValidationResult, ToxicityRequest, SchemaRequest, JsonRequest, ValidationLog
from app.db.database import SessionLocal
from app.services.hallucination import check_hallucination
from app.services.toxicity import check_toxicity
from app.services.schema_check import check_schema, validate_json_schema, validate_json_data

router = APIRouter()

@router.post("/validate", response_model=ValidationResult)
async def validate(req: ValidationRequest):
    # Compute the scores
    hallucination_score = check_hallucination(req.prompt, req.response)
    toxicity_score = check_toxicity(req.response)
    schema_score = check_schema(req.response, req.expected_schema)

    # Save to DB
    async with SessionLocal() as session:
        log = ValidationLog(
            prompt=req.prompt,
            response=req.response,
            hallucination_score=hallucination_score,
            toxicity_score=toxicity_score,
            schema_score=schema_score
        )
        session.add(log)
        await session.commit()

    return ValidationResult(
        hallucination_score=hallucination_score,
        toxicity_score=toxicity_score,
        schema_score=schema_score
    )


@router.post("/validate-toxicity")
def validate_toxicity(req: ToxicityRequest):
    return {"toxicity_score": check_toxicity(req.text)}

@router.post("/validate-schema")
def validate_schema(req: SchemaRequest):
    return {"is_valid": validate_json_schema(req.schema)}

@router.post("/validate-json")
def validate_json(req: JsonRequest):
    return {"is_valid": validate_json_data(req.json_data, req.schema)}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    min_score: Optional[float] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None)
):
    query = db.query(PromptLog)

    if min_score is not None:
        query = query.filter(PromptLog.scores["final_score"].as_float() >= min_score)

    if from_date:
        query = query.filter(PromptLog.created_at >= from_date)

    if to_date:
        query = query.filter(PromptLog.created_at <= to_date)

    logs = query.order_by(desc(PromptLog.created_at)).offset(skip).limit(limit).all()

    return {
        "count": len(logs),
        "results": [
            {
                "id": log.id,
                "prompt": log.prompt,
                "response": log.response,
                "scores": log.scores,
                "created_at": log.created_at
            } for log in logs
        ]
    }