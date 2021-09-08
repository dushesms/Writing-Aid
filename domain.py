from dataclasses import dataclass
from typing import TypedDict, Dict, List


class CorrectionType(TypedDict):
    correct: List[str]
    position: int


@dataclass
class SuggestCorrection:
    data: Dict[str, CorrectionType]
    percentage_of_incorrect: float
