from sqlalchemy.orm import Session

from app.database.models import Dish


class DishDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_dish(self, title: str, description: str, price: str, submenu_id: str):
        dish = Dish(title=title, description=description, price=price, submenu_id=submenu_id)
        self.db_session.add(dish)
        self.db_session.commit()
        self.db_session.refresh(dish)
        return dish

    def get_dish(self, dish_id: str):
        return self.db_session.query(Dish).filter(Dish.id == dish_id).first()

    def get_all_dishes(self):
        return self.db_session.query(Dish).all()

    def get_dishes_by_submenu_id(self, submenu_id: str):
        return self.db_session.query(Dish).filter(Dish.submenu_id == submenu_id).all()

    def update_dish(self, dish_id: str, title: str, description: str, price: str):
        dish = self.get_dish(dish_id)
        if dish:
            dish.title = title
            dish.description = description
            dish.price = price
            self.db_session.commit()
            self.db_session.refresh(dish)
        return dish

    def delete_dish(self, dish_id: str):
        dish = self.get_dish(dish_id)
        if dish:
            self.db_session.delete(dish)
            self.db_session.commit()
        return dish

    def delete_dish_by_obj(self, dish: Dish):
        if dish:
            self.db_session.delete(dish)
            self.db_session.commit()
        return dish
