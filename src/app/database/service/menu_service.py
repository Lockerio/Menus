from sqlalchemy.orm import Session

from app.database.dal.menu_dal import MenuDAO
from app.database.service.submenu_service import SubmenuService


class MenuService:
    def __init__(self, db_session: Session):
        self.menu_dao = MenuDAO(db_session)
        self.submenu_service = SubmenuService(db_session)

    def create(self, title: str, description: str):
        return self.menu_dao.create_menu(title, description)

    def read(self, menu_id: str):
        return self.menu_dao.get_menu(menu_id)

    def read_all(self):
        return self.menu_dao.get_all_menus()

    def update(self, title: str, description: str, menu_id: str):
        return self.menu_dao.update_menu(menu_id, title, description)

    def delete(self, menu_id: str):
        menu = self.menu_dao.get_menu(menu_id)

        for submenu in menu.submenus:
            self.submenu_service.delete(submenu.id)

        return self.menu_dao.delete_menu_by_obj(menu)
