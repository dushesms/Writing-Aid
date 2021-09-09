from dataclasses import dataclass
from typing import Dict, List


class CorrectionType(Dict):
    correct: List[str]
    position: int


@dataclass
class SuggestCorrection:
    data: Dict[str, CorrectionType]
    percentage_of_incorrect: float
