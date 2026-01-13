from typing import Dict, Any, Optional
from uuid import UUID
import logging
from app.ai.agents.frontend_agent import FrontendAgent
from app.ai.schemas import GeneratedFrontend
from app.db.session import SessionLocal
from app.models.project import Project, ProjectStatus
from app.models.job import Job, JobType, JobStatus
from datetime import datetime

logger = logging.getLogger(__name__)


class GenerationService:
    """Сервис для управления процессом генерации"""

    def __init__(self):
        self.frontend_agent = FrontendAgent()

    async def start_generation(
        self, user_prompt: str, project_name: str, user_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Запуск процесса генерации сайта

        Returns:
            Dict с project_id и initial status
        """
        db = SessionLocal()
        try:
            # 1. Создаем проект
            project = Project(
                name=project_name,
                description="Автоматически сгенерированный сайт",
                prompt=user_prompt,
                user_id=user_id,
                status=ProjectStatus.GENERATING,
            )
            db.add(project)
            db.flush()  # Получаем ID

            # 2. Создаем задание для фронтенда
            frontend_job = Job(
                project_id=project.id,
                job_type=JobType.FRONTEND_GENERATION,
                status=JobStatus.PENDING,
                input_data={"user_prompt": user_prompt},
            )
            db.add(frontend_job)

            db.commit()

            logger.info(
                f"Created project {project.id} with frontend job {frontend_job.id}"
            )

            # 3. Запускаем асинхронную генерацию
            # В реальном приложении тут будет вызов Celery/Background task
            # Для простоты делаем синхронно в этом примере

            return {
                "project_id": str(project.id),
                "status": "generating",
                "message": "Генерация начата",
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to start generation: {e}")
            raise
        finally:
            db.close()

    async def generate_frontend(self, project_id: UUID) -> GeneratedFrontend:
        """Генерация фронтенд части"""
        db = SessionLocal()
        try:
            # Получаем проект
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise ValueError(f"Project {project_id} not found")

            # Находим соответствующее задание
            job = (
                db.query(Job)
                .filter(
                    Job.project_id == project_id,
                    Job.job_type == JobType.FRONTEND_GENERATION,
                )
                .first()
            )

            if job:
                job.status = JobStatus.RUNNING
                job.started_at = datetime.utcnow()
                db.commit()

            # Генерация фронтенда
            result = await self.frontend_agent.generate(
                {"user_prompt": project.prompt, "color_scheme": project.color_scheme}
            )

            # Обновляем проект
            project.generated_html = result["html"]
            project.generated_css = result["css"]
            project.generated_js = result["javascript"]
            project.generated_structure = result["structure"]
            project.status = ProjectStatus.READY
            project.completed_at = datetime.utcnow()

            # Обновляем задание
            if job:
                job.status = JobStatus.COMPLETED
                job.completed_at = datetime.utcnow()
                job.output_data = {"success": True}
                job.tokens_used = 1000  # В реальности из response

            db.commit()

            return GeneratedFrontend(**result)

        except Exception as e:
            # Обновляем статус при ошибке
            if "project" in locals() and project:
                project.status = ProjectStatus.FAILED

            if "job" in locals() and job:
                job.status = JobStatus.FAILED
                job.error_message = str(e)

            db.commit()
            logger.error(f"Failed to generate frontend: {e}")
            raise
        finally:
            db.close()
