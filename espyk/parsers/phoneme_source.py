from typing import Optional

from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction


class VowelTransitionLexer(Lexer):
    tokens = {
        'LEN', 'LENADD', 'RATE', 'RMS', 'GLOTAL_STOP',
        'FORMANT', 'EQUAL', 'INTEGER'
    }

    ignore_whitespace = "\s+"

    LENADD = r"lenadd"
    LEN = r"len"
    RATE = r"rate"
    RMS = r"rms"
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
        'PHONEMETABLE' 'INCLUDE', 'PROCEDURE_START', 'PROCEDURE END',
        'PHONEME_START', 'PHONEME_END', 'L_PAREN', 'R_PAREN', 'COMMA',
        'TYPE', 'FEATURE', 'LENGTHMOD', 'STARTYPE', 'ENDTYPE',
        'IF', 'THEN', 'ELSE', 'ELIF', 'ENDIF', 'OR', 'AND', 'NOT',
        'FORMANTS', 'CALL', 'WAV', 'ADD_WAV', 'RETURN', 'PHONEME_CHANGE',
        'VOWEL_TRANSITION', 'VOWEL_MODIFICATION', 'NEXT_VOWEL_SWITCH',
        'ENDSWITCH', 'LENGTH', 'IPA', 'CONDITION', 'NOARG_CONDITION',
        'ATTRIBUTE', 'LITERAL'
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
    PROCEDURE_START = r"procedure"
    PROCEDURE_END = r"endprocedure"

    # phoneme declarations literals
    PHONEME_START = r"phoneme"
    PHONEME_END = r"endphoneme"

    L_PAREN = r"\("
    R_PAREN = r"\)"
    COMMA = r","

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
                     r"ChangeIfNotStressed|ChangeIfStressed|IfNextVowelAppend|" \
                     r"IfNextVowelAppend)"
    VOWEL_TRANSITIONS = r"(Vowelin|Vowelout)"
    VOWEL_MODIFICATION = r"(VowelStart|VowelEnding)"
    NEXT_VOWEL_SWITCH = r"r(NextVowelStarts|PrevVowelEndings)"
    ENDWSITCH = r"EndSwitch"
    LENGTH = r"length"
    IPA = r"ipa"

    # conditions keywords
    CONDITION = r"(thisPh|prevPh|prevPhW|prev2PhW|nextPh|next2Ph|nextPhW|" \
                r"next2PhW|next3PhW|nextVowel|prevVowel"
    NOARG_CONDITION = r"(PreVoicing|KlattSynth)"

    # attributes keywords (used in conditions)
    ATTRIBUTE = r"(isPause|isPause2|isVowel|isNotVowel|isLiquid|isNasal|" \
                r"isVFricative|isPalatal|isRhotic|isWordStart|notWordStart|" \
                r"isWordEnd|isFirstVowel|isSecondVowel|isFinalVowel|" \
                r"isAfterStress|isVoiced|isDiminished|isUnstressed|" \
                r"isNotStressed|isStressed|isMaxStress)"

    # either a string or a number, can be used for some literal value or
    # for a phoneme's name. Has to be kept here at the end,
    # else will match everything
    LITERAL = r"\S+"


class PhonemeSourceTableParser(Parser):
    """Parses phoneme source files (definitions and prononciation rules
    for all phonemes)"""
    tokens = PhonemeSourceTableLexer.tokens

    def __init__(self, for_root: bool, table: Optional[str] = None):
        self.for_root = True
        self.table = table

        # todo: depending on for_root, the starter rule is to be different

    def parse(self, table_name: str):
        pass

    @_("block blocks_list",
       "block")
    def blocks_list(self, p: YaccProduction):
        pass

    @_("PHONEMETABLE LITERAL LITERAL blocks_list")
    def block(self, p: YaccProduction):
        pass

    @_("PHONEME_START phoneme_body PHONEME_END")
    def block(self, p: YaccProduction):
        pass

    @_("INCLUDE LITERAL")
    def block(self, p: YaccProduction):
        pass

    @_("PROCEDURE_START instructions_list PROCEDURE_END")
    def block(self, p: YaccProduction):
        pass

    @_("instruction instructions_list",
       "intruction")
    def instructions_list(self, p: YaccProduction):
        pass

    @_("LITERAL literals_list",
       "LITERAL")
    def literals_list(self, p: YaccProduction):
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

    @_("VOWEL_TRANSITIONS literals_list")
    def instruction(self, p: YaccProduction):
        pass

    @_("VOWEL_MODIFICATION L_PAREN LITERAL R_PAREN",
       "VOWEL_MODIFICATION L_PAREN LITERAL COMMA LITERAL R_PAREN")
    def instruction(self, p: YaccProduction):
        pass

    @_("NEXT_VOWEL_SWITCH vowel_mod_list ENDWSITCH")
    def instruction(self, p: YaccProduction):
        pass

    @_("VOWEL_MODIFICATION vowel_mod_list",
       "VOWEL_MODIFICATION")
    def vowel_mod_list(self, p: YaccProduction):
        pass

    @_("conditional_statement")
    def instruction(self, p: YaccProduction):
        pass

    @_("if_branch elif_list else_branch ENDIF")
    def conditional_statement(self, p: YaccProduction):
        pass

    @_("IF conditions THEN instructions_list")
    def if_branch(self, p: YaccProduction):
        pass

    @_("ELSE instructions_list")
    def else_branch(self, p: YaccProduction):
        pass

    @_("ELIF conditions THEN instructions_list")
    def elif_branch(self, p: YaccProduction):
        pass

    @_("elif_branch elif_list",
       "elif_branch",
       "")
    def elif_list(self, p: YaccProduction):
        pass

    @_("conditional_statement OR conditions",
       "conditional_statement AND conditions",
       "conditional_statement")
    def conditions(self, p: YaccProduction):
        pass

    @_("condition",
       "NOT condition")
    def conditional_statement(self, p: YaccProduction):
        pass

    @_("CONDITION L_PAREN ATTRIBUTE R_PAREN",
       "NOARG_CONDITION")
    def condition(self, p: YaccProduction):
        pass