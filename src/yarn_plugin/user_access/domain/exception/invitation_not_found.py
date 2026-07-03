class InvitationNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Invitation not found")
