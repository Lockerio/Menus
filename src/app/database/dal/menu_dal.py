from sqlalchemy import select, func, distinct, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Menu, Submenu, Dish


class MenuDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_menu(self, title: str, description: str):
        menu = Menu(title=title, description=description)
        self.db_session.add(menu)
        await self.db_session.flush()
        return menu

    async def get_menu_obj(self, menu_id: str):
        query = select(Menu).where(Menu.id == menu_id)
        res = await self.db_session.execute(query)
        return res.scalars().first()

    async def get_menu(self, menu_id: str):
        query = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label("submenus_count"),
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(
                Submenu,
                Menu.id == Submenu.menu_id,
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Menu.id == menu_id)
            .group_by(Menu.id)
        )
        menu = await self.db_session.execute(query)
        return menu.first()

    async def get_all_menus(self):
        res = await self.db_session.execute(select(Menu))
        return res.scalars().all()

    async def update_menu(self, menu_id: str, title: str, description: str):
        menu = await self.get_menu_obj(menu_id)
        if menu:
            menu.title = title
            menu.description = description
            await self.db_session.flush()
        return menu

    async def delete_menu(self, menu_id: str):
        query = delete(Menu).where(Menu.id == menu_id)
        await self.db_session.execute(query)
