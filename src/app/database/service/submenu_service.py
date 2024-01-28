from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dal.submenu_dal import SubmenuDAO
from app.database.models import Submenu
from app.database.service.dish_service import DishService


class SubmenuService:
    def __init__(self, db_session: AsyncSession):
        self.submenu_dao = SubmenuDAO(db_session)
        self.dish_service = DishService(db_session)
        self.MAX_SUBMENUS_AMOUNT = 2

    async def create(self, title: str, description: str, menu_id: str):
        submenus = await self.submenu_dao.get_submenu_by_menu_id(menu_id)

        if len(submenus) > self.MAX_SUBMENUS_AMOUNT:
            raise ValueError("Number of submenus exceeds the maximum allowed "
                             f"{self.MAX_SUBMENUS_AMOUNT}.")
        else:
            return await self.submenu_dao.create_submenu(title, description, menu_id)

    async def read(self, submenu_id: str):
        return await self.submenu_dao.get_submenu(submenu_id)

    async def read_all(self):
        return await self.submenu_dao.get_all_submenus()

    async def read_by_menu_id(self, menu_id: str):
        return await self.submenu_dao.get_submenu_by_menu_id(menu_id)

    async def read_obj(self, submenu_id: str):
        return await self.submenu_dao.get_submenu_obj(submenu_id)

    async def read_submenu_ids_by_menu_id(self, menu_id: str):
        return await self.submenu_dao.get_submenu_ids_by_menu_id(menu_id)

    async def update(self, title: str, description: str, submenu_id: str):
        return await self.submenu_dao.update_submenu(title, description, submenu_id)

    async def delete(self, submenu_id: str):
        dishes = await self.dish_service.read_by_submenu_id(submenu_id)
        for dish in dishes:
            await self.dish_service.delete(dish.id)
        return await self.submenu_dao.delete_submenu(submenu_id)
