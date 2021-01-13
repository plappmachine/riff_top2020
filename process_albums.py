#!python3

import os
import statistics as st
import openpyxl as opx

from build_db import engine, User, Album, Entry, Genre
from add_albums import export_album_list

from sqlalchemy.orm import sessionmaker

entries_excelpath = "top2020_entries.xlsx"
albumlist_excelpath = "top2020_albums_list.xlsx"
genres_excelpath = "genres_list.xlsx"

Session = sessionmaker(bind=engine)
session = Session()


def update_albums_genres():

    albums_wb = opx.load_workbook(albumlist_excelpath)
    ws = albums_wb['albums_scores']

    for row in ws.rows:
        
        album_id = row[0].value
        album_name = row[1].value
        genre_name = row[2].value
        genre_obj = session.query(Genre).filter(Genre.name == genre_name).first()
        # skip header row
        if album_id  == 'id':
            continue
        
        print("ALBUM NAME: {}".format(album_name))
        album_obj = session.query(Album).filter(Album.name == album_name).first()
        print("ALBUM OBJ: {}".format(album_obj))
        album_obj.genre = genre_obj


def main():

    update_albums_genres()
    # export_album_list()

    session.commit()
    
if __name__ == "__main__":
    main()
