#!python3

import os
import statistics as st
import openpyxl as opx
import pandas as pd

from build_db import engine

results_excelpath = "top2020_RESULTS.xlsx"

df_entries = pd.read_sql_table('entries',engine)
df_albums = pd.read_sql_table('albums',engine,index_col='id')
df_users = pd.read_sql_table('users',engine,index_col='id')
df_genres = pd.read_sql_table('genres',engine,index_col='id')

def compute_all_stats():

   entries = build_entries()
   entries = format_entries(entries)

   print(entries.head(20))

   album_results = build_album_stats(entries)
   album_results = format_album_results(album_results)
   album_results.to_sql('album_stats', engine, if_exists='replace')

   full_entries = extend_entries(entries, album_results)
   full_entries = compute_entry_stats(full_entries)
   full_entries.to_sql('entry_stats', engine, if_exists='replace')

   user_genres, user_edgyness = compute_user_stats(full_entries)

   # write it all to a big Excel
   writer = pd.ExcelWriter(results_excelpath)
   album_results.to_excel(writer, sheet_name='album_results')
   full_entries.to_excel(writer, sheet_name='full_entries')
   user_genres.to_excel(writer, sheet_name='user_genres')
   user_edgyness.to_excel(writer, sheet_name='user_edgyness')

   writer.save()


   # album_results.to_excel('top2020_album_results.xlsx')

def build_entries():

   entries = pd.merge(df_entries, df_albums, left_on='album_id', right_on='id')
   entries = pd.merge(entries, df_genres, left_on='genre_id', right_on='id')

   return entries

def format_entries(entries):

   map = {
      'id':'entry_id',
      'user_id':'user_id',
      'album_id':'album_id',
      'name_y':'album',
      'genre_id':'genre_id',
      'name':'genre',
      'position':'position',
      'score':'score'
   }

   drop_cols = (x for x in entries.columns if x not in map.keys())

   entries.drop(drop_cols, axis=1, inplace=True)
   entries.rename(map, axis=1, inplace=True)
   entries.set_index('entry_id', drop=False, inplace=True)

   return entries

def build_album_stats(entries):

   album_stats = pd.pivot_table(entries, index = ['genre_id','genre','album_id','album'], values = ['score','position'], aggfunc=['count','sum','mean','min','max'])

   album_ranking = album_stats.rank(method='dense',ascending=False)[('sum','score')]
   album_genre_ranking = album_stats.groupby('genre').rank(method='dense',ascending=False)[('sum','score')]

   album_results = pd.merge(album_stats, album_ranking, left_index=True, right_index=True)
   album_results = pd.merge(album_results, album_genre_ranking, left_index=True, right_index=True)

   album_results.reset_index(inplace=True)

   return album_results

def format_album_results(album_results):

   album_results.columns = album_results.columns.map('|'.join).str.strip('|')

   map = {
      'sum_y|score':'rank',
      'album_id':'album_id',
      'album':'album',
      'sum|score':'genre_rank',
      'genre_id':'genre_id',
      'genre':'genre',
      'count|score':'nb_votes',
      'sum_x|score':'total_score',
      'mean|score':'mean_score',
      'max|score':'highest_score',
      'min|score':'lowest_score',
      'mean|position':'mean_position',
      'min|position':'highest_position',
      'max|position':'lowest_position'
   }
   
   album_results = album_results.reindex(columns=map.keys())

   drop_cols = (x for x in album_results.columns if x not in map.keys())
   album_results.drop(drop_cols, axis=1, inplace=True)
   
   album_results.rename(map, axis=1, inplace=True)

   album_results.set_index('album_id', inplace=True, drop=True)

   album_results.sort_values('rank', inplace=True)

   return album_results

def extend_entries(entries, album_results):

    album_keepcols = [
        'album_id',
        'total_score'
    ]
    album_dropcols = (x for x in album_results.columns if x not in album_keepcols)
    album_scores = album_results.drop(album_dropcols, axis=1)

    full_entries = pd.merge(entries, album_scores, on='album_id')

    full_entries = pd.merge(full_entries, df_users, left_on='user_id', right_on='id')

    full_entries.set_index('entry_id', inplace=True)
    cols = [
        'user_id',
        'name',
        'album_id',
        'album',
        'genre_id',
        'genre',
        'top_size',
        'position',
        'score',
        'total_score'
    ]

    full_entries = full_entries.reindex(columns=cols)

    return full_entries

def compute_entry_stats(full_entries):

    full_entries['pop_score'] = full_entries['score'] * full_entries['total_score'] / 1000
    full_entries['edgyness'] = full_entries['top_size'] / full_entries['pop_score']

    full_entries.sort_values('entry_id', inplace=True)

    return full_entries

def compute_user_stats(full_entries):
    
    user_genres = pd.pivot_table(full_entries, index=['name'], columns=['genre'], values=['score'], aggfunc=['sum'])
    user_edgyness = pd.pivot_table(full_entries, index = ['name'], values=['pop_score','edgyness'], aggfunc=['sum','mean'])

    user_edgyness.sort_values(('mean','edgyness'), ascending=False, inplace=True)

    return user_genres,user_edgyness

if __name__ == "__main__":

   compute_all_stats()