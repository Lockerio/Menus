from sqlalchemy.orm import Session

from app.database.dal.submenu_dal import SubmenuDAO


class SubmenuService:
    def __init__(self, db_session: Session):
        self.submenu_dao = SubmenuDAO(db_session)
        self.MAX_SUBMENUS_AMOUNT = 2

    def create(self, title: str, description: str, menu_id: str):
        submenus = self.submenu_dao.get_submenu_by_menu_id(menu_id)

        if len(submenus) > self.MAX_SUBMENUS_AMOUNT:
            raise ValueError("Number of submenus exceeds the maximum allowed "
                             f"{self.MAX_SUBMENUS_AMOUNT}.")
        else:
            self.submenu_dao.create_submenu(title, description, menu_id)

    def read(self, submenu_id: str):
        self.submenu_dao.get_submenu(submenu_id)

    def update(self):
        pass

    def delete(self):
        pass