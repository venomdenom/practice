from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import crud_user
from app.schemas.user import UserCreate
from app.core.config import settings
from app.db.session import AsyncSessionLocal


async def create_first_superuser() -> None:
    async with AsyncSessionLocal() as session:
        user = await crud_user.get_by_email(
            session=session, email=settings.FIRST_SUPERUSER
        )
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                first_name="Initial",
                last_name="Admin",
                phone="+1234567890"
            )
            await crud_user.create(session=session, obj_in=user_in)
            print(f"Суперпользователь {settings.FIRST_SUPERUSER} создан")
