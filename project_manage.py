from database import *
import random

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

def generate_random_project_id():
    """
    Generates a random 4-digit ID for a project.
    Returns a string of 4 digits.
    """
    __random_id = f"{random.randint(0, 9999):04d}"
    return __random_id

random_id = generate_random_project_id()


class Student:
    def __init__(self, ID, status, projectID):
        self.ID = ID
        self.status = status
        self.projectID = projectID

    def view_requests(self, memberstatus):
        pending_requests = [request for request in
                            memberstatus.table if
                            request['to_be_member'] == self.ID]
        for request in pending_requests:
            print(f"ProjectID: {request['ProjectID']}, Response: {request['Response']}, Date: {request.get('Response_date', 'N/A')}")
        return pending_requests

    def accept_deny_request(self, request_id, accept, memberstatus, project_table):
        for request in memberstatus.table:
            if request['ProjectID'] == request_id:
                if accept:
                    request['Response'] = 'Accepted'
                    for project in project_table.table:
                        if project['ProjectID'] == request_id:
                            if self.ID != project['Member1'] and self.ID != \
                                    project['Member2']:
                                if project['Member1'] is None:
                                    project['Member1'] = self.ID
                                elif project['Member2'] is None:
                                    project['Member2'] = self.ID
                                else:
                                    print(
                                        "Project already has maximum members.")
                                break
                else:
                    request['Response'] = 'Denied'
                break

    def handle_requests(self, member_pending_request_table, project_table):
        print('Project Invitation:')
        pending_requests = self.view_requests(member_pending_request_table)
        if pending_requests:
            request_id = input(
                "Enter the ProjectID to respond to (or 'exit' to cancel): ")
            if request_id.lower() == 'exit':
                return
            response = input(
                "Do you want to accept (type 'accept') or deny (type 'deny') the request? ")
            if response.lower() in ['accept', 'deny']:
                accept = response.lower() == 'accept'
                self.accept_deny_request(request_id, accept,
                                         member_pending_request_table,
                                         project_table)
                print("Request response updated.")
            else:
                print("Invalid response. No action taken.")
        else:
            print("No pending requests.")

    def change_to_lead(self, project_id, member_pending_request_table, project_table):
        for request in member_pending_request_table.table:
            if request['to_be_member'] == self.ID:
                request['Response'] = 'Denied'
        is_already_lead = any(
            project['Lead'] == self.ID for project in project_table.table)
        if is_already_lead:
            print("This student is already a project lead.")
        print(f"Role changed to 'lead' for project {project_id}. New project created.")


class Lead:
    def __init__(self, person_id, first, last):
        self.person_id = person_id
        self.person_first = first
        self.person_last = last
        self.person_type = "Lead"

    def project_status(self, project_id, project_table):
        project = next((p for p in project_table.table if p['ProjectID'] == project_id), None)
        if project:
            print(f"\nProject Status - ProjectID: {project_id}, Title: {project['Title']}, Status: {project['Status']}")
        else:
            print(f"No project found with ProjectID {project_id}.")

    def modify_project(self, project_table):
        project_id = input("Enter the ProjectID you want to modify: ")
        project = next((p for p in project_table.table if p['ProjectID'] == project_id), None)
        if project:
            print("\nCurrent Project Details:")
            for key, value in project.items():
                print(f"{key}: {value}")
            new_title = input("Enter the new title for the project (or press Enter to keep the current title): ")
            if new_title:
                project['Title'] = new_title
            print(f"Project details updated for ProjectID {project_id}.")
        else:
            print(f"No project found with ProjectID {project_id}.")

    def create_project(self, project_table, member_table):
        project_title = input("Enter the title of the project: ")
        existing_project = next((project for project in project_table.table if project['Lead'] == self.person_id), None)
        if existing_project:
            print(f"You are already leading a project with ProjectID {existing_project['ProjectID']}.")
        else:
            new_project = {
                'ProjectID': generate_random_project_id(),
                'Title': project_title,
                'Lead': self.person_id,
                'Member1': None,
                'Member2': None,
                'Advisor': None,
                'Status': 'Open'
            }
            project_table.insert_data(new_project)
            print(f"Project '{project_title}' created with ProjectID {new_project['ProjectID']}.")
            project_csv_filename = 'Project_table.csv'
            with open(project_csv_filename, mode='w', newline='', encoding='utf-8') as file:
                headers = project_table.data[0].keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(project_table.data)
            print(f"'Project table' saved to {project_csv_filename}.")


