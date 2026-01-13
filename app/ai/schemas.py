from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum


class SectionType(str, Enum):
    HERO = "hero"
    ABOUT = "about"
    PROJECTS = "projects"
    CONTACT = "contact"
    SERVICES = "services"
    TESTIMONIALS = "testimonials"
    BLOG = "blog"


class WebsiteSection(BaseModel):
    """Схема для секции сайта"""

    type: SectionType
    title: str
    description: Optional[str] = None
    content: Optional[List[Dict[str, Any]]] = None
    order: int


class WebsiteStructure(BaseModel):
    """Структура сайта, генерируемая AI"""

    name: str
    description: str
    sections: List[WebsiteSection]
    features: List[str]
    target_audience: str


class ColorScheme(BaseModel):
    """Цветовая схема"""

    primary: str = Field(..., description="Основной цвет (#HEX)")
    secondary: str = Field(..., description="Вторичный цвет (#HEX)")
    accent: str = Field(..., description="Акцентный цвет (#HEX)")
    background: str = Field(..., description="Фоновый цвет (#HEX)")
    text: str = Field(..., description="Цвет текста (#HEX)")


class GeneratedFrontend(BaseModel):
    """Сгенерированный фронтенд"""

    html: str
    css: str
    javascript: str
    structure: WebsiteStructure


class GeneratedBackend(BaseModel):
    """Сгенерированный бэкенд"""

    main_py: str
    requirements_txt: str
    endpoints: List[Dict[str, Any]]
