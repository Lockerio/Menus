from sqlalchemy.orm import Session

from app.database.models import Submenu


class SubmenuDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_submenu(self, title: str, description: str, menu_id: str):
        submenu = Submenu(title=title, description=description, menu_id=menu_id)
        self.db_session.add(submenu)
        self.db_session.commit()
        self.db_session.refresh(submenu)
        return submenu

    def get_submenu(self, submenu_id: str):
        return self.db_session.query(Submenu).filter(Submenu.id == submenu_id).first()

    def get_all_submenus(self):
        return self.db_session.query(Submenu).all()

    def get_submenu_by_menu_id(self, menu_id: str):
        return self.db_session.query(Submenu).filter(Submenu.menu_id == menu_id).all()

    def update_submenu(self, title: str, description: str, menu_id: str):
        submenu = self.get_submenu(menu_id)
        if submenu:
            submenu.title = title
            submenu.description = description
            self.db_session.commit()
            self.db_session.refresh(submenu)
        return submenu

    def delete_submenu(self, submenu_id: str):
        submenu = self.get_submenu(submenu_id)
        if submenu:
            self.db_session.delete(submenu)
            self.db_session.commit()
        return submenu
