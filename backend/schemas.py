from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# Each model corresponds to one MongoDB collection (collection name = class name lowercased)

class Profile(BaseModel):
    name: str
    title: str
    bio: str
    location: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    socials: Optional[dict] = None  # {"github": "", "linkedin": "", ...}

class Skill(BaseModel):
    category: str  # e.g., "Elektronik" or "IT"
    name: str
    level: Optional[int] = Field(default=None, ge=1, le=5)  # 1..5

class Project(BaseModel):
    title: str
    description: str
    tags: List[str] = []
    link: Optional[str] = None
    image: Optional[str] = None

class Experience(BaseModel):
    company: str
    role: str
    start: str  # YYYY-MM
    end: Optional[str] = None  # YYYY-MM or "Present"
    summary: Optional[str] = None

class Education(BaseModel):
    school: str
    degree: str
    start: str
    end: Optional[str] = None

class Message(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
