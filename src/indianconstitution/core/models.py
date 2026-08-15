"""Pydantic v2 data models for the Constitution of India.

All public models are fully typed, serializable, and validated on construction.
"""

import re
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


def infer_part(number: str) -> Optional[int]:
    """Infer the Part number (1..22) for a given article number."""
    m = re.match(r"^(\d+)", str(number).strip())
    if not m:
        return None
    num = int(m.group(1))
    if 1 <= num <= 4:
        return 1
    elif 5 <= num <= 11:
        return 2
    elif 12 <= num <= 35:
        return 3
    elif 36 <= num <= 51:
        return 4
    elif 52 <= num <= 151:
        return 5
    elif 152 <= num <= 237:
        return 6
    elif num == 238:
        return 7
    elif 239 <= num <= 242:
        return 8
    elif num == 243:
        return 9
    elif num == 244:
        return 10
    elif 245 <= num <= 263:
        return 11
    elif 264 <= num <= 300:
        return 12
    elif 301 <= num <= 307:
        return 13
    elif 308 <= num <= 323:
        return 14
    elif 324 <= num <= 329:
        return 15
    elif 330 <= num <= 342:
        return 16
    elif 343 <= num <= 351:
        return 17
    elif 352 <= num <= 360:
        return 18
    elif 361 <= num <= 367:
        return 19
    elif num == 368:
        return 20
    elif 369 <= num <= 392:
        return 21
    elif 393 <= num <= 395:
        return 22
    return None


class Article(BaseModel):
    """Represents a single article in the Constitution.

    Attributes:
        number: The article number (e.g. '14', '21A').
        title: The title or short description of the article.
        content: The full text / description of the article.
        part: The Part number this article belongs to (inferred if None).
        chapter: The Chapter number within the Part, if any.
    """

    number: str = Field(..., alias="article")
    title: str
    content: str = Field(..., alias="description")
    part: Optional[int] = None
    chapter: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    @model_validator(mode="after")
    def populate_part(self) -> "Article":
        """Auto-populate part if missing."""
        if self.part is None:
            self.part = infer_part(self.number)
        return self

    @property
    def text(self) -> str:
        """Alias for ``content`` — provides compatibility with README examples."""
        return self.content


class SearchResult(BaseModel):
    """An article paired with a relevance score from semantic search.

    Attributes:
        number: The article number.
        title: The article title.
        content: Full article text.
        score: Similarity / relevance score (0.0 – 1.0).
        part: Part number, if any.
        chapter: Chapter number, if any.
    """

    number: str
    title: str
    content: str
    score: float = 0.0
    part: Optional[int] = None
    chapter: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True)

    @property
    def text(self) -> str:
        """Alias for ``content``."""
        return self.content

    @classmethod
    def from_article(cls, article: "Article", score: float = 0.0) -> "SearchResult":
        """Construct a ``SearchResult`` from an ``Article`` and a score."""
        return cls(
            number=article.number,
            title=article.title,
            content=article.content,
            score=score,
            part=article.part,
            chapter=article.chapter,
        )


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


class CaseLaw(BaseModel):
    """Represents a landmark Supreme Court judgment linked to an article.

    Attributes:
        case_name: Title of the landmark case.
        year: Year of the judgment.
        holding: A concise summary of the court's holding.
        article_number: Article number (e.g. '21', '368').
        citation: Official citation string, if available.
        bench: Bench size or description, if available.
    """

    case_name: str
    year: int
    holding: str
    article_number: str
    citation: Optional[str] = None
    bench: Optional[str] = None


class AmendmentEvent(BaseModel):
    """Represents an amendment event affecting an article.

    Attributes:
        amendment_number: Amendment name/number (e.g. '86th Amendment Act').
        year: Year of enactment.
        title: Short title of the change.
        description: Description of textual/structural alterations.
        article_number: Target article number (e.g. '21A').
        text_before: Optional text before the amendment.
        text_after: Optional text after the amendment.
    """

    amendment_number: str
    year: int
    title: str
    description: str
    article_number: str
    text_before: Optional[str] = None
    text_after: Optional[str] = None


class DutyCrossReference(BaseModel):
    """Cross-reference linking a Fundamental Right to a Fundamental Duty.

    Attributes:
        right_article: Article number of the Fundamental Right (e.g. '21A').
        duty_clause: Clause in Article 51A (e.g. '51A(k)').
        duty_text: Summary of the fundamental duty.
        rationale: Legal/civic relationship rationale.
    """

    right_article: str
    duty_clause: str
    duty_text: str
    rationale: str
