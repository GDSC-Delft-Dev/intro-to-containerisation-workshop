"""
This file we has reusable functions to interact with the data in the database.
CRUD comes from: Create, Read, Update, and Delete.
"""
from typing import Dict
from sqlalchemy.orm import Session, Query
from models import User
from schemas import UserCreate


def hash_password(password: str) -> str:
    return password + "not_really_hashed"

def get_user(db: Session, user_id: int) -> Query[User]:
    """Finds a user by id.

    Args:
        db (Session): database session that manages persistence operations for ORM-mapped objects
        user_id (int): user id

    Returns:
        Query[User]: query result object
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Query[User]:
    """Finds a user by email.

    Args:
        db (Session): database session that manages persistence operations for ORM-mapped objects
        email (str): email of the user

    Returns:
        Query[User]: query result object
    """
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> Query[User]:
    """Gets all users in a certain range.

    Args:
        db (Session): database session that manages persistence operations for ORM-mapped objects
        skip (int, optional): number of items to skip from a list of all users. Defaults to 0.
        limit (int, optional): _description_. Defaults to 100.

    Returns:
        Query[User]: query result object
    """
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user.

    Args:
        db (Session): database session that manages persistence operations for ORM-mapped objects
        user (UserCreate): Create user schema

    Returns:
        User: user object
    """
    fake_hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User) -> User:
    """Update an existing user's data.

    Args:
        db (Session): database session that manages persistence operations for ORM-mapped objects
        user (User): update user schema

    Returns:
        User: user object
    """
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User) -> User:
    """Delete an existing user.

    Args:
        db (Session): database session that manages persistence operations for ORM-mapped objects
        user (Dict): user to delete
    """
    user = db.query(User).filter(User.id == db_user.id).first()
    db.delete(user)
    return user
