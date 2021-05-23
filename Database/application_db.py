from app import login
import configparser as cp
import os

''' application modules '''
from Database.db_utils import Database_Connection
from Models import model


''' database configuration parser and connections '''
parser = cp.SafeConfigParser()
parser.read(os.getcwd()+'\Database\db.ini')

''' GLOBAL QUERY STRING '''
user_exist = 'select name from user where name = "{0}";'  # parser.get('database_query_details', 'user_exist')
# parser.get('database_query_details', 'insert_new_user')
insert_new_user = 'insert into user (name,email_id,mobile_no,password,status) values ("{0}","{1}",{2},"{3}",True);'
# parser.get('database_query_details', 'login_user')
login_user = 'select name from user where name = "{0}" and password = "{1}";'
# parser.get('database_query_details', 'file_upload')
file_uploads = 'insert into result (process_id,file_name,file_path,status) values ("{0}","{1}","{2}",False);'
# parser.get('database_query_details', 'process_status')
process_status = 'select * from result where process_id = "{0}";'

''' user creation '''


def user_create(usermodel: model.User_Model):
    my_connection = Database_Connection()

    _user_exist = user_exist.format(usermodel.username)

    if len(my_connection._select_query(_user_exist)) == 0:
        _insert_new_user = insert_new_user.format(
            usermodel.username, usermodel.email, usermodel.mobileno, usermodel.password)
        my_connection._insert_query(_insert_new_user)
        my_connection._disconnect_database()


''' login flow '''


def login_check(model: model.Login) -> bool:
    my_connection = Database_Connection()

    _login_user = login_user.format(model.username, model.password)
    is_exist = len(my_connection._select_query(_login_user))
    my_connection._disconnect_database()

    if is_exist == 1:
        return True
    else:
        return False


def insert_file_detatils(file_property: model.File_Upload) -> bool:
    my_connection = Database_Connection()

    _file_upload = file_uploads.format(file_property.guid,
                                       file_property.filename, file_property.path)

    my_connection._insert_query(_file_upload)
    my_connection._disconnect_database()
    return True


def check_process(process_id: str):
    my_connection = Database_Connection()
    _process_status = process_status.format(process_id)

    result = my_connection._select_query(_process_status)
    return result
