from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.database.db import get_db
from app.database.service.menu_service import MenuService
from app.menu.schemas import MenuCreateUpdate


menu_router = APIRouter(prefix="/api/v1")


@menu_router.post("/menus/")
async def create_menu(
        menu_data: MenuCreateUpdate,
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        menu_service = MenuService(db)
        menu = await menu_service.create(menu_data.title, menu_data.description)

    return JSONResponse({
        "id": str(menu.id),
        "title": menu.title,
        "description": menu.description
    }, status_code=201)


@menu_router.get("/menus/")
async def read_menus(
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        menu_service = MenuService(db)
        menus = await menu_service.read_all()

    response = [{
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description
        }
        for menu in menus
    ]

    return JSONResponse(response)


@menu_router.get("/menus/{target_menu_id}/")
async def read_menu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        menu_service = MenuService(db)
        try:
            menu = await menu_service.read(target_menu_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    if menu:
        return JSONResponse({
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": menu.submenus_count,
            "dishes_count": menu.dishes_count
        })

    raise HTTPException(status_code=404, detail="menu not found")


@menu_router.patch("/menus/{target_menu_id}/")
async def update_menu(
        menu_data: MenuCreateUpdate,
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        menu_service = MenuService(db)
        try:
            menu = await menu_service.update(menu_data.title, menu_data.description, target_menu_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    if menu:
        return JSONResponse({
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description
        })

    raise HTTPException(status_code=404, detail="menu not found")


@menu_router.delete("/menus/{target_menu_id}/")
async def delete_menu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        menu_service = MenuService(db)

        try:
            await menu_service.delete(target_menu_id)
        except AttributeError:
            raise HTTPException(status_code=500, detail="Something went wrong")

    return JSONResponse(None)
