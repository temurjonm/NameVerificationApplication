import os
from openai import AsyncOpenAI
from app.store.memory import NameStore


class NameGenerator:
    """Generates target names from prompts using LLM."""
    
    def __init__(self, store: NameStore, api_key: str = None):
        self._store = store
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key required")
        self._client = AsyncOpenAI(api_key=api_key)
    
    async def generate(self, prompt: str) -> str:
        """Generate a name from prompt and store it."""
        try:
            response = await self._client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Generate a single name based on the user's prompt. Return only the name, nothing else."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=50,
                temperature=0.7,
                timeout=10.0
            )
            
            name = response.choices[0].message.content.strip()
            self._store.set_target(name)
            return name
            
        except Exception as e:
            raise RuntimeError(f"Name generation failed: {str(e)}")
