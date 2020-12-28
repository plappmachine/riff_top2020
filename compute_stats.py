#!python3

import os
import statistics as st
import openpyxl as opx

from build_db import engine, User, Album, Entry
from sqlalchemy.orm import sessionmaker

input_excelpath = "top2020_entries.xlsx"
output_excelpath = "top2020_entries.xlsx"

Session = sessionmaker(bind=engine)
session = Session()

def load_worksheet():

    wb = opx.load_workbook(input_excelpath)
    ws = wb['albums_list']

    return ws, wb

def add_albums_genres(ws):

    for row in ws.rows:
        
        album_id = row[0].value
        genre = row[2].value
        # skip header row
        if album_id  == 'id':
            continue
        
        album_obj = session.query(Album).filter(Album.id == album_id).first()
        album_obj.genre = genre


def calculate_album_stats():

    for album in session.query(Album):
        
        entries = session.query(Entry).join(Album).filter(Album.id == album.id).all()
        
        scores = set(entry.score for entry in entries)
        album.total_score = sum(scores)
        album.min_score = min(scores)
        album.max_score = max(scores)
        album.average_score = st.mean(scores)

        positions = set(entry.position for entry in entries)
        album.min_pos = min(positions)
        album.max_pos = max(positions)
        album.average_pos = st.mean(positions)

        album.nb_votes = len(entries)

        album.print_fields()

def export_albums(workbook):

    albums = session.query(Album).all()
    ws = workbook.create_sheet(title='albums_scores')
    header = [
        'id',
        'name',
        'genre',
        'total_score',
        'nb_votes',
        'min_score',
        'max_score',
        'average_score',
        'min_pos',
        'max_pos',
        'average_pos'
    ]
    ws.append(header)
    
    for album in albums:
        ws.append(album.get_values())

    workbook.save(output_excelpath)

def main():

    ws, wb = load_worksheet()
    
    add_albums_genres(ws)
    calculate_album_stats()
    export_albums(wb)

    session.commit()
    


if __name__ == "__main__":
    main()
