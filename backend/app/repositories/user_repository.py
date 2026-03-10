# app/repositories/user_repository.py
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.profile_model import Profile
from app.repositories.interfaces.i_user_repository import IUserRepository, IProfileRepository


class UserRepository(IUserRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def find_by_cpf(self, cpf: str) -> User | None:
        return self.db.query(User).filter(User.cpf == cpf).first()

    def find_all(self) -> list[User]:
        return self.db.query(User).order_by(User.name).all()

    def find_paginated(self, page: int, page_size: int) -> tuple[list[User], int]:
        query = self.db.query(User).order_by(User.name)
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def delete(self, user_id: UUID) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class ProfileRepository(IProfileRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_user_id(self, user_id: UUID) -> Profile | None:
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()

    def save(self, profile: Profile) -> Profile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile