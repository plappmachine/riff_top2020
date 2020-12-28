#!python3

import os
import openpyxl as opx

from build_db import engine, User, Album, Entry
from sqlalchemy.orm import sessionmaker

input_excelpath = "scoring top2020.xlsx"
output_excelpath = "top2020_entries.xlsx"

Session = sessionmaker(bind=engine)
session = Session()

def load_worksheet():

    wb = opx.load_workbook(input_excelpath)
    entries = wb['entries']

    return entries, wb

def add_user_entry(raw_entry):

    user_name = raw_entry[1].value
    # top_size = raw_entry[1].value
    top_size = len(list(x for x in raw_entry if x.value is not None))-2

    print("======================== NAME: {} ========================".format(user_name))
    # print('TOP SIZE EQUAL ? {}'.format(top_size == top_size_1))
    print('FILE TOP SIZE = {}'.format(top_size))
    # print('CALC TOP SIZE = {}'.format(top_size_1))
    
    user_obj = session.query(User).filter(User.name == user_name).first()
    if user_obj is None:
        user_obj = User(
            name = user_name,
            top_size = top_size
        )
        session.add(user_obj)

    for i in range(2,top_size+2):
        
        raw_name = raw_entry[i].value
        position = i-1
        
        if raw_name:
        
            entry_name = raw_name.lower()
            print(entry_name)

            entry_score = score(position,top_size)
            print('Entry Score: {}'.format(entry_score))
            entry_obj = Entry(
                user = user_obj,
                name = entry_name,
                # album = album_obj,
                position = position,
                score = entry_score
            )
            session.add(entry_obj)

        else:
            break

def score(position, top_size):

    return 30 - 25*(position-1)/(top_size-1)

def export_linear_entries():

    wb = opx.Workbook()
    entries = session.query(Entry).all()
    ws = wb.create_sheet(title='entries_linear')
    header = [
        'id',
        'user',
        'entry_name',
        'position',
        'score'
    ]
    ws.append(header)
    
    for entry in entries:
        ws.append(entry.get_values())

    wb.save(output_excelpath)

def main():

    entries, wb = load_worksheet()

    for raw_entry in entries.rows:
        add_user_entry(raw_entry)

    export_linear_entries()

    session.commit()

    # add_albums(wb)
    # calculate_album_stats()
    # export_albums()

    


if __name__ == "__main__":
    main()
