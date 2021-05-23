import re
from threading import Thread

''' application modules '''
from Models import model
from Database.application_db import user_create, insert_file_detatils, check_process, login_check


''' Thread opration for operation to start '''
class Process(Thread):
    def __init__(self, file_property: model.File_Upload):
        Thread.__init__(self)
        self.__file_property = file_property

    def run(self):
        filename = self.__file_property.filename
        filepath = self.__file_property.path
        print("file path and name is {0} {1}",filepath,filename)

def _user_creation(_usermodel: model.User_Model) -> bool:
    return user_create(_usermodel)


def _login(login: model.Login) -> bool:
    return login_check(login)


def _file_upload(file_property: model.File_Upload) -> bool:

    insert_file_detatils(file_property)
    thread_a = Process(file_property)
    thread_a.start()

    return True


def _check_process(process_id):
    result = check_process(process_id=process_id)
    try:
        if result[0][6] == 1:
            ### to do for opencv task ###
            return "processed_image_path"
        else:
            return "running"
    except:
        return "invalide process id..."
