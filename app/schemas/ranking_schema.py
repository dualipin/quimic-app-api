from pydantic import BaseModel


class RankingSchema(BaseModel):
    user: int
    score: int
    name: str
    username: str

    model_config = {"from_attributes": True}


class CreateRankingItem(RankingSchema):
    pass


class RankingItem(RankingSchema):
    id: int
