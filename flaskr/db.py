import sqlite3

DATABASE = "baseball.db"

def create_books_table():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS  player\
         (player_id INTEGER PRIMARY KEY AUTOINCREMENT, \
            family_name TEXT, \
            first_name  TEXT,\
            age tinyint, career text,\
            hometown text, hand text,\
            bbox text, position text,\
            meatAbility tinyint,\
            powerAbility tinyint,\
            trajectory tinyint,\
            speedAbility tinyint,\
            shoulderAbility tinyint,\
            throwAbility tinyint,\
            catchAbility tinyint)")
    con.close()