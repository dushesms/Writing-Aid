from dataclasses import dataclass
from collections import OrderedDict

@dataclass
class SuggestCorrection:
    data: OrderedDict
    percentage_of_incorrect: float
