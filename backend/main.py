from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware


from app.api import users, courses, grades
from app.db.db_setup import engine
from app.db.models import user, grade,course

user.Base.metadata.create_all(bind= engine)
grade.Base.metadata.create_all(bind= engine)
course.Base.metadata.create_all(bind= engine)

app = FastAPI(
    title= "Student Portal",
    description="Academic grade system to report students grades",
    version="0.0.1",
    contact={"name":"Developer","email":"itp23107@hua.gr"}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(grades.router)
# app.include_router(teachers.router)
# app.include_router(helpdesk.router)