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

def main():

   print("TODO")
    


if __name__ == "__main__":
    main()
