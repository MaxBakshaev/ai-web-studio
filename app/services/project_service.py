from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.project_repo import ProjectRepository
from app.models import Project


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def create(
        self,
        session: AsyncSession,
        user_id: int,
        title: str,
        prompt: str,
        tech_stack: str,
    ) -> Project:
        return await self.repo.create(
            session,
            user_id=user_id,
            title=title,
            prompt=prompt,
            tech_stack=tech_stack,
        )

    async def list_my(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[Project]:
        return await self.repo.list_by_user(
            session,
            user_id=user_id,
        )

    async def get_my(
        self,
        session: AsyncSession,
        user_id: int,
        project_id: int,
    ) -> Project | None:
        return await self.repo.get(
            session,
            project_id=project_id,
            user_id=user_id,
        )
