from typing import Optional
from pydantic import BaseModel

class ScrapeSettings(BaseModel):
    pages_limit: Optional[int] = None
    proxy: Optional[str] = None
