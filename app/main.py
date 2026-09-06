from fastapi import FastAPI, Depends
from app.models.user_model import UserResponse
from app.services.user_service import UserService

app = FastAPI()


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, service: UserService = Depends()):
    return service.fetch_user_data(user_id)
