from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str
    invitation_id: UUID
    created_at: datetime
