import language_tool_python
from write_results import write_results
from nlprule import Tokenizer, Rules
from collections import OrderedDict

def compare(text1, text2):
    l1 = text1.split()
    l2 = text2.split()
    correct = 0
    incorrect = 0
    dict_of_incorrect = OrderedDict()
    for i in range(0, len(l2)):
        if l1[i] != l2[i]:
            incorrect += 1
            message = 'Error'
            dict_of_incorrect[l1[i]] = {'incorrect': l1[i],'correct': l2[i], 'position': i, 'message': message}
        else:
            correct += 1

    return (correct, incorrect), dict_of_incorrect


def nlp_rule_check(text):
    splitted_text = text.split()
    tokenizer = Tokenizer.load("en")
    rules = Rules.load("en", tokenizer)
    d = {}
    index = -1
    for s in rules.suggest(text):
        start = s.start
        end = s.end
        mistake_word = text[start:end]
        message = s.message
        correct = s.replacements[:2]
        for i in range(len(splitted_text)):
            if splitted_text[i].lower() == mistake_word.lower():
                index = i + 1
        d[mistake_word] = {'incorrect': mistake_word, 'correct': correct, 'position': index,
                           'message': message}
    return SuggestCorrection(
        data=d,
        percentage_of_incorrect=0
    )

def nlp_rule_print_results(text):
    result = nlp_rule_check(text)
    write_results(text, result.percentage_of_incorrect, result.data)

def grammar_check(text: str):
    tool = language_tool_python.LanguageTool( 'en-US' )
    splitted_text = text.split()
    is_bad_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and \
                               rule.replacements[0][0].isupper()
    matches = tool.check(text)
    matches = [rule for rule in matches if not is_bad_rule(rule)]

    d = OrderedDict()
    index = -1
    for match in matches:
        mistake_word = text[match.offset:match.offset + match.errorLength]
        message = match.message
        for i in range( len( splitted_text ) ):
            if splitted_text[i].lower() == mistake_word.lower():
                index = i + 1
        d[mistake_word] = {'incorrect': mistake_word, 'correct': match.replacements[:2], 'position': index,
                           'message': message}
    return SuggestCorrection(
        data=d,
        percentage_of_incorrect=0
    )


def grammar_check_with_print_result(text: str):
    result = grammar_check(text)
    write_results(text, result.percentage_of_incorrect, result.data)


