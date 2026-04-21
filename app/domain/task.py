from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class GithubTask:
    repo: str
    since: datetime

    status: str = "pending"   # pending / running / done / failed / skipped
    result: Optional[str] = None
    error: Optional[str] = None

    raw_file: Optional[str] = None
    report_file: Optional[str] = None
