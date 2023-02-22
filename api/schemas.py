"""
Pydantic models ("schemas") to have common attributes while creating or reading data.
"""
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    """Pydantic model to have common attributes while creating or reading data.

    Args:
        BaseModel (class): class from pydantic
    """
    email: str

class UserCreate(UserBase):
    """Pydantic model that inherits from UserBase so that it will have the same attributes,
    plus any additional data (attributes) needed for creation.

    Args:
        UserBase (class): user base class
    """
    password: str

class UserPatch(UserBase):
    """Pydantic model that inherits from UserBase so that it will have the same attributes,
    plus any additional data (attributes) needed for creation.

    Args:
        UserBase (class): user base class
    """
    email: Optional[str]
    is_active: Optional[bool]

class UserPatchPassword(BaseModel):
    """Pydantic model that inherits from UserBase so that it will have the same attributes,
    plus any additional data (attributes) needed for creation.

    Args:
        UserBase (class): user base class
    """
    password: str

class UserUpdate(UserBase):
    """Pydantic model that inherits from UserBase so that it will have the same attributes,
    plus any additional data (attributes) needed for creation.

    Args:
        UserBase (class): user base class
    """
    email: str
    is_active: bool
    password: str

class UserLogin(UserBase):
    """Pydantic model that inherits from UserBase so that it will have the same attributes,
    plus any additional data (attributes) needed for creation.

    Args:
        UserBase (class): user base class
    """
    password: str

class User(UserBase):
    """Pydantic models (schemas) that will be used when reading data, when returning it from the API.

    Args:
        UserBase (class): user base class
    """
    id: int
    is_active: bool

    class Config:
        """
        Class used to provide configurations to Pydantic. Attribute orm_mode will tell the Pydantic
        model to read the data even if it is not a dict, but an ORM model (or any other arbitrary
        object with attributes).
        """
        orm_mode = True
