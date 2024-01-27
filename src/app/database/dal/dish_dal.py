from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Dish


class DishDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_dish(self, title: str, description: str, price: str, submenu_id: str):
        dish = Dish(title=title, description=description, price=price, submenu_id=submenu_id)
        self.db_session.add(dish)
        await self.db_session.flush()
        return dish

    async def get_dish(self, dish_id: str):
        query = select(Dish).where(Dish.id == dish_id)
        res = await self.db_session.execute(query)
        group_row = res.fetchone()
        if group_row is not None:
            return group_row[0]

    async def get_all_dishes(self):
        return await self.db_session.execute(select(Dish)).scalars().all()

    async def get_dishes_by_submenu_id(self, submenu_id: str):
        query = select(Dish).where(Dish.submenu_id == submenu_id)
        res = await self.db_session.execute(query).scalars().all()
        return res

    async def update_dish(self, title: str, description: str, price: str, dish_id: str):
        dish = await self.get_dish(dish_id)
        if dish:
            dish.title = title
            dish.description = description
            dish.price = price
            await self.db_session.flush()
        return dish

    async def delete_dish(self, dish_id: str):
        dish = await self.get_dish(dish_id)
        if dish:
            await self.db_session.delete(dish)
            await self.db_session.flush()
        return dish

    async def delete_dish_by_obj(self, dish: Dish):
        if dish:
            await self.db_session.delete(dish)
            await self.db_session.flush()
        return dish