class Member:
    def __init__(self, person_id, first, last):
        self.person_id = person_id
        self.person_first = first
        self.person_last = last
        self.person_type = "Member"

    def modify_project(self, project_table):
        project_id = input("Enter the ProjectID you want to modify: ")
        project = next((p for p in project_table.table if p['ProjectID'] == project_id), None)
        if project and self.person_id in [project['Member1'], project['Member2']]:
            print("\nCurrent Project Details:")
            for key, value in project.items():
                print(f"{key}: {value}")
            new_title = input("Enter the new title for the project (or press Enter to keep the current title): ")
            if new_title:
                project['Title'] = new_title
            print(f"Project details updated for ProjectID {project_id}.")
        elif not project:
            print(f"No project found with ProjectID {project_id}.")
        else:
            print(f"You are not a member of the project with ProjectID {project_id}.")


class NormalFaculty:
    def __init__(self, person_id, first, last):
        self.person_id = person_id
        self.person_first = first
        self.person_last = last
        self.person_type = "Normal Faculty"

    def deny_to_serve_as_advisor(self, project_id, advisor_pending_request_table):
        request = next((r for r in advisor_pending_request_table.data if r['ProjectID'] == project_id), None)
        if request:
            request['Response'] = 'Denied'
            print(f"Advisor request for ProjectID {project_id} denied.")
        else:
            print(f"No pending advisor request found for ProjectID {project_id}.")

    def view_all_projects(self, project_table):
        print("\nList of All Projects:")
        for project in project_table.table:
            print(f"ProjectID: {project['ProjectID']}, Title: {project['Title']}, Status: {project['Status']}")

    def evaluate_project(self, project_id, project_table):
        project = next((p for p in project_table.table if p['ProjectID'] == project_id), None)
        if project:
            print(f"\nEvaluate Project - ProjectID: {project_id}, Title: {project['Title']}")
            evaluation = input("Enter your evaluation and feedback for the project: ")
            print(f"Thank you for evaluating ProjectID {project_id}.")
        else:
            print(f"No project found with ProjectID {project_id}.")


class AdvisingFaculty:
    def __init__(self, person_id, first, last):
        self.person_id = person_id
        self.person_first = first
        self.person_last = last
        self.person_type = "Advising Faculty"

    def deny_to_serve_as_advisor(self, project_id, advisor_pending_request_table):
        request = next((r for r in advisor_pending_request_table.data if r['ProjectID'] == project_id), None)
        if request:
            request['Response'] = 'Denied'
            print(f"Advisor request for ProjectID {project_id} denied.")
        else:
            print(f"No pending advisor request found for ProjectID {project_id}.")

    def accept_to_serve_as_advisor(self, project_id, advisor_pending_request_table):
        request = next((r for r in advisor_pending_request_table.data if r['ProjectID'] == project_id), None)
        if request:
            request['Response'] = 'Accepted'
            print(f"Advisor request for ProjectID {project_id} accepted.")
        else:
            print(f"No pending advisor request found for ProjectID {project_id}.")

    def view_all_projects(self, project_table):
        print("\nList of All Projects:")
        for project in project_table.table:
            print(f"ProjectID: {project['ProjectID']}, Title: {project['Title']}, Status: {project['Status']}")

    def evaluate_project(self, project_id, project_table):
        project = next((p for p in project_table.table if p['ProjectID'] == project_id), None)
        if project:
            print(f"\nEvaluate Project - ProjectID: {project_id}, Title: {project['Title']}")
            evaluation = input("Enter your evaluation and feedback for the project: ")
            print(evaluation)
            print(f"Thank you for evaluating ProjectID {project_id}.")
        else:
            print(f"No project found with ProjectID {project_id}.")

    def approve_project(self, project_id, project_table):
        project = next((p for p in project_table.table if p['ProjectID'] == project_id), None)
        if project:
            project['Status'] = 'Approved'
            print(f"ProjectID {project_id} has been approved.")
        else:
            print(f"No project found with ProjectID {project_id}.")

class Admin:
    pass

initializing()
val = login()

memPendReq_table = database_n.search('Member_pending_request')
project_table = database_n.search('project')
login_table = database_n.search('login')

