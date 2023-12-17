import csv
import os
import copy

class ReadCSV:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_csv()

    def read_csv(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        data = []
        with open(os.path.join(__location__, self.filename)) as f:
            rows = csv.DictReader(f)
            data = [dict(row) for row in rows]
        return data

class DB:
    def __init__(self):
        self.database = []

    def table_names(self):
        return [table.table_name for table in self.database]

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        return next((table for table in self.database if table.table_name == table_name), None)

    def project_id_exists(self, project_id):
        project_table = self.search('Project Table')
        return project_table and any(row.get('ProjectID') == project_id for row in project_table.data)

    def add_table(self, table):
        if table.table_name not in self.database:
            self.database.append(table)

    def get_table(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None

    def create_table(self, table_name, initial_data=None):
        if initial_data is None:
            initial_data = None
        new_table = Table(table_name, initial_data)
        self.add_table(new_table)
        return new_table

    def __str__(self):
        return '\n'.join(map(str, self.database))

class Table:
    def __init__(self, table_name: str, data: list or dict):
        self.table_name = table_name
        self.data = data
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def insert_data(self, new_data: dict):
        if not self.data:
            self.data.append(new_data)
        else:
            # Check if the keys in new_data match the keys in the existing table
            existing_keys = set(self.data[0].keys())
            new_data_keys = set(new_data.keys())
            if existing_keys == new_data_keys:
                self.data.append(new_data)
            else:
                raise KeyError("Keys in new data do not match keys in the table")

    def update_entry(self, user_id, key, value):
        for entry in self.data:
            user_id_key = list(entry.keys())[0]
            if entry[user_id_key] == user_id:
                entry[key] = value

    def join(self, other_table, common_key):
        joined_table = Table(
            f'{self.table_name}_joins_{other_table.table_name}', [])
        for item1 in self.data:
            for item2 in other_table.data:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.data.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(f'{self.table_name}_filtered', [])
        filtered_table.data = [entry for entry in self.data if condition(entry)]
        return filtered_table

    def aggregate(self, aggregation_function, aggregation_key):
        values = [float(entry[aggregation_key]) for entry in self.data]
        return aggregation_function(values)

    def select_attributes(self, selected_attributes):
        selected_data = []
        for entry in self.data:
            selected_data.append({key: entry[key] for key in selected_attributes if key in entry})
        return selected_data

    def __str__(self):
        return f'{self.table_name}: {str(self.data)}'
