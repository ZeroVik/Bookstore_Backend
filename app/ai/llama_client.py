import os, httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()
OLLAMA = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
MODEL = os.getenv("LLAMA_MODEL", "llama3:latest")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
async def llama_chat(prompt: str) -> str:
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{OLLAMA}/api/generate", json=payload)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "").strip()
