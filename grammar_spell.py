import logging
from typing import List
import streamlit
from Spell_check import spell_check_js, spell_check_norvig, spell_check_enchant
from domain import SuggestCorrection
from grammar_check import grammar_check
from grammar_check import nlp_rule_check
from utils import percentage_of_incorrect
from write_results import write_results
from collections import OrderedDict

logger = logging.getLogger(__name__)

def _calculate_actual_percentage_of_incorrect(text:str, mistake_keys: List[str]) -> float:
    text_keys = text.split()
    errors_count = len(mistake_keys)
    text_keys_without_error_count = len(text_keys) - errors_count

    return percentage_of_incorrect(text_keys_without_error_count, errors_count)


def example_check(text: str):
    # spell_enchant_result = spell_check_enchant(text)
    # spell_norvig_result = spell_check_norvig(text)

    # grammar_result = grammar_check(text)
    # spell_jamspell_result = spell_check_js(text)
    # nlp_rule_result = nlp_rule_check(text)
    suggestions_data = OrderedDict()
    checkers = [
        grammar_check,
        spell_check_enchant,
        nlp_rule_check
    ]
    attempt_check_count = len(checkers)

    for checker in [
        grammar_check,
        spell_check_enchant,
        nlp_rule_check
    ]:
        try:
            result = checker(text)
            suggestions_data.update(result.data)
        except Exception as error:
            logger.error("Something is going wrong...", exc_info=error)
            attempt_check_count -= 1
            pass

    if attempt_check_count:
        result = SuggestCorrection(
            data=suggestions_data,
            percentage_of_incorrect=_calculate_actual_percentage_of_incorrect(text, suggestions_data.keys())
        )
        write_results(text, result.percentage_of_incorrect, result.data)
    else:
        streamlit.write("Sorry, temporary unavailable")
