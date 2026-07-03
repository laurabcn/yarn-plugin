class InvitationExpired(Exception):
    def __init__(self) -> None:
        super().__init__("Invitation has expired")
