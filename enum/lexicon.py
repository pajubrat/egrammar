from phrase_structure import PhraseStructure

# Lexicon with the following features
# !COMP: mandatory complement
# -COMP: illicit complement
# !SPEC: mandatory specifier
# -SPEC: illicit specifier
# EPP: standard EPP triggering A-movement
# #X: bound morpheme
# WH: Wh-operator feature
# SCOPE: Scope marking element for operators
# + major lexical categories
lexicon = {'a': {'a', 'f1', 'f2'},
           'b': {'b', 'f3', 'f4'},
           'c': {'c', 'f5', 'f6'},
           'd': {'d', 'f7', 'f8'},
           'the': {'D'},
           'dog': {'N'},
           'bark': {'V', 'V/INTR'},
           'barks': {'V', 'V/INTR'},
           'ing': {'N', '!wCOMP:V', 'PC:#X', 'ε'},
           'bites': {'V', '!COMP:D', '!SPEC:D'},
           'bite': {'V', '!COMP:D'},
           'bite*': {'V', 'V/TR'},
           'which': {'D', 'WH'},
           'man': {'N'},
           'angry': {'A', 'α:N', 'λ:L'},
           'frequently': {'Adv', 'α:V', 'λ:R'},
           'city': {'N'},
           'from': {'P'},
           'in': {'P', 'α:V', },
           'ed': {'T', 'PC:#X', '!wCOMP:V', '-ε'},
           'T': {'T', 'PC:#X', 'EPP', '!SPEC:D', '!wCOMP:V', '-ε'},
           'T*': {'T', 'PC:#X', '!wCOMP:V', '-ε'},
           'did': {'T', 'EPP'},
           'does': {'T'},
           'was': {'T', 'EPP'},
           'C': {'C', 'PC:#X', '!wCOMP:T', '-ε'},
           'C(wh)': {'C', 'C(wh)', 'PC:#X', '!wCOMP:T', '-ε', 'WH', 'SCOPE'},
           'v': {'v', 'PC:#X', '!wCOMP:V', '-ε'},
           'v*': {'V', 'EPP', 'PC:#X', '!COMP:V', '-SPEC:v', '!wCOMP:V', '-ε'},
           'that': {'C'},
           'believe': {'V', '!COMP:C'},
           'seem': {'V', 'EPP', '!SPEC:D', '!COMP:T/inf', 'RAISING'},
           'to': {'T/inf', '!COMP:V', '-COMP:RAISING', '-COMP:T', 'EPP'}}

lexical_redundancy_rules = {'D': {'!COMP:N', '-COMP:Adv', '-SPEC:C', '-SPEC:T', '-SPEC:N', '-SPEC:V', '-SPEC:D', '-SPEC:P', '-SPEC:T/inf', '-SPEC:Adv'},
                            'V': {'-SPEC:C', '-SPEC:N', '-SPEC:T', '-SPEC:T/inf', '-COMP:A', '-COMP:N', '-COMP:T'},
                            'Adv': {'-COMP:D', '-COMP:N', '-SPEC:V', '-SPEC:v', '-SPEC:T', '-SPEC:D', '-COMP:Adv', '-COMP:A'},
                            'P': {'!COMP:D', '-COMP:Adv', '-SPEC:Adv', '-SPEC:C', '-SPEC:T', '-SPEC:N', '-SPEC:V', '-SPEC:v', '-SPEC:T/inf', 'λ:R'},
                            'C': {'!COMP:T', '-COMP:Adv', '-SPEC:V', '-SPEC:C', '-SPEC:N', '-SPEC:T/inf'},
                            'A': {'-COMP:D', '-SPEC:Adv', '-COMP:Adv', '-SPEC:D', '-SPEC:V', '-COMP:V', '-COMP:T', '-SPEC:T', '-SPEC:C', '-COMP:C'},
                            'N': {'-COMP:A', '-SPEC:Adv', '-COMP:V', '-COMP:D', '-COMP:V', '-COMP:T', '-COMP:Adv', '-SPEC:V', '-SPEC:T', '-SPEC:C', '-SPEC:N', '-SPEC:D', '-SPEC:N', '-SPEC:P', '-SPEC:T/inf'},
                            'T': {'!COMP:V', '-COMP:Adv', '-SPEC:C', '-SPEC:T', '-SPEC:V', '-SPEC:T/inf', '-ε'},
                            'v': {'V', '!COMP:V', '!SPEC:D', '-COMP:Adv', '-COMP:A', '-COMP:v',  '-SPEC:T/inf', '!wCOMP:V', '-ε'},
                            'V/INTR': {'-COMP:D', '!SPEC:D'},
                            'V/TR': {'-SPEC:D', '!COMP:D'}
                            }

# Class which stores and maintains the lexicon
class Lexicon:
    def __init__(self):
        self.lexical_entries = dict()   #   The lexicon is a dictionary
        self.compose_lexicon()          #   Creates the runtime lexicon by combining the lexicon and
                                        #   the lexical redundancy rules

    # Composes the lexicon from the list of words and lexical redundancy rules
    def compose_lexicon(self):
        for lex in lexicon.keys():
            self.lexical_entries[lex] = lexicon[lex]
            for trigger_feature in lexical_redundancy_rules.keys():
                if trigger_feature in lexicon[lex]:
                    self.lexical_entries[lex] = self.lexical_entries[lex] | lexical_redundancy_rules[trigger_feature]

    # Retrieves lexical items from the lexicon and wraps them into zero-level phrase structure
    # objects
    def retrieve(self, name):
        X0 = PhraseStructure()
        X0.features = self.lexical_entries[name]        # Retrieves lexical features from the lexicon
        X0.phon = name                                  # Name for identification and easy recognition
        X0.zero = True                                  # True = zero-level category
        return X0
