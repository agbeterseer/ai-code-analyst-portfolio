from sqlalchemy.orm import Session
from app.models.prompt_log import PromptLog

def save_prompt_log(db: Session, prompt: str, response: str, scores: dict):
    log = PromptLog(prompt=prompt, response=response, scores=scores)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
