# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file
import csv
import os

# __location__ = os.path.realpath(
#     os.path.join(os.getcwd(), os.path.dirname(__file__)))
#
# persons = []
# with open(os.path.join(__location__, 'persons.csv')) as f:
#     rows = csv.DictReader(f)
#     for r in rows:
#         persons.append(dict(r))
# print(persons)

class Readcsv:
    def __init__(self, filename):
        self.data = []
        self.filename = filename
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def read_csv(self):
        with open(self.filename) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.data.append(dict(row))

# add in code for a Database class

class DB:
    def __init__(self):
        self.database = []

    def table_names(self):
        return [table.table_name for table in self.database]

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for i in self.database:
            if i.table_name == table_name:
                return i
        return None

    def __str__(self):
        return '\n'.join(map(str, self.database))

# add in code for a Table class

import copy

class Table:
    def __init__(self, table_name: str, data: list or dict):
        self.table_name = table_name
        self.data = data
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def update_entry(self, user_id, key, value):
        for i in self.data:
            user_id_key = list(i.keys())[0]
            if i[user_id_key] == user_id:
                i[key] = value

        def join(self, other_table, common_key):
            joined_table = Table(
                self.table_name + '_joins_' + other_table.table_name, [])
            for item1 in self.table:
                for item2 in other_table.table:
                    if item1[common_key] == item2[common_key]:
                        dict1 = copy.deepcopy(item1)
                        dict2 = copy.deepcopy(item2)
                        dict1.update(dict2)
                        joined_table.data.append(dict1)
            return joined_table

        def insert_entry(self, new_entry):
            if isinstance(new_entry, dict):
                self.data.append(new_entry)



# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary

# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated
