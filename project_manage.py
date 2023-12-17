from database import *
import random


def initializing():
    database_n = DB()

    read_person = ReadCSV('persons.csv')
    person = read_person.open_csv()
    person_table = Table('person', person)
    database_n.insert(person_table)

    read_login = ReadCSV('login.csv')
    login = read_login.open_csv()
    login_table = Table('login', login)
    database_n.insert(login_table)

    read_project = ReadCSV('project.csv')
    project = read_project.open_csv()
    project_table = Table('project',project)
    database_n.insert(project_table)

    read_member = ReadCSV('Member_pending_request.csv')
    member = read_member.open_csv()
    member_table = Table('Member_pending',member)
    database_n.insert(member_table)

    read_advisor = ReadCSV('Advisor_pending_request.csv')
    advisor = read_advisor.open_csv()
    advisor_table = Table('Advisor_pending',advisor)
    database_n.insert(advisor_table)

    return database_n


def login():
    data = initializing()
    list = data.search('login')
    username = input('Enter username: ')
    password = input('Enter password: ')
    id_role = []
    for user_info in list.data:
        if username == user_info['username'] and password == user_info['password']:
            id_role.extend([user_info['ID'], user_info['role']])
            return id_role
    return None


def exit():
    myFile_project = open('project.csv', 'w')
    myFile_advisor_pending = open('Advisor_pending_request.csv', 'w')
    myFile_login = open('login.csv', 'w')
    myFile_person = open('persons.csv', 'w')
    myFile_member_pending = open('Member_pending_request.csv', 'w')

    writer_project = csv.writer(myFile_project)
    writer_advisor = csv.writer(myFile_advisor_pending)
    writer_login = csv.writer(myFile_login)
    writer_person = csv.writer(myFile_person)
    writer_member = csv.writer(myFile_member_pending)

    writer_project.writerow(['ProjectID','Title','Lead','Member1','Member2','Advisor','Status'])
    writer_advisor.writerow(['ProjectID','to_be_advisor','Response','Response_date'])
    writer_person.writerow(['ID','fist','last','type'])
    writer_login.writerow(['ID','username','password','role'])
    writer_member.writerow(['ProjectID','to_be_member','Response','Response_date'])

    for dictionary in newdata.search('project').data:
        writer_project.writerow(dictionary.values())
    myFile_project.close()

    for dictionary in newdata.search('persons').data:
        writer_person.writerow(dictionary.values())
    myFile_person.close()

    for dictionary in newdata.search('login').data:
        writer_login.writerow(dictionary.values())
    myFile_login.close()

    for dictionary in newdata.search('Advisor_pending').data:
        writer_advisor.writerow(dictionary.values())
    myFile_advisor_pending.close()

    for dictionary in newdata.search('Member_pending').data:
        writer_member.writerow(dictionary.values())
    myFile_member_pending.close()


def generate_random_project_id():
    random_id = f"{random.randint(0, 99999):06d}"
    return random_id


class Student:
    def __init__(self):
        for i in newdata.search('Member_pending').data:
            self.ID = i['projectID']

    def view_requests(self):
        pending_requests = False
        for i in newdata.search('Member_pending').data:
            if val[0] == i['to_be_member']:
                pending_requests = True
                break
        if pending_requests:
            filtered_data = newdata.search('Member_pending').filter(lambda x: x['to_be_member'] == val[0])
            print(filtered_data)
        else:
            print('You dont have any invite')

    def accept_deny_request(self, request_id):
        choice = input("you want to accept or deny? ")
        if choice == 'accept':
            project_table = newdata.search('project')
            user_projects = project_table.filter(lambda x: x['ProjectID'] == self.ID).table
            for project in user_projects:
                if project['Member1'] == 'None':
                    member_key = 'Member1'
                elif project['Member2'] == 'None':
                    member_key = 'Member2'
                else:
                    print('This group is full')
                    break
            newdata.search('Member_pending').update_row('to_be_member', 'pending', 'to_be_member', 'accepted','to_be_member', val[0])
            newdata.search('login').update_row('role', 'student', 'role', 'member', 'ID', val[0])
            newdata.search('project').update_row(member_key, 'None', member_key, val[0], 'ProjectID', request_id)
        elif choice == 'deny':
            newdata.search('Member_pending').update_row('Response', 'pending', 'Response', 'deny', 'to_be_member', val[0])

    def change_to_lead(self):
        status = 'lead'
        newdata.search('login').update_row('role', 'student', 'role', status, 'ID', val[0])
        print(newdata.search('login'))
        print('Now your status is Lead')


class Lead:
    def __init__(self):
        projects_led_by_user = newdata.search('project').filter(lambda x: x['lead'] == val[0]).data
        if projects_led_by_user:
            project = projects_led_by_user[0]
            self.ID = project['ProjectID']
            self.status = project['status']
        else:
            self.ID = None
            self.status = None

    def create_project(self):
        project_name = input("Enter project name: ")
        project_id = generate_random_project_id()
        dct = {'ProjectID': generate_random_project_id(), 'Title': project_name, 'Lead': val[0], 'Member1': 'None', 'Member2': 'None',
                 'Advisor': 'None', 'status': 'None'}
        newdata.search('project').insert_row(dct)
        print(newdata.search('project'))
        print("NEW PROJECT CREATED")
        return project_id, project_name

    def sent_request(self):
        check = input('Want to request for advisor or member? ')
        if check == 'advisor':
            for project in newdata.search('project').filter(lambda x: x['ProjectID'] == self.ID).data:
                if project['Advisor'] != 'None':
                    print('Your group already has an advisor')
                elif project['Advisor'] == 'None':
                    print(newdata.search('login').filter(lambda x: x['role'] == 'faculty'))
                    faculty_id = int(input('Faculty(ID): '))
                    if any(invite['to_be_advisor'] == faculty_id for invite in newdata.search('advisor table').data):
                        print('You already sent an invitation to this faculty')
                    else:
                        date = input('Date/month/year: ')
                        dct_add = {'ProjectID': self.ID, 'to_be_advisor': faculty_id, 'Response': 'pending', 'Response_date': date}
                        newdata.search('Advisor_pending').insert_row(dct_add)
                        print(newdata.search('Advisor_pending'))
        if check == 'member':
            for project in newdata.search('project').filter(lambda x: x['ProjectID'] == self.ID).data:
                if project['Member1'] != 'None' and project['Member2'] != 'None':
                    print('Your group is full')
                elif project['Member1'] == 'None' or project['Member2'] == 'None':
                    print(newdata.search('login').filter(lambda x: x['role'] == 'student'))
                    student_id = int(input('Student(ID): '))
                    if any(invite['to_be_member'] == student_id for invite in newdata.search('Member_pending').data):
                        print('You already sent an invitation to this student')
                    else:
                        date = input('Date/month/year: ')
                        dict_mem = {'ProjectID': self.ID, 'to_be_member': student_id, 'Response': 'pending',
                                    'Response_date': date}
                        newdata.search('Member_pending').insert_row(dict_mem)

    def modify_project(self):
        project_name = input("Enter what you want to modify: ")
        newdata.search('project').update_row('status', self.status, 'status', project_name, 'ProjectID', self.ID)
        print('project has been updated')

    def project_status(self):
        project_info = newdata.search('project').filter(lambda x: x['ProjectID'] == self.ID).data
        print(project_info)

class Member:
    def __init__(self):
        projects_led_by_user = newdata.search('project').filter(lambda x: x['lead'] == val[0]).data
        if projects_led_by_user:
            project = projects_led_by_user[0]
            self.ID = project['ProjectID']
            self.status = project['status']
        else:
            self.ID = None
            self.status = None

    def modify_project(self):
        project_name = input("Enter what you want to modify: ")
        newdata.search('project').update_row('status', self.status, 'status', project_name, 'ProjectID', self.ID)
        print('project has been updated')

    def project_status(self):
        project_info = newdata.search('project').filter(lambda x: x['ProjectID'] == self.ID).data
        print(project_info)

