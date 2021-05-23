from fastapi import FastAPI, Response, status, File, UploadFile
import os
import uuid
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, UJSONResponse

''' application modules '''
from Models import model
from Bussiness import bussiness

tags_metadata = [
    {
        "name": "Mantis Shrimp Web Console services",
        "description": "The web console for admins to access the MantisShrimp deep learning tool",
        "externalDocs": {"description": "Items external docs",
                         "url": "https://fastapi.tiangolo.com/", }
    }
]

app = FastAPI(
    # servers=[
    # {"url": "https://localhost", "description": "Staging environment"},
    # {"url": "https://localhost", "description": "Production environment"},],
    openapi_tags=tags_metadata,
    docs_url="/api_documentation", redoc_url=None)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get('/test-api')
async def hello():
    return "Application is running.."

@app.post("/create-user/",
          summary="Create an application user")
async def create_user(createuser: model.User_Model, response: Response):
    bussiness._user_creation(createuser)
    response.status_code = status.HTTP_201_CREATED
    return True


@app.post("/update-user/",
          summary="Update an application user details")
async def update_user(updateuser: model.Login, response: Response):
    response.status_code = status.HTTP_200_OK
    return True


@app.post("/delete-user/",
          summary="Delete an application user details")
async def delete_user(deleteuser: model.DeleteUser, response: Response):
    response.status_code = status.HTTP_200_OK
    return True


@app.post("/login",
          summary="User login route")
async def login(login: model.Login, response: Response):

    if bussiness._login(login=login):
        login_status = {"messgage": "User exist", "status": True}
    else:
        login_status = {"messgage": "User not exist", "status": False}

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(login_status), media_type="application/json")


@app.post("/logout",
          summary="User logout route")
async def login(logout: model.Logout, response: Response):
    response.status_code = status.HTTP_200_OK
    return True


@app.post("/upload-file/")
async def upload_file(response: Response, uploded_file: UploadFile = File(...)):
    os.mkdir("files")

    gui_id = uuid.uuid1().hex
    _file_name = gui_id+"__"+uploded_file.filename.replace(" ", "-")
    _file_name = _file_name.strip().lower()

    file_path = os.getcwd()+"/files/"+_file_name

    with open(file_path, 'wb+') as f:
        f.write(uploded_file.file.read())
        f.close()

    model.File_Upload.filename = _file_name
    model.File_Upload.path = file_path
    model.File_Upload.guid = gui_id
    response.status_code = status.HTTP_200_OK
    
    if bussiness._file_upload(model.File_Upload):
        return _file_name.split("__")[0]
    else:
        return ""


@app.get("/result/{process_id}")
async def check_presocess(process_id: str):
    return bussiness._check_process(process_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
