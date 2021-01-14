# README

This is a small home project made to compute a ranking between a collection of objects. In that case, the objects are musical records, sourced from responses to a web poll. In addition to the ranking between all musical albums, the code computes a couple of interesting statistics about the respondent population.

# Context

This code was written for the '2020 album of the year' poll of a facebook group dedicated to rock music. We wanted people to vote for the albums they loved in 2020, and order them by preference. The goal was to aggregate all votes with a scoring system that would do justice not only to the albums that were the most cited, but also shed light to a certain extent on niche albums that people loved.

Group members were asked to provide and classify their preferred albums for 2020 through a simple Google Forms poll. Two constraints were given :

- Each individual 'AOTY' list needed to be **ordered** (ie, no "ex aequo" in a list)
- **List size is not constant** ; minimum = 3 albums, maximum = 30 albums

In addition to a tier-list of the community's album preferences, data from the poll was enriched with contextual information - mainly, the musical sub-genres involved - and additional insights were provided to the community's members : the general and individual preferences for members towards a sub-genre or another, their sense of either eclectism or specialization, who is following the group's tendency, and who has the most 'niche' tastes.

The code is entirely made in Python, using the following modules :

- openpyxl for I/O with excel data
- sqlalchemy to manage a small local db
- pandas for computing the metrics and insights

# Input Structure

The input is taken in a simple Google Form and the resulting excel file thus depends on how Google implement their outputs.

An example structure can be found in the '**scoring top2020.xslx'** file :

- One header line giving the field names
- One line for each User that responded to the poll
- Each cell of each line is an 'entry', ie a reference to an album
- Each line has as many entries as the user entered - which means each line can have a length between 3 and 30

To be able to process these lines accordingly, the data needs to be 'linearized' into a tabular structure where each line is an entry - as opposed to lines with several entries and a varying size.

This is the first step of the Data Flow described below.

# Data Flow

As the technical means are very limited - no access or connection to a structured web database -  group members were asked to provide their responses through a web form, each 'entry' being given in a free text field. Which means each member could have their own way of writing an album's name.

As a consequence, the 'raw', input data needs some human-made cleaning and processing to be structured into a reliable database, upon which metrics can be calculated.

The workflow follows 6 main steps:

1. Initiate the data structure
2. **manual step :** harmonize album names in the poll responses
3. add the harmonized album names to the database so they can be aggregated
4. **manual step :** enrich the albums list with the musical genres
5. update the albums/genres in the db
6. compute the final ranking and statistics

## 1. Initiate Data Structure

That's where you create the sqlite3 db and populate the first entry table.

To create the database and the schema, just run :

```graphql
./build_db.py
```

It creates the db and schema using the sqlalchemy ORM. To understand the schema, plz read build_db.py. You'll need a basic familiarity with sqlalchemy 🙂

Then you need to populate the first, 'raw' table of user entries :

```graphql
./add_entries.py
```

**definition :** an 'entry' is an response to one poll question by one user. In other terms, a user that submitted their 'top 15' albums of 2020 through the poll has generated 15 entries, each one referencing an album.

The add_entries script reads the '**scoring top2020.xlsx**' file and converts the input data into a linear list of entries, in the 'entry' table of the db.

add_entries.py outputs a new excel file, **top2020_entries.xlsx** which contains the linear entries taken from the db table.

## 2. Harmonize album names in entries

At this point entries given by users are mentions of musical albums with potentially different spellings for a given album that is cited several times. 

At this point you need to harmonize album names in the **top2020_entries.xlsx** file. 

For each value in the 'entry_name' column, there needs to be a corresponding value in the 'album_name' column, that follows a more rigorous spelling pattern. 

The important thing is, if several entries are about the same album, but 'entry_name' values have different spellings, all the corresponding **'album_name' values MUST have the same spelling**, so the votes count can be properly aggregated for any given album. This is manual work in excel, you can figure it out 😉

## 3. Add the Albums to the db

When all 'album_names' are filled out and harmonized, you can populate the 'albums' table of the database by running the script :

```graphql
./add_albums.py
```

The script takes **top2020_entries.xslx** as input and creates the 'albums' db objects accordingly. It also takes **genres_list.xlsx** as input and populates the 'genres' table of the database with the list of accepted musical sub-genres. You can edit the list with whatever values you like and re-run the script as many times as necessary if you wish to alter / add more genres.

The script outputs the following file : **top2020_albums_list.xlsx** which contains the list of all albums and the list of all genres.

## 4. Enrich albums with musical genres

At this point the 'albums' table basically has album names. To get richer insights you can add the musical genre for each album in the **top2020_albums_list.xlsx** file.

This is manual work again ; the list of all genres in the file is there so you can apply Data Validation to the 'genre' column, so the work can be a little bit easier anf fail-proof if you work on this as a team, as we did.

## 5. Update the album & genres in the db

Run the script :

```graphql
./process_albums.py
```

It reads out the **top2020_albums_list.xlsx** and updates the 'albums' table in the db by adding / editing each album's 'genre' field value, according to the list you curated.

## 6. Compute all metrics and insights

Now that you have a clean and complete database of entries, albums, users and genres, this is when the magic happens.

Run the final script to generate all insights :

```graphql
./compute_stats.py
```

To understand all the insights that are calculated here, see the 'Metrics' section below.

If you want to test out, modify or scrutinize how all metrics are built, you can use the Jupyter notebook, which basically has all python functions used in the script, but split out into cells so you can visualize data at every step :

```graphql
./compute_stats.ipynb
```

# Metrics Definitions

Here is a definition  of all metrics used in the code :

[Untitled](https://www.notion.so/ad9087e0d25949a2862d3a94debd60bb)