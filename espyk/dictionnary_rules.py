from dataclasses import dataclass

class AbstractRuleChar:
    pass

@dataclass
class LanguageCode(AbstractRuleChar):
    lang: str

class AnyVowel(AbstractRuleChar):
    pass

class AnyConsonnant(AbstractRuleChar):
    pass

class WordBoundary(AbstractRuleChar):
    pass

class Hyphen(AbstractRuleChar):
    pass

