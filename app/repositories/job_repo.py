from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import GenerationJob


class JobRepository:
    async def create(
        self,
        session: AsyncSession,
        project_id: int,
    ) -> GenerationJob:
        job = GenerationJob(project_id=project_id, status="pending")
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job

    async def get(
        self,
        session: AsyncSession,
        job_id: int,
    ) -> GenerationJob | None:
        res = await session.execute(
            select(GenerationJob).where(GenerationJob.id == job_id)
        )
        return res.scalar_one_or_none()

    async def set_status(
        self,
        session: AsyncSession,
        job: GenerationJob,
        status: str,
        error_message: str | None = None,
        n8n_execution_id: str | None = None,
    ) -> GenerationJob:
        job.status = status
        job.error_message = error_message
        if n8n_execution_id:
            job.n8n_execution_id = n8n_execution_id
        await session.commit()
        await session.refresh(job)
        return job
