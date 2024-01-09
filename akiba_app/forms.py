from fastapi import Request
from typing import Optional, List

class RegisterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.firstname: Optional[str] = None
        self.lastname: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.firstname = form.get("firstname")
        self.lastname = form.get("lastname")
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.firstname or not self.lastname or not self.email:
            self.errors.append("Field is required")
        if not self.password or len(self.password) < 5:
            self.errors.append("A valid password is required (more than 4 characters)")
        if not self.errors:
            return True
        return False
    

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username:
            self.errors.append("Email is required")
        if not self.password:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False