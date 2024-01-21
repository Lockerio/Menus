from pydantic import BaseModel, constr


class MenuCreateUpdate(BaseModel):
    title: str
    description: str
