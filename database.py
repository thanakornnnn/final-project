import os
import csv

class ReadCSV:
    def __init__(self, file_name):
        self.file_name = file_name
        self.list = []

    def open_csv(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        file_path = os.path.join(__location__, self.file_name)
        with open(file_path) as f:
            rows = csv.DictReader(f)
            for r in rows:
                self.list.append(dict(r))
        return self.list

class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


# add in code for a Table class
import copy


class Table:
    def __init__(self, table_name, data):
        self.table_name = table_name
        self.data = data

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.data:
            for item2 in other_table.data:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.data.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.data:
            if condition(item1):
                filtered_table.data.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.data:
            temps.append(float(item1[aggregation_key]))
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.data:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.data)

    def insert_row(self, list):
        return self.data.append(list)

    def update_row(self, primary_attribute, primary_attribute_value, update_attribute, update_value, prima,
                   selected_key):
        for i, row in enumerate(self.data):
            if row[primary_attribute] == primary_attribute_value and row[prima] == selected_key:
                self.data[i][update_attribute] = update_value
                break

    def to_dict(self, dict_key, dict_value):
        return {dict_key: self.table_name, dict_value: self.data}

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary