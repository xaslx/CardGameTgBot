from pydantic import BaseModel




class UserCreate(BaseModel):
    user_id: int



class UserOut(BaseModel):
    rating: int
    name: str
    money: int
    wins: int
    losses: int
    games: int
    draw: int
