from datetime import datetime
import uuid
from typing import Dict, Optional

from .schemas import UserCreate, UserRead

class UserStore:
    def __init__(self):
        self.users: Dict[str, UserRead] = {}
        self.emails: Dict[str, str] = {}
        self.usernames: Dict[str, str] = {}

    def create_user(self, user: UserCreate) -> UserRead:
        if user.email in self.emails:
            raise ValueError("Email already registered")
        if user.username in self.usernames:
            raise ValueError("Username already taken")
        
        user_id = str(uuid.uuid4())
        user_data = UserRead(
            id=user_id,
            email=user.email,
            username=user.username,
            created_at=datetime.now().replace(microsecond=0)
        )
        
        self.users[user_id] = user_data
        self.emails[user.email] = user_id
        self.usernames[user.username] = user_id
        
        return user_data

    def get_user(self, user_id: str) -> Optional[UserRead]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[UserRead]:
        user_id = self.emails.get(email)
        return self.users.get(user_id) if user_id else None

    def get_user_by_username(self, username: str) -> Optional[UserRead]:
        user_id = self.usernames.get(username)
        return self.users.get(user_id) if user_id else None

user_store = UserStore()