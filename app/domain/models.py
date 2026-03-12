from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class NoteMark:
    id: int
    timestamp: datetime
    time_len: float
    text: str


@dataclass
class ProblemMark:
    id: int
    timestamp: datetime
    time_len: float
    text: str


@dataclass
class Lecture:
    id: int
    title: str
    audio_record_url: Optional[str] = None
    text: Optional[str] = None
    conspect_url: Optional[str] = None
    notes: List[NoteMark] = field(default_factory=list)
    problems: List[ProblemMark] = field(default_factory=list)

