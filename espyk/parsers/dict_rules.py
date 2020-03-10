from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction

from ..dictionnary_rules import *


class DictRulesLexer(Lexer):
    ignore = ' \t'
    ignore_comments = r'//.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # structural tokens
    REPLACE = r"\.replace"
    LETTER_GROUP = r"\.L[0-9]{2}"
    GROUP_HEADER = r"\.group"
    L_PAREN = r"\("
    R_PAREN = r"\)"

    # TODO : do smtng for B H F G Y
    # special characters
    def LANGUAGE_CODE(self, t: Token):
        t.value = LanguageCode(t.value[3:])
        return t
    BEGIN_END_WORD = r"_"
    HYPHEN = r"-"
    ANY_VOWEL = r"A"
    ANY_CONSONANT = r"C"

    LITERAL = r"\S+"


class DictRulesParser(Parser):

    @_("rule rules_list",
       "rule")
    def rules_list(self, p: YaccProduction):
        pass

    @_("replace",
       "group",
       "letter_group")
    def rule(self, p: YaccProduction):
        pass

    @_("literal literals_list",
       "literal")
    def literals_list(self, p: YaccProduction):
        pass

    @_("REPLACE substitutions_list")
    def replace(self, p: YaccProduction):
        pass

    @_("substitution substitutions_list",
       "substitution")
    def substitutions_list(self, p: YaccProduction):
        pass

    @_("LITERAL LITERAL")
    def substitution(self, p: YaccProduction):
        pass

    @_("LETTER_GROUP literals_list ")
    def letter_group(self, p: YaccProduction):
        pass

    @_("GROUP LITERAL rules_list ")
    def group(self, p: YaccProduction):
        pass

    @_("rule rules_list",
       "rule")
    def rules_list(self, p: YaccProduction):
        pass

    @_("pre LITERAL post LITERAL")
    def rule(self):
        pass

    @_("literals_list R_PAREN",
       "")
    def pre(self):
        pass

    @_("L_PAREN literals_list",
       "")
    def post(self):
        pass
