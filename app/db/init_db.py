from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user_crud
from app.schemas.user import UserCreate
from app.core.config import settings
from app.db.session import AsyncSessionLocal


async def create_first_superuser() -> None:
    async with AsyncSessionLocal() as session:
        user = await user_crud.get_by_email(
            session=session, email=settings.FIRST_SUPERUSER
        )
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                full_name="Initial Admin",
                phone="+1234567890"
            )
            await user_crud.create(session=session, obj_in=user_in)
            print(f"Суперпользователь {settings.FIRST_SUPERUSER} создан")
