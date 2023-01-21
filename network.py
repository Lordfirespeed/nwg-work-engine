from uuid import uuid4 as random_uuid


class Pipe:  # Edge
    def __init__(self) -> None:
        self.uuid = random_uuid()

    def __hash__(self) -> int:
        return hash(self.uuid)


class Junction:   # Node
    def __init__(self) -> None:
        self.uuid = random_uuid()

    def __hash__(self) -> int:
        return hash(self.uuid)