class NormalFaculty:
    def __init__(self):
        advisor_pending_request = newdata.search('Advisor_pending').filter(lambda x: x['to_be_advisor'] == val[0]).table
        if advisor_pending_request:
            self.id = advisor_pending_request[0]['ProjectID']
        else:
            self.id = None

    def view_request(self):
        for i in newdata.search('Advisor_pending').data:
            if val[0] == i['to_be_advisor']:
                print(newdata.search('Advisor_pending').filter(lambda x: x['to_be_advisor'] == val[0]))
            elif val[0] != i['to_be_advisor']:
                print('You dont have any invite')

    def project_detail(self):
        print(newdata.search('project'))


    def accept_deny_to_serve_as_advisor(self,ID):
        choice = input('accept/deny: ')
        if choice == 'accept':
            newdata.search('Advisor_pending').update_row('to_be_advisor', 'pending', 'to_be_advisor', 'accepted',                                                       'ProjectID', ID)
            newdata.search('login').update_row('role', 'faculty', 'role', 'advisor', 'ID', val[0])
            newdata.search('project').update_row('Advisor', 'None', 'Advisor', val[0], 'ProjectID', ID)
        elif choice == 'deny':
            newdata.search('Advisor_pending').update_row('Response', 'pending', 'Response', 'deny', 'to_be_advisor',val[0])


class AdvisingFaculty:
    def __init__(self):
        projects_with_advisor = newdata.search('project').filter(lambda x: x['Advisor'] == val[0]).data
        if projects_with_advisor:
            project_info = projects_with_advisor[0]
            self.ID = project_info['ProjectID']
            self.status = project_info['status']
        else:
            self.ID = None
            self.status = None

    def update_status(self):
        status = input('what is your progress: ')
        newdata.search('project').update_row('status', self.status, 'status', status, 'ProjectID', self.ID)
        print('updated')

    def project_status(self):
        project_info = newdata.search('project').filter(lambda x: x['ProjectID'] == self.ID).data
        print(project_info)

    def approve(self):
        approve = input('You want to approve this project(yes/no)? ')
        if approve == 'yes':
            newdata.search('project').update_row('status', self.status, 'status', 'approve', 'ProjectID',
                                                     self.ID)
        elif approve == 'no':
            newdata.search('project').update_row('status', self.status, 'status', 'not_approve', 'ProjectID',
                                                     self.ID)
class Admin:
    pass

data = initializing()
newdata = copy.deepcopy(data)
val = login()
print(val)

if val[1] == 'student':
    student = Student()
    while True:
            print("\n=== Student Menu ===")
            print("1. View Pending Requests")
            print("2. Accept or Deny Requests")
            print("3. Change Role to Lead")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                student.view_requests()
            elif choice == '2':
                project_id = input('Enter projectID: ')
                student.accept_deny_request(project_id)
            elif choice == '3':
                student.change_to_lead()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

elif val[1] == 'member':
    member = Member()
    while True:
        print("\n=== Member Menu ===")
        print("1. Modify Project Details")
        print("2. See project status")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            member.modify_project()
        elif choice == '2':
            member.project_status()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
#
elif val[1] == 'faculty':
    faculty = NormalFaculty()
    while True:
        print("\n=== Faculty Menu ===")
        print("1. View Request")
        print("2. see projects detail")
        print("3. accept/deny to serve as advisor")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            faculty.view_request()
        elif choice == '2':
            faculty.project_detail()
        elif choice == '3':
            ID = input('Project[ID] to accept/deny: ')
            faculty.accept_deny_to_serve_as_advisor(ID)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
#
elif val[1] == 'lead':
    lead = Lead()
    while True:
        print("\n=== Lead Menu ===")
        print("1. Create project")
        print("2. Sent request for advisor or member")
        print("3. Modify project")
        print("4. Check project status")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            lead.create_project()
        if choice == '2':
            lead.sent_request()
        elif choice == '3':
            lead.modify_project()
        elif choice == '4':
            lead.project_status()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

elif val[1] == 'advisor':
    advisor = AdvisingFaculty()
    while True:
        print("\n=== Advisor Menu ===")
        print("1. Update status")
        print("2. Check project status")
        print("3. Aprrove project")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
           advisor.update_status()
        elif choice == '2':
            advisor.project_status()
        elif choice == '3':
            advisor.approve()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

exit()