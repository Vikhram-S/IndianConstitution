from typing import List, Optional, Union
from pydantic import BaseModel, Field

class Article(BaseModel):
    """Represents a single article in the Constitution."""
    number: Union[int, str] = Field(..., alias="article")
    title: str
    content: str = Field(..., alias="description")
    part: Optional[int] = None
    chapter: Optional[int] = None
    
    class Config:
        populate_by_name = True

class Part(BaseModel):
    """Represents a Part of the Constitution (group of articles)."""
    number: int
    title: str
    articles: List[Article] = []

class Schedule(BaseModel):
    """Represents a Schedule in the Constitution."""
    number: int
    title: str
    content: str

class ConstitutionData(BaseModel):
    """The full constitution data structure."""
    preamble: str
    articles: List[Article]
    parts: List[Part] = []
    schedules: List[Schedule] = []
