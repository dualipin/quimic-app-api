from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.ranking import Ranking
from app.schemas.ranking_schema import CreateRankingItem, RankingItem


def create_ranking_item(db: Session, item: CreateRankingItem) -> RankingItem:
    db_item = Ranking(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return RankingItem.model_validate(db_item)


def get_rankings(db: Session, name: str) -> list[RankingItem]:
    subquery = (
        db.query(Ranking.user, func.max(Ranking.score).label("max_score"))
        .filter(Ranking.name == name)
        .group_by(Ranking.user)
        .subquery()
    )

    return [
        RankingItem.model_validate(item)
        for item in db.query(Ranking)
        .join(
            subquery,
            (Ranking.user == subquery.c.user) & (Ranking.score == subquery.c.max_score),
        )
        .filter(Ranking.name == name)
        .order_by(Ranking.score.desc())
        .all()
    ]


def update_score(db: Session, user: int, name: str, new_score: int):
    db.query(Ranking).filter(Ranking.user == user, Ranking.name == name).update(
        {"score": new_score}
    )
    db.commit()
