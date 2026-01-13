import os
import json
import aiohttp
from typing import Dict, Any, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class DeepSeekClient:
    """Клиент для работы с DeepSeek API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False,
    ) -> Dict[str, Any]:
        """
        Генерация текста через DeepSeek API
        """
        if not self.api_key:
            raise ValueError("DeepSeek API key not configured")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": "deepseek-coder-33b-instruct",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=60,
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "content": data["choices"][0]["message"]["content"],
                            "tokens_used": data.get("usage", {}),
                            "model": data["model"],
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API error: {error_text}")
                        raise Exception(f"API error: {response.status}")

        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
            raise

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Генерация структурированного JSON ответа
        """
        schema_str = json.dumps(response_schema, indent=2)
        enhanced_prompt = f"""{prompt}

Ты должен вернуть ответ в строгом JSON формате согласно этой схеме:
{schema_str}

Верни ТОЛЬКО JSON без каких-либо пояснений, кода бэктиков или markdown."""

        result = await self.generate_completion(
            prompt=enhanced_prompt, system_prompt=system_prompt, json_mode=True
        )

        try:
            return json.loads(result["content"])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from AI response: {e}")
            # Попробуем извлечь JSON из текста
            import re

            json_match = re.search(r"\{.*\}", result["content"], re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise
