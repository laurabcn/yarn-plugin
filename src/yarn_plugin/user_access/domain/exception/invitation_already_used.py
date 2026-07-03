class InvitationAlreadyUsed(Exception):
    def __init__(self) -> None:
        super().__init__("Invitation has already been used")