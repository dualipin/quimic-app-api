from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, index=True)
    username = Column(String, index=True)
    score = Column(Integer)
    name = Column(String)
