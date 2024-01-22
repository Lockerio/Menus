from pydantic import BaseModel, constr


class DishCreateUpdate(BaseModel):
    title: str
    description: str
    price: constr(regex=r"^\d+(\.\d{1,2})?$")
