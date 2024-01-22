from pydantic import BaseModel


class SubmenuCreateUpdate(BaseModel):
    title: str
    description: str
