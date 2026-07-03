from dataclasses import dataclass


@dataclass(frozen=True)
class CreateInvitationCommand:
    email: str