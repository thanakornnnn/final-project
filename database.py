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

    def __str__(self):
        return '\n'.join(map(str, self.database))

class Table:
    def __init__(self, table_name: str, data: list or dict):
        self.table_name = table_name
        self.data = data
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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

    def insert(self, entry, db_instance=None):
        if self.table_name in ['Advisor_pending_request Table', 'Member_pending_request table']:
            project_id = entry.get('ProjectID')
            if project_id and db_instance and not db_instance.project_id_exists(project_id):
                raise ValueError(f"ProjectID {project_id} does not exist in Project Table.")
        elif isinstance(entry, dict):
            self.data.append(entry)

    def add_field_to_dicts(self, dicts_list, field_name, field_value):
        for dict_item in dicts_list:
            dict_item[field_name] = field_value

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
