from pydantic import BaseModel


class TodoCreate(BaseModel):
    """Schema for creating a todo."""

    title: str
    description: str | None = None
    status: str | None = "pending"


class TodoUpdate(BaseModel):
    """Schema for updating a todo."""

    title: str | None = None
    description: str | None = None
    status: str | None = None


class TodoOut(TodoCreate):
    """Schema for todo output."""

    id: int

    class Config:
        from_attributes = True