memPendReq_mockdata = [
    {'ProjectID': 'P001', 'to_be_member': '9898118', 'Response': None, 'Response_date': None},
    {'ProjectID': 'P002', 'to_be_member': '9898118', 'Response': None, 'Response_date': None}
]
project_mockdata = [
    {'ProjectID': 'P001', 'Title': 'Project A', 'Lead': None, 'Member1': None, 'Member2': None, 'Advisor': None, 'Status': 'Open'},
    {'ProjectID': 'P002', 'Title': 'Project B', 'Lead': None, 'Member1': None, 'Member2': None, 'Advisor': None, 'Status': 'Open'}
]

advisorPendReq_data = [{'ProjectID': None, 'to_be_advisor': None, 'Response': None, 'Response_date': None}]
advisor_pending_request_table = Table('Advisor_pending_request', advisorPendReq_data)
database_n.insert(advisor_pending_request_table)

from database import Table

member_table_data = [
    {'ID': '1', 'first': 'John', 'last': 'Doe', 'Status': 'Available'},
    {'ID': '2', 'first': 'Jane', 'last': 'Doe', 'Status': 'Available'},]
member_table = Table('Member table', member_table_data)


if val[1] == 'student':
    student_instance = Student(val[0], memPendReq_table, project_table)
    while True:
            print("\n=== Student Menu ===")
            print("1. View Pending Requests")
            print("2. Accept or Deny Requests")
            print("3. View Project Details")
            print("4. Change Role to Lead")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                student_instance.view_requests(memPendReq_table)
            elif choice == '2':
                student_instance.handle_requests(memPendReq_table, project_table)
            elif choice == '3':
                student_instance.view_requests(memPendReq_table)
                project_id = input("Enter the ProjectID to view details: ")
            elif choice == '4':
                student_instance.change_to_lead(random_id,memPendReq_table, project_table)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

elif val[1] == 'member':
    member_instance = Member(val[0], "MemberFirstName", "MemberLastName")
    while True:
        print("\n=== Member Menu ===")
        print("1. Modify Project Details")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            member_instance.modify_project(project_table)
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

elif val[1] == 'faculty':
    faculty_instance = NormalFaculty(val[0], "FacultyFirstName", "FacultyLastName")
    while True:
        print("\n=== Faculty Menu ===")
        print("1. Deny Advisor Request")
        print("2. View All Projects")
        print("3. Evaluate Project")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            project_id = input("Enter ProjectID to deny advisor request: ")
            faculty_instance.deny_to_serve_as_advisor(project_id, advisor_pending_request_table)
        elif choice == '2':
            faculty_instance.view_all_projects(project_table)
        elif choice == '3':
            project_id = input("Enter ProjectID to evaluate: ")
            faculty_instance.evaluate_project(project_id, project_table)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

elif val[1] == 'lead':
    lead_instance = Lead(val[0], "LeadFirstName", "LeadLastName")
    while True:
        print("\n=== Lead Menu ===")
        print("1. View Project Status")
        print("2. Modify Project Details")
        print("3. See Responded Requests")
        print("4. Send Requests")
        print("5. Request Advisor for Project")
        print("6. Create Project")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            project_id = input("Enter ProjectID to view status: ")
            lead_instance.project_status(project_id,project_table)
        if choice == '2':
            project_id = input("Enter ProjectID to modify details: ")
            changes = input("Enter modifications: ")
            lead_instance.modify_project(project_table)
        elif choice == '6':
            lead_instance.create_project(project_table, member_table)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

elif val[1] == 'advisor':
    advisor_instance = AdvisingFaculty(val[0], "AdvisorFirstName", "AdvisorLastName")
    while True:
        print("\n=== Advisor Menu ===")
        print("1. Request Supervisor")
        print("2. Deny Advisor Request")
        print("3. Accept Advisor Request")
        print("4. View All Projects")
        print("5. Evaluate Project")
        print("6. Approve Project")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            project_id = input("Enter ProjectID to deny advisor request: ")
            advisor_instance.deny_to_serve_as_advisor(project_id, advisor_pending_request_table)
        elif choice == '2':
            project_id = input("Enter ProjectID to accept advisor request: ")
            advisor_instance.accept_to_serve_as_advisor(project_id, advisor_pending_request_table)
        elif choice == '3':
            advisor_instance.view_all_projects(project_table)
        elif choice == '4':
            project_id = input("Enter ProjectID to evaluate: ")
            advisor_instance.evaluate_project(project_id, project_table)
        elif choice == '5':
            project_id = input("Enter ProjectID to approve: ")
            advisor_instance.approve_project(project_id, project_table)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

exit()

