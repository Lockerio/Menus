from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Menu


class MenuDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_menu(self, title: str, description: str):
        menu = Menu(title=title, description=description)
        self.db_session.add(menu)
        await self.db_session.flush()
        return menu

    async def get_menu(self, menu_id: str):
        query = select(Menu).where(Menu.id == menu_id)
        res = await self.db_session.execute(query)
        group_row = res.fetchone()
        if group_row is not None:
            return group_row[0]

    async def get_all_menus(self):
        return await self.db_session.execute(select(Menu)).scalars().all()

    async def update_menu(self, menu_id: str, title: str, description: str):
        menu = await self.get_menu(menu_id)
        if menu:
            menu.title = title
            menu.description = description
            await self.db_session.flush()
        return menu

    async def delete_menu(self, menu_id: str):
        menu = await self.get_menu(menu_id)
        if menu:
            await self.db_session.delete(menu)
            await self.db_session.flush()
        return menu

    async def delete_menu_by_obj(self, menu: Menu):
        if menu:
            await self.db_session.delete(menu)
            await self.db_session.flush()
        return menu
