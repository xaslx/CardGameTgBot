from src.repositories.sqlalchemy import SQLAlchemyRepository
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy import select, desc


logger = logging.getLogger(__name__)


class UserRepository(SQLAlchemyRepository):

    model: User = User



    @classmethod
    async def find_best_rating(cls, session: AsyncSession, **filter_by):
        try:
            stmt = select(cls.model).filter_by(**filter_by).order_by(desc(cls.model.rating))
            res = await session.execute(stmt)
            return res.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при поиске всех значений в базе данных', extra={'ошибка': e})
            return None