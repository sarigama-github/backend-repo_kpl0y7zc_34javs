from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, EmailStr

class Profile(BaseModel):
    name: str = Field(..., description="Full name")
    title: str = Field(..., description="Professional title")
    bio: str = Field(..., description="Short biography")
    location: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    links: Optional[dict] = Field(default_factory=dict)

class Skill(BaseModel):
    name: str
    level: str = Field(..., description="e.g., Beginner, Intermediate, Advanced, Expert")
    category: str = Field(..., description="e.g., Electronics, IT, Networking, DevOps")

class Project(BaseModel):
    name: str
    description: str
    tags: List[str] = Field(default_factory=list)
    repo: Optional[HttpUrl] = None
    demo: Optional[HttpUrl] = None

class Experience(BaseModel):
    company: str
    role: str
    start: str
    end: Optional[str] = "Present"
    summary: Optional[str] = None

class Education(BaseModel):
    school: str
    degree: str
    start: str
    end: str
    details: Optional[str] = None

class Message(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
