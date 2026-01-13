from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.ai.client import DeepSeekClient
import logging

logger = logging.getLogger(__name__)


class BaseAIAgent(ABC):
    """Базовый класс для всех AI агентов"""

    def __init__(self, client: Optional[DeepSeekClient] = None):
        self.client = client or DeepSeekClient()
        self.agent_name = self.__class__.__name__

    @abstractmethod
    async def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Основной метод генерации"""
        pass

    async def _call_ai(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Обертка для вызова AI с логированием"""
        logger.info(f"[{self.agent_name}] Calling AI with prompt length: {len(prompt)}")

        try:
            if json_schema:
                result = await self.client.generate_structured(
                    prompt=prompt,
                    response_schema=json_schema,
                    system_prompt=system_prompt,
                )
            else:
                result = await self.client.generate_completion(
                    prompt=prompt, system_prompt=system_prompt
                )

            logger.info(f"[{self.agent_name}] AI call successful")
            return result

        except Exception as e:
            logger.error(f"[{self.agent_name}] AI call failed: {e}")
            raise
