from app.models.user_model import UserResponse


class UserService:
    def fetch_user_data(self, user_id: int) -> UserResponse:
        # Construct and validate Pydantic response object
        return UserResponse(
            user_id=user_id,
            username="dev_user",
            email="dev@example.com"
        )
