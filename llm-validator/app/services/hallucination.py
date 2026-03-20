import openai
from app.config import ENABLE_HALLUCINATION_CHECK, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def check_hallucination(prompt: str, response: str) -> float:
    if not ENABLE_HALLUCINATION_CHECK:
        return 0.5  # Neutral score if disabled

    try:
        prompt_text = f"""
        Given the following prompt and response, rate the factual accuracy of the response on a scale from 0 to 1.

        Prompt: {prompt}
        Response: {response}

        Return only a number between 0 and 1.
        """

        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt_text}]
        )
        score = float(res["choices"][0]["message"]["content"].strip())
        return round(score, 2)
    except Exception as e:
        print(f"Hallucination check failed: {e}")
        return 0.5  # fallback score
