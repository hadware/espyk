from typing import Optional

from sly import Lexer, Parser


class PhonemeSourceTableLexer(Lexer):


    tokens = {

    }
    # ignoring whitespace and comments
    ignore = ' \t'
    ignore_comments = r'//.*'

    # table declaration and include literals
    PHONEMETABLE = r"phonemetable"
    INCLUDE = r"include"

    # phoneme declarations literals
    PHONEME_START = r"phoneme"
    PHONEME_END = r"endphoneme"

    L_PAREN = r"\("
    R_PAREN = r"\)"

    # instructions conditional keywords
    IF = r"IF"
    THEN = r"THEN"
    ELSE = r"ELSE"
    ELIF = r"ELIF"
    ENDIF = r"ENDIF"

    # instruction statements
    FORMANTS = r"FMT"
    CALL = r"CALL"
    WAV = r"WAV"
    RETURN = r"RETURN"
    PHONEME_CHANGE = r"(ChangePhoneme|ChangeIfDiminished|ChangeIfUnstressed|" \
                     r"ChangeIfNotStressed|ChangeIfStressed|IfNextVowelAppend)"
    VOWEL_TRANSITIONS = r"(Vowelin|Vowelout)"
    VOWEL_MODIFICATIOn = r"(VowelStart|VowelEnding)"
    PROP_LENGTH = r"length"
    PROP_IPA = r"ipa"

    # conditions keywords
    CONDITION = r"(thisPh|prevPh|prevPhW|prev2PhW|nextPh|next2Ph|nextPhW|" \
                 r"next2PhW|next3PhW|nextVowel|prevVowel|PreVoicing|KlattSynth)"

    # attributes keywords (used in conditions)
    ATTRIBUTE = r"(isPause|isPause2|isVowel|isNotVowel|isLiquid|isNasal|" \
                r"isVFricative|isPalatal|isRhotic|isWordStart|notWordStart|" \
                r"isWordEnd|isFirstVowel|isSecondVowel|isFinalVowel|" \
                r"isAfterStress|isVoiced|isDiminished|isUnstressed|" \
                r"isNotStressed|isStressed|isMaxStress)"

    # static properties
    PROPERTIES = r"(pause|nopause|stress|unstressed|liquid)" # TODO add all
    PROP_LENGTHMOD = r"lengthmod"
    PROP_STARTTYPE = r"starttype"
    PROP_ENDTYPE = r"endtype"

    LITERAL = r"\S+"

    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += len(t.value)
        return t


class PhonemeSourceTableParser(Parser):
    """Parses phoneme source files (definitions and prononciation rules
    for all phonemes)"""

    def __init__(self, for_root: bool, table: Optional[str] = None):
        self.for_root = True
        self.table = table

    def parse(self, table_name: str):
        pass

