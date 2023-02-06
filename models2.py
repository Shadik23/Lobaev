from sqlalchemy import Column, Integer, String
from database import Base


class Lobaev(Base):
    __tablename__="Lobaev Arms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    calibr = Column(String)
    description = Column(String)
    weight = Column(Integer)