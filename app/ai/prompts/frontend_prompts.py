from typing import Dict
from app.ai.schemas import WebsiteStructure


class FrontendPrompts:
    """Шаблоны промптов для генерации фронтенда"""

    @staticmethod
    def get_structure_prompt(user_prompt: str) -> str:
        return f"""Проанализируй запрос пользователя и создай структуру веб-сайта.

Запрос пользователя: "{user_prompt}"

Создай подробную структуру сайта включая:
1. Название сайта
2. Описание (1-2 предложения)
3. Список секций в правильном порядке
4. Ключевые особенности
5. Целевую аудиторию

Для каждой секции укажи:
- Тип секции (hero, about, projects, contact и т.д.)
- Заголовок
- Описание содержания
- Порядок отображения

Секции должны быть логичными и соответствовать запросу пользователя."""

    @staticmethod
    def get_html_prompt(
        structure: WebsiteStructure, color_scheme: Dict[str, str]
    ) -> str:
        sections_html = "\n".join(
            [
                f"""<!-- {section.type.value} Section -->
<section id="{section.type.value}" class="section-{section.type.value}">
    <div class="container">
        <h2>{section.title}</h2>
        <p>{section.description or 'Описание секции'}</p>
    </div>
</section>"""
                for section in structure.sections
            ]
        )

        return f"""Сгенерируй HTML код для сайта со следующей структурой:

Название: {structure.name}
Описание: {structure.description}
Цветовая схема: {color_scheme}

Секции:
{sections_html}

Требования:
1. Используй семантические HTML5 теги
2. Добавь мета-теги для SEO
3. Сделай адаптивную верстку
4. Добавь комментарии к ключевым блокам
5. Используй современные подходы (CSS Grid/Flexbox)
6. Включи Font Awesome для иконок
7. Создай навигационное меню с якорными ссылками на секции

Верни ТОЛЬКО HTML код без пояснений."""

    @staticmethod
    def get_css_prompt(
        structure: WebsiteStructure, color_scheme: Dict[str, str]
    ) -> str:
        return f"""Создай CSS код для сайта со следующей структурой:

Название: {structure.name}
Цветовая схема:
- Основной: {color_scheme.get('primary', '#3a86ff')}
- Вторичный: {color_scheme.get('secondary', '#8338ec')}
- Фон: {color_scheme.get('background', '#0d1b2a')}
- Текст: {color_scheme.get('text', '#e0e1dd')}

Секции: {[s.type.value for s in structure.sections]}

Требования:
1. Используй CSS variables для цветов
2. Сделай темную тему по умолчанию
3. Добавь плавные анимации для hover эффектов
4. Создай адаптивные breakpoints для mobile/tablet/desktop
5. Используй modern CSS (Grid, Flexbox)
6. Добавь стили для навигации, кнопок, форм
7. Включи reset/normalize стили

Верни ТОЛЬКО CSS код без пояснений."""
