from database import *

database_n = DB()


def initializing():
    read_person = ReadCSV('persons.csv')
    person_table = Table('Person table', read_person.data)
    database_n.insert(person_table)

    read_login = ReadCSV('login.csv')
    login_table = Table('Login table', read_login.data)
    database_n.insert(login_table)

    project_data = [
        {'ProjectID': None, 'Title': None, 'Lead': None, 'Member1': None,
         'Member2': None, 'Advisor': None, 'Status': None}]
    project_table = Table('Project table', project_data)
    database_n.insert(project_table)

    adPendReq_data = [
        {'ProjectID': None, 'to_be_advisor': None, 'Response': None, 'Response_date': None}]
    adPendReq_table = Table('Advisor_pending_request table', adPendReq_data)
    database_n.insert(adPendReq_table)

    memPendReq_data = [{'ProjectID': None, 'to_be_member': None, 'Response': None, 'Response_date': None}]
    memPendReq_table = Table('Member_pending_request table', memPendReq_data)
    database_n.insert(memPendReq_table)

def login():
    while True:
        username = input("Enter username: ")
        login_table = database_n.search('Login table')
        user_found = next((user for user in login_table.data if user['username'] == username), None)
        if user_found:
            break
        else:
            print("Username not found. Please try again.")
    password = input("Enter password: ")
    if user_found['password'] == password:
        return [user_found['ID'], user_found['role']]
    else:
        return None


def exit():
    """
    here are things to do in this function:
    - write out all the tables that have been modified to the corresponding csv files
    - By now, you know how to read in a csv file and transform it into a list of dictionaries.
        For this project, you also need to know how to do the reverse,
        i.e., writing out to a csv file given a list of dictionaries.
        See the link below for a tutorial on how to do this:
        https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python
    """
    for table in database_n.database:
        filename = f"{table.table_name}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            if table.data:
                headers = table.data[0].keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(table.data)
            else:
                print(f"Table '{table.table_name}' is empty. No CSV file created.")
    print("All tables have been written out to CSV files.")



initializing()
val = login()


# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
#     see and do admin related activities
# elif val[1] = 'student':
#     see and do student related activities
# elif val[1] = 'member':
#     see and do member related activities
# elif val[1] = 'lead':
#     see and do lead related activities
# elif val[1] = 'faculty':
#     see and do faculty related activities
# elif val[1] = 'advisor':
#     see and do advisor related activities

# once everyhthing is done, make a call to the exit function
exit()

