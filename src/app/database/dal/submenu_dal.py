from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Submenu


class SubmenuDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_submenu(self, title: str, description: str, menu_id: str):
        submenu = Submenu(title=title, description=description, menu_id=menu_id)
        self.db_session.add(submenu)
        await self.db_session.flush()
        return submenu

    async def get_submenu(self, submenu_id: str):
        query = select(Submenu).where(Submenu.id == submenu_id)
        res = await self.db_session.execute(query)
        group_row = res.fetchone()
        if group_row is not None:
            return group_row[0]

    async def get_all_submenus(self):
        return await self.db_session.execute(select(Submenu)).scalars().all()

    async def get_submenu_by_menu_id(self, menu_id: str):
        query = select(Submenu).where(Submenu.menu_id == menu_id)
        res = await self.db_session.execute(query).scalars().all()
        return res

    async def update_submenu(self, title: str, description: str, submenu_id: str):
        submenu = await self.get_submenu(submenu_id)
        if submenu:
            submenu.title = title
            submenu.description = description
            await self.db_session.flush()
        return submenu

    async def delete_submenu(self, submenu_id: str):
        submenu = await self.get_submenu(submenu_id)
        if submenu:
            await self.db_session.delete(submenu)
            await self.db_session.commit()
        return submenu

    async def delete_submenu_by_obj(self, submenu: Submenu):
        if submenu:
            await self.db_session.delete(submenu)
            await self.db_session.commit()
        return submenu
