from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project


class ProjectRepository:
    async def create(
        self,
        session: AsyncSession,
        user_id: int,
        title: str,
        prompt: str,
        tech_stack: str,
    ) -> Project:
        p = Project(
            user_id=user_id,
            title=title,
            prompt=prompt,
            tech_stack=tech_stack,
            status="draft",
        )
        session.add(p)
        await session.commit()
        await session.refresh(p)
        return p

    async def list_by_user(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[Project]:
        res = await session.execute(
            select(Project)
            .where(Project.user_id == user_id)
            .order_by(Project.id.desc())
        )
        return list(res.scalars().all())

    async def get(
        self,
        session: AsyncSession,
        project_id: int,
        user_id: int,
    ) -> Project | None:
        res = await session.execute(
            select(Project).where(
                Project.id == project_id,
                Project.user_id == user_id,
            )
        )
        return res.scalar_one_or_none()
