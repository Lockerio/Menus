from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dal.menu_dal import MenuDAO
from app.database.models import Menu
from app.database.service.submenu_service import SubmenuService


class MenuService:
    def __init__(self, db_session: AsyncSession):
        self.menu_dao = MenuDAO(db_session)
        self.submenu_service = SubmenuService(db_session)

    async def create(self, title: str, description: str):
        return await self.menu_dao.create_menu(title, description)

    async def read(self, menu_id: str):
        return await self.menu_dao.get_menu(menu_id)

    async def read_obj(self, menu_id: str):
        return await self.menu_dao.get_menu_obj(menu_id)

    async def read_all(self):
        return await self.menu_dao.get_all_menus()

    async def update(self, title: str, description: str, menu_id: str):
        return await self.menu_dao.update_menu(menu_id, title, description)

    async def delete(self, menu_id: str):
        submenus = await self.submenu_service.read_by_menu_id(menu_id)
        for submenu in submenus:
            await self.submenu_service.delete(submenu.id)
        return await self.menu_dao.delete_menu(menu_id)
