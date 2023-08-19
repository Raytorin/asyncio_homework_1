from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String


Base = declarative_base()


class SwapiCharacter(Base):

    __tablename__ = 'swapi_character'

    id = Column(Integer, primary_key=True, autoincrement=False)
    birth_year = Column(String, nullable=False)
    eye_color = Column(String, nullable=False)
    films = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    hair_color = Column(String, nullable=False)
    height = Column(String, nullable=False)
    homeworld = Column(String, nullable=False)
    mass = Column(String, nullable=False)
    name = Column(String, nullable=False)
    skin_color = Column(String, nullable=False)
    species = Column(String, nullable=True)
    starship = Column(String, nullable=True)
    vehicles = Column(String, nullable=True)
