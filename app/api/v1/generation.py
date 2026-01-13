from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any
from uuid import UUID
from pydantic import BaseModel
from app.services.generation_service import GenerationService
import logging

router = APIRouter(prefix="/generate", tags=["generation"])
logger = logging.getLogger(__name__)


class GenerateRequest(BaseModel):
    prompt: str
    project_name: str
    color_scheme: str = "тёмная"


@router.post("/start")
async def start_generation(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    service: GenerationService = Depends(),
) -> Dict[str, Any]:
    """
    Запуск генерации сайта по промпту

    Пример запроса:
    {
        "prompt": "Создай сайт-портфолио с секциями: обо мне, проекты, контакты",
        "project_name": "Мое портфолио",
        "color_scheme": "тёмная"
    }
    """
    try:
        result = await service.start_generation(
            user_prompt=request.prompt, project_name=request.project_name
        )

        # В реальном приложении здесь будет вызов фоновой задачи
        # background_tasks.add_task(service.process_generation, result["project_id"])

        return {
            "success": True,
            **result,
            "next_steps": "Используйте /generate/status/{project_id} для отслеживания",
        }
    except Exception as e:
        logger.error(f"Generation start failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{project_id}")
async def get_generation_status(
    project_id: UUID, service: GenerationService = Depends()
) -> Dict[str, Any]:
    """Получение статуса генерации"""
    # Здесь будет логика получения статуса из БД
    # Пока заглушка
    return {
        "project_id": str(project_id),
        "status": "generating",
        "message": "Генерация в процессе",
    }


@router.get("/result/{project_id}")
async def get_generation_result(
    project_id: UUID, service: GenerationService = Depends()
) -> Dict[str, Any]:
    """Получение результатов генерации"""
    try:
        # В реальном приложении тут будет получение из БД
        result = await service.generate_frontend(project_id)

        return {
            "success": True,
            "project_id": str(project_id),
            "html": (
                result.html[:500] + "..." if len(result.html) > 500 else result.html
            ),
            "css": result.css[:500] + "..." if len(result.css) > 500 else result.css,
            "has_javascript": bool(result.javascript),
            "structure": result.structure.dict(),
        }
    except Exception as e:
        logger.error(f"Failed to get result: {e}")
        raise HTTPException(status_code=404, detail="Project not found or not ready")
