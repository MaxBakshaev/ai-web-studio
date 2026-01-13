from app.ai.agents.base_agent import BaseAIAgent
from app.ai.prompts.frontend_prompts import FrontendPrompts
from app.ai.schemas import WebsiteStructure, GeneratedFrontend, ColorScheme
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class FrontendAgent(BaseAIAgent):
    """Агент для генерации фронтенд кода"""

    async def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация фронтенд кода на основе промпта пользователя

        Args:
            input_data: {
                "user_prompt": str,
                "color_scheme": dict (опционально)
            }

        Returns:
            GeneratedFrontend
        """
        logger.info(
            f"[FrontendAgent] Starting generation for prompt: {input_data['user_prompt'][:100]}..."
        )

        # 1. Генерация структуры сайта
        structure = await self._generate_structure(input_data["user_prompt"])

        # 2. Определение цветовой схемы
        color_scheme = await self._generate_color_scheme(
            input_data.get("color_scheme"), structure
        )

        # 3. Генерация HTML
        html = await self._generate_html(structure, color_scheme)

        # 4. Генерация CSS
        css = await self._generate_css(structure, color_scheme)

        # 5. Генерация JavaScript
        js = await self._generate_javascript(structure)

        result = GeneratedFrontend(
            html=html, css=css, javascript=js, structure=structure
        )

        logger.info(f"[FrontendAgent] Generation completed successfully")
        return result.dict()

    async def _generate_structure(self, user_prompt: str) -> WebsiteStructure:
        """Генерация структуры сайта"""
        prompt = FrontendPrompts.get_structure_prompt(user_prompt)

        result = await self._call_ai(
            prompt=prompt,
            system_prompt="Ты опытный UX/UI дизайнер и веб-разработчик.",
            json_schema=WebsiteStructure.schema(),
        )

        return WebsiteStructure(**result)

    async def _generate_color_scheme(
        self, color_hint: Optional[str], structure: WebsiteStructure
    ) -> Dict[str, str]:
        """Генерация или парсинг цветовой схемы"""
        if color_hint and "тёмная" in color_hint.lower():
            # Стандартная темная схема
            return {
                "primary": "#3a86ff",
                "secondary": "#8338ec",
                "accent": "#ff006e",
                "background": "#0d1b2a",
                "text": "#e0e1dd",
            }

        # Или можно добавить AI для генерации цветовых схем
        return {
            "primary": "#3a86ff",
            "secondary": "#8338ec",
            "accent": "#ff006e",
            "background": "#0d1b2a",
            "text": "#e0e1dd",
        }

    async def _generate_html(
        self, structure: WebsiteStructure, color_scheme: Dict[str, str]
    ) -> str:
        """Генерация HTML кода"""
        prompt = FrontendPrompts.get_html_prompt(structure, color_scheme)

        result = await self._call_ai(
            prompt=prompt,
            system_prompt="Ты опытный фронтенд разработчик. Генерируй чистый, семантический HTML5 код.",
        )

        return result["content"]

    async def _generate_css(
        self, structure: WebsiteStructure, color_scheme: Dict[str, str]
    ) -> str:
        """Генерация CSS кода"""
        prompt = FrontendPrompts.get_css_prompt(structure, color_scheme)

        result = await self._call_ai(
            prompt=prompt,
            system_prompt="Ты опытный CSS разработчик. Генерируй современный, адаптивный CSS код.",
        )

        return result["content"]

    async def _generate_javascript(self, structure: WebsiteStructure) -> str:
        """Генерация JavaScript кода"""
        prompt = f"""Сгенерируй JavaScript код для сайта портфолио.

Сайт имеет следующие секции: {[s.type.value for s in structure.sections]}

Требования:
1. Плавная прокрутка к якорям
2. Анимация появления элементов при скролле
3. Работа с формами (если есть contact форма)
4. Интерактивные элементы портфолио
5. Мобильная навигация (бургер меню)
6. Динамическая подгрузка проектов (если есть projects секция)

Верни ТОЛЬКО JavaScript код без пояснений."""

        result = await self._call_ai(
            prompt=prompt,
            system_prompt="Ты опытный JavaScript разработчик. Пиши чистый, современный JS код.",
        )

        return result["content"]
