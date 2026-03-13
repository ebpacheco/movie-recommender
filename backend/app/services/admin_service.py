# app/services/admin_service.py
import math
from uuid import UUID

from fastapi import HTTPException, status

from app.models.user_model import User, UserRole
from app.repositories.interfaces.i_user_repository import IUserRepository


class AdminService:

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def list_all(self) -> list[User]:
        return self.user_repo.find_all()

    def list_paginated(self, page: int, page_size: int) -> dict:
        items, total = self.user_repo.find_paginated(page, page_size)
        return {
            "items": items,
            "total": total,
            "page":  page,
            "pages": max(1, math.ceil(total / page_size)),
        }

    def update_role(self, user_id: UUID, role: UserRole) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        user.role = role
        return self.user_repo.save(user)

    def update_user(self, user_id: UUID, data) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        existing = self.user_repo.find_by_email(data.email)
        if existing and existing.id != user_id:
            raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já em uso por outro usuário")
        user.name  = data.name
        user.email = data.email
        user.role  = data.role
        return self.user_repo.save(user)

    def delete_user(self, user_id: UUID) -> None:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        self.user_repo.delete(user_id)
