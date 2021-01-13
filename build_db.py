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


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship("Genre", back_populates = "albums")

    # total_score = Column(Float)
    # nb_votes = Column(Integer)
    # min_score = Column(Float)
    # max_score = Column(Float)
    # average_score = Column(Float)
    # min_pos = Column(Integer)
    # max_pos = Column(Integer)
    # average_pos = Column(Float)

    def print_fields(self):

        print("""
            ALBUM Object
            id: {}
            name: {}
            genre: {}
            """.format(
                self.id,
                self.name,
                (self.genre.name if self.genre else None)
            )
        )

    def get_values(self):

        values = [
            self.id,
            self.name,
            (self.genre.name if self.genre else None)
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
            (self.album.name if self.album else None),
            self.position,
            self.score
        ]
        return values
        
# define all back-propagated relationships
User.entries = relationship("Entry", back_populates = "user")
Album.entries = relationship("Entry", back_populates = "album")
Genre.albums = relationship("Album", back_populates = "genre")


def create_schema():

    Base.metadata.create_all(engine)

if __name__ == "__main__":

    create_schema()
