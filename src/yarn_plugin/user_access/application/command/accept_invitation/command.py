from dataclasses import dataclass


@dataclass(frozen=True)
class AcceptInvitationCommand:
    token: str
    password: str