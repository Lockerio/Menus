from sqlalchemy import select, distinct, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Submenu, Dish


class SubmenuDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_submenu(self, title: str, description: str, menu_id: str):
        submenu = Submenu(title=title, description=description, menu_id=menu_id)
        self.db_session.add(submenu)
        await self.db_session.flush()
        return submenu

    async def get_submenu(self, submenu_id: str):
        query = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                Submenu.menu_id,
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Submenu.id == submenu_id)
            .group_by(Submenu.id)
        )

        submenu = await self.db_session.execute(query)
        return submenu.first()

    async def get_submenu_obj(self, submenu_id: str):
        query = select(Submenu).where(Submenu.id == submenu_id)
        res = await self.db_session.execute(query)
        return res.scalars().first()

    async def get_all_submenus(self):
        res = await self.db_session.execute(select(Submenu))
        return res.scalars().all()

    async def get_submenu_by_menu_id(self, menu_id: str):
        query = select(Submenu).where(Submenu.menu_id == menu_id)
        res = await self.db_session.execute(query)
        return res.scalars().all()

    async def get_submenu_ids_by_menu_id(self, menu_id: str):
        query = select(Submenu.id).where(Submenu.menu_id == menu_id)
        res = await self.db_session.execute(query)
        return res.scalars().all()

    async def update_submenu(self, title: str, description: str, submenu_id: str):
        submenu = await self.get_submenu_obj(submenu_id)
        if submenu:
            submenu.title = title
            submenu.description = description
            await self.db_session.flush()
        return submenu

    async def delete_submenu(self, submenu_id: str):
        query = delete(Submenu).where(Submenu.id == submenu_id)
        await self.db_session.execute(query)
