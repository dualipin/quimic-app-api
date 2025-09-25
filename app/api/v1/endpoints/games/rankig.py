from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import ranking_service
from app.schemas.ranking_schema import CreateRankingItem, RankingItem

router = APIRouter(prefix="/ranking")


@router.post("/create", response_model=RankingItem)
def create_ranking(item: CreateRankingItem, db: Session = Depends(get_db)):
    return ranking_service.create_ranking_item(db, item)


@router.get("/list/{name}", response_model=list[RankingItem])
def list_rankings(name: str, db: Session = Depends(get_db)):
    return ranking_service.get_rankings(db, name)


@router.put("/update/{user}/{name}", response_model=list[RankingItem])
def update_ranking(user: int, name: str, new_score: int, db: Session = Depends(get_db)):
    ranking_service.update_score(db, user, name, new_score)
    return ranking_service.get_rankings(db, name)
