from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)

    submenus = relationship("Submenu", back_populates="menu")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    menu_id = Column(Integer(), ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    price = Column(String(), nullable=False)
    submenu_id = Column(Integer(), ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")
