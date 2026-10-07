"""Business logic for user registration and authentication."""
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import AlreadyExistsError, InvalidCredentialsError


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, email: str, full_name: str, password: str) -> User:
        """Create a new user, raising if the email is already taken."""
        if self.repo.get_by_email(email):
            raise AlreadyExistsError("User", "email", email)

        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
        )
        return self.repo.create(user)

    def authenticate(self, email: str, password: str) -> str:
        """Verify credentials and return a signed access token."""
        user = self.repo.get_by_email(email)
        if not user or not user.is_active or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
        return create_access_token(subject=str(user.id))

    def get_by_id(self, user_id: int) -> User | None:
        return self.repo.get(user_id)
