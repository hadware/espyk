from typing import Optional

from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction


class VowelTransitionLexer(Lexer):
    tokens = {
        'LEN', 'RATE', 'RMS', 'GLOTAL_STOP', 'FORMANT', 'EQUAL', 'INTEGER'
    }

    ignore_whitespace = "\s+"

    LEN = r"len"
    RATE = r"rate"
    RMS = r"rate"
    GLOTAL_STOP = r"glstop"
    FORMANT = r"f[1-4]"
    EQUAL = "="

    @_(r"-?[0-9]+")
    def INTEGER(self, t: Token):
        t.value = int(t.value)
        return t


class VowelTransitionParser(Parser):
    tokens = VowelTransitionLexer.tokens
    lexer = VowelTransitionLexer()

    def parse(self, text: str):
        return super().parse(self.lexer.tokenize(text))


class PhonemeSourceTableLexer(Lexer):
    tokens = {

    }
    # ignoring whitespace and comments
    ignore = ' \t'
    ignore_comments = r'//.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # table declaration and include literals
    PHONEMETABLE = r"phonemetable"
    INCLUDE = r"include"

    # procedure declaration
    PROCEDURE = r"procedure"
    PROCEDURE_END = r"endprocedure"

    # phoneme declarations literals
    PHONEME_START = r"phoneme"
    PHONEME_END = r"endphoneme"

    L_PAREN = r"\("
    R_PAREN = r"\)"
    COMMA = r","

    # instructions conditional keywords
    IF = r"IF"
    THEN = r"THEN"
    ELSE = r"ELSE"
    ELIF = r"ELIF"
    ENDIF = r"ENDIF"
    OR = r"OR"
    AND = r"AND"
    NOT = r"NOT"

    # instruction statements
    FORMANTS = r"FMT"
    CALL = r"CALL"
    WAV = r"WAV"
    ADD_WAV = r"addWav"
    RETURN = r"RETURN"
    PHONEME_CHANGE = r"(ChangePhoneme|ChangeIfDiminished|ChangeIfUnstressed|" \
                     r"ChangeIfNotStressed|ChangeIfStressed|IfNextVowelAppend)"
    VOWEL_TRANSITIONS = r"(Vowelin|Vowelout)"
    VOWEL_MODIFICATIOn = r"(VowelStart|VowelEnding)"
    LENGTH = r"length"
    IPA = r"ipa"

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
    TYPE = r"(pause|nopause|stress|unstressed|liquid|rhotic|trill|virtual)"
    FEATURE = r"(nas|stp|afr|frc|flp|trl|apr|clk|ejc|imp|vwl|lat|sib|blb|lbd|" \
              r"bld|dnt|alv|pla|rfx|alp|pal|vel|lbv|uvl|phr|glt|vcd|vls|hgh|" \
              r"smh|umd|mid|lmd|sml|low|fnt|cnt|bck|unr|rnd|lgl|idt|apc|lmn|" \
              r"egs|igs|brv|slv|stv|crv|glc|ptr|cmp|mrd|lrd|syl|nsy|asp|nrs|" \
              r"lrs|unx|pzd|vzd|fzd|nzd|rzd|atr|rtr|fts|lns|est|hlg|lng|elg)"
    LENGTHMOD = r"lengthmod"
    STARTTYPE = r"starttype"
    ENDTYPE = r"endtype"

    # either a string or a number, can be used for some literal value or
    # for a phoneme's name
    LITERAL = r"\S+"


class PhonemeSourceTableParser(Parser):
    """Parses phoneme source files (definitions and prononciation rules
    for all phonemes)"""

    def __init__(self, for_root: bool, table: Optional[str] = None):
        self.for_root = True
        self.table = table

    def parse(self, table_name: str):
        pass

    @_("PHONEMETABLE LITERAL LITERAL table_body")
    def phonemetable(self, p: YaccProduction):
        pass

    @_("INCLUDE LITERAL")
    def table_body(self, p: YaccProduction):
        pass

    # TODO : add procedures
    @_("table_body phoneme_definition",
       "phoneme_definition")
    def table_body(self, p: YaccProduction):
        pass

    @_("PHONEME_START phoneme_body PHONEME_END")
    def phoneme_definition(self, p: YaccProduction):
        pass

    @_("phoneme_body phoneme_property",
       "phoneme_property")
    def phoneme_body(self, p: YaccProduction):
        pass

    @_("static_property")
    def phoneme_property(self, p: YaccProduction):
        pass

    @_("instruction")
    def phoneme_property(self, p: YaccProduction):
        pass

    @_("FEATURE")
    def static_property(self, p: YaccProduction):
        pass

    @_("TYPE")
    def static_property(self, p: YaccProduction):
        pass

    @_("LENGTHMOD LITERAL")
    def static_property(self, p: YaccProduction):
        pass

    @_("STARTYPE LITERAL",
       "ENDTYPE LITERAL")
    def static_property(self, p: YaccProduction):
        pass

    @_("LENGTH LITERAL")
    def instruction(self, p: YaccProduction):
        pass

    @_("IPA LITERAL")
    def instruction(self, p: YaccProduction):
        pass

    @_("CALL LITERAL")
    def instruction(self, p: YaccProduction):
        pass

    @_("RETURN")
    def instruction(self, p: YaccProduction):
        pass

    @_("FMT L_PAREN LITERAL R_PAREN",
       "FMT L_PAREN LITERAL R_PAREN add_wav")
    def instruction(self, p: YaccProduction):
        pass

    @_("ADD_WAV L_PAREN LITERAL R_PAREN",
       "ADD_WAV L_PAREN LITERAL COMMA LITERAL R_PAREN")
    def add_wav(self, p: YaccProduction):
        pass

    @_("WAV L_PAREN LITERAL R_PAREN",
       "WAV L_PAREN LITERAL COMMA LITERAL R_PAREN")
    def instruction(self, p: YaccProduction):
        pass

    @_("conditional_statement")
    def instruction(self, p: YaccProduction):
        pass

    @_("if_branch elif_list else_branch ENDIF")
    def conditional_statement(self, p: YaccProduction):
        pass

    @_("IF conditions THEN instructions")
    def if_branch(self, p: YaccProduction):
        pass

    @_("ELSE instructions")
    def else_branch(self, p: YaccProduction):
        pass

    @_("ELIF conditions THEN instructions")
    def elif_branch(self, p: YaccProduction):
        pass

    @_("elif_branch elif_list",
       "elif_branch",
       "")
    def elif_list(self, p: YaccProduction):
        pass

    @_("conditions_and_list",
       "condition_or_list",
       "conditional_statement")
    def conditions(self, p: YaccProduction):
        pass

    @_("NOT condition",
       "condition")
    def conditional_statement(self, p: YaccProduction):
        pass