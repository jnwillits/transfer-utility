"""
Data Transfer Utility for Code Driller
Copyright (c) 2019 (MIT License) Jeffrey Neil Willits   @jnwillits

This reads content from The Flashcard Project database and stores it in the SQL database for the Code Driller web application.

Here is the structure of the imported database: {card: [status, '', '', set()], }
"""

import pickle
import os
import sys
from pathlib import Path
import sqlite3


def read(card_file):
    card_path = ''
    if os.path.exists(card_file):
        card_path = Path.cwd() / card_file
    if os.path.isfile(card_path):
        with open(card_path, 'rb') as f:
            cards = pickle.load(f)
    else:
        print(f'The file {card_file} is not available.')
    return cards


if __name__ == '__main__':
        cards = {}
        cards = read('fp-python.db')

        try:
            sqliteConnection = sqlite3.connect('site.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")


            for card_num in range(1, len(cards)):
                my_query = f'INSERT INTO python_cards (user_id, question, answer, upvoted, downvoted, flagged, flag_reason)
                    VALUES (1, "{cards[card_num][1]}", "{cards[card_num][2]}", 0, 0, 0, 0);'
                sqlite_insert_query = my_query
                count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            print("Record inserted successfully into python_cards table ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

        sys.exit()
