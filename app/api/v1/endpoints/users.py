from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud_user.create(db, obj_in=user_in)
    return user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/me", response_model=User)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user

@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete user.
    """
    if not crud_user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = crud_user.remove(db=db, id=user_id)
    return user