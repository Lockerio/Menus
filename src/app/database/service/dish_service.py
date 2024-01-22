from sqlalchemy.orm import Session

from app.database.dal.dish_dal import DishDAO
from app.database.models import Dish


class DishService:
    def __init__(self, db_session: Session):
        self.dish_dao = DishDAO(db_session)
        self.MAX_DISHES_AMOUNT = 2

    def create(self, title: str, description: str, price: str, submenu_id: str):
        dishes = self.dish_dao.get_dishes_by_submenu_id(submenu_id)

        if len(dishes) > self.MAX_DISHES_AMOUNT:
            raise ValueError("Number of dishes exceeds the maximum allowed "
                             f"{self.MAX_DISHES_AMOUNT}.")
        else:
            return self.dish_dao.create_dish(title, description, price, submenu_id)

    def read(self, dish_id: str):
        return self.dish_dao.get_dish(dish_id)

    def read_all(self):
        return self.dish_dao.get_all_dishes()

    def read_by_submenu_id(self, submenu_id: str):
        return self.dish_dao.get_dishes_by_submenu_id(submenu_id)

    def update(self, title: str, description: str, price: str, dish_id: str):
        return self.dish_dao.update_dish(title, description, price, dish_id)

    def delete(self, dish: Dish):
        return self.dish_dao.delete_dish_by_obj(dish)
