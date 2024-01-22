from sqlalchemy.orm import Session

from app.database.dal.submenu_dal import SubmenuDAO
from app.database.models import Submenu
from app.database.service.dish_service import DishService


class SubmenuService:
    def __init__(self, db_session: Session):
        self.submenu_dao = SubmenuDAO(db_session)
        self.dish_service = DishService(db_session)
        self.MAX_SUBMENUS_AMOUNT = 2

    def create(self, title: str, description: str, menu_id: str):
        submenus = self.submenu_dao.get_submenu_by_menu_id(menu_id)

        if len(submenus) > self.MAX_SUBMENUS_AMOUNT:
            raise ValueError("Number of submenus exceeds the maximum allowed "
                             f"{self.MAX_SUBMENUS_AMOUNT}.")
        else:
            return self.submenu_dao.create_submenu(title, description, menu_id)

    def read(self, submenu_id: str):
        return self.submenu_dao.get_submenu(submenu_id)

    def read_all(self):
        return self.submenu_dao.get_all_submenus()

    def read_by_menu_id(self, menu_id: str):
        return self.submenu_dao.get_submenu_by_menu_id(menu_id)

    def update(self, title: str, description: str, submenu_id: str):
        return self.submenu_dao.update_submenu(title, description, submenu_id)

    def delete(self, submenu: Submenu):
        for dish in submenu.dishes:
            self.dish_service.delete(dish)

        return self.submenu_dao.delete_submenu_by_obj(submenu)
