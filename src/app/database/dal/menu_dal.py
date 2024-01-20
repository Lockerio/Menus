from sqlalchemy.orm import Session

from app.database.models import Menu


class MenuDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_menu(self, title: str, description: str):
        menu = Menu(title=title, description=description)
        self.db_session.add(menu)
        self.db_session.commit()
        self.db_session.refresh(menu)
        return menu

    def get_menu(self, menu_id: str):
        return self.db_session.query(Menu).filter(Menu.id == menu_id).first()

    def get_all_menus(self):
        return self.db_session.query(Menu).all()

    def update_menu(self, menu_id: str, title: str, description: str):
        menu = self.get_menu(menu_id)
        if menu:
            menu.title = title
            menu.description = description
            self.db_session.commit()
            self.db_session.refresh(menu)
        return menu

    def delete_menu(self, menu_id: str):
        menu = self.get_menu(menu_id)
        if menu:
            self.db_session.delete(menu)
            self.db_session.commit()
        return menu
