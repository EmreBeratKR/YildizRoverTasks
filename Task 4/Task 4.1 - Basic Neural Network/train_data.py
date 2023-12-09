from dataclasses import dataclass


@dataclass
class TrainData:
    inputs: list[int]
    output: int

    def __str__(self) -> str:
        return f"({self.inputs}: {self.output})"
