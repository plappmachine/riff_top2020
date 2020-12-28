#!python3

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db="sqlite:///top2020.db"
engine = create_engine(db,echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    top_size = Column(Integer)

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)
    # genre_02 = Column(String)
    total_score = Column(Float)
    nb_votes = Column(Integer)
    min_score = Column(Float)
    max_score = Column(Float)
    average_score = Column(Float)
    min_pos = Column(Integer)
    max_pos = Column(Integer)
    average_pos = Column(Float)

    def print_fields(self):

        print("""
            ALBUM Object
            id: {}
            name: {}
            genre: {}
            total_score: {}
            nb_votes: {}
            min_score: {}
            max_score: {}
            average_score: {}
            min_pos: {}
            max_pos: {}
            average_pos: {}
            """.format(
                self.id,
                self.name,
                self.genre,
                self.total_score,
                self.nb_votes,
                self.min_score,
                self.max_score,
                self.average_score,
                self.min_pos,
                self.max_pos,
                self.average_pos
            )
        )

    def get_values(self):

        values = [
            self.id,
            self.name,
            self.genre,
            # self.genre_02,
            self.total_score,
            self.nb_votes,
            self.min_score,
            self.max_score,
            self.average_score,
            self.min_pos,
            self.max_pos,
            self.average_pos
        ]
        return values

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates = "entries")
    
    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship("Album", back_populates = "entries" )

    position = Column(Integer, nullable = False)
    score = Column(Float)

    def get_values(self):

        values = [
            self.id,
            self.user.name,
            self.name,
            self.position,
            self.score
        ]
        return values
        
User.entries = relationship("Entry", back_populates = "user")
Album.entries = relationship("Entry", back_populates = "album")

def create_schema():

    Base.metadata.create_all(engine)

if __name__ == "__main__":

    create_schema()
    # print("safe")
