from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dal.dish_dal import DishDAO
from app.database.models import Dish


class DishService:
    def __init__(self, db_session: AsyncSession):
        self.dish_dao = DishDAO(db_session)
        self.MAX_DISHES_AMOUNT = 2

    async def create(self, title: str, description: str, price: str, submenu_id: str):
        dishes = await self.dish_dao.get_dishes_by_submenu_id(submenu_id)

        if len(dishes) > self.MAX_DISHES_AMOUNT:
            raise ValueError("Number of dishes exceeds the maximum allowed "
                             f"{self.MAX_DISHES_AMOUNT}.")
        else:
            return await self.dish_dao.create_dish(title, description, price, submenu_id)

    async def read(self, dish_id: str):
        return await self.dish_dao.get_dish(dish_id)

    async def read_all(self):
        return await self.dish_dao.get_all_dishes()

    async def read_by_submenu_id(self, submenu_id: str):
        return await self.dish_dao.get_dishes_by_submenu_id(submenu_id)

    async def update(self, title: str, description: str, price: str, dish_id: str):
        return await self.dish_dao.update_dish(title, description, price, dish_id)

    async def delete(self, dish_id: str):
        return await self.dish_dao.delete_dish(dish_id)
