from __future__ import unicode_literals

import random
import sqlite3

import os


class DatabaseAccessor:

    def __init__(self, initialise_columns=False):
        self.db_path = 'faces.sqlite'
        self.db = sqlite3.connect(self.db_path)
        # Get a cursor object
        self.cursor = self.db.cursor()
        # Check if table users does not exist and create it
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS faces(id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT)''')
        self.db.row_factory = self.dict_factory

        if initialise_columns:
            self.initialise_columns()

    def initialise_columns(self):
        num_columns = 128
        for i in range(0, num_columns):
            col_name = "face_" + str(i)
            self.cursor.execute("alter table faces add column '%s' 'float'" % col_name)
            print("Added column: {}".format(col_name))

    def dict_factory(self, cursor, row):
        dict = {}
        for idx, col in enumerate(self.cursor.description):
            dict[col[0]] = row[idx]
        return dict

    def save_face(self, name, face_encoding):
        # todo update value if duplicate
        # todo store checksum
        # faces = "'{}'".format(name)
        # values = "?"
        # for idx, elem in enumerate(face_encoding):
        #     faces += "," + str(idx)
        #     values += ",?"
        #
        # query = '''INSERT INTO faces({}) VALUES({}) '''.format(faces, values)
        # print query
        # self.cursor.execute(query, "faces")

        row = face_encoding
        row.insert(0, "'{}'".format(name))
        cols = ', '.join('"{}"'.format(col) for col in range(0, len(row)))
        vals = ', '.join('{}'.format(face_encoding[col]) for col in range(0, len(row)))
        sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format("faces", cols, vals)
        self.cursor.execute(sql)
        self.db.commit()

        # for item in face_encoding:
        #     self.cursor.execute('insert into faces values (?,?,?)', item)

    def show_data(self):
        res = self.cursor.execute("select * from faces")
        r = res.fetchall()
        for x in r:
            print(x)

db = DatabaseAccessor()

face_encoding = [random.uniform(-20.0, 20.0) for i in range(0, 3)]
db.save_face("test", face_encoding)

print(db.show_data())

