import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.job_repo import JobRepository
from app.repositories.project_repo import ProjectRepository


class GenerationService:
    def __init__(
        self,
        jobs: JobRepository,
        projects: ProjectRepository,
        n8n_url: str,
        shared_secret: str,
    ):
        self.jobs = jobs
        self.projects = projects
        self.n8n_url = n8n_url
        self.shared_secret = shared_secret

    async def start(
        self,
        session: AsyncSession,
        user_id: int,
        project_id: int,
    ):
        project = await self.projects.get(
            session,
            project_id,
            user_id,
        )
        if not project:
            raise ValueError("Project not found")

        job = await self.jobs.create(
            session,
            project_id=project.id,
        )

        payload = {
            "job_id": job.id,
            "project_id": project.id,
            "user_id": user_id,
            "title": project.title,
            "prompt": project.prompt,
            "tech_stack": project.tech_stack,
        }

        headers = {"X-AIWS-SECRET": self.shared_secret}

        # отправляем в n8n
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                self.n8n_url,
                json=payload,
                headers=headers,
            )

        # если n8n упал — job в failed
        if resp.status_code >= 400:
            await self.jobs.set_status(
                session,
                job,
                "failed",
                error_message=f"n8n error {resp.status_code}: {resp.text[:200]}",
            )
            raise ValueError("Automation service error")

        await self.jobs.set_status(session, job, "running")
        return job
