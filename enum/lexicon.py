from phrase_structure import PhraseStructure
from support import comment, well_formed_lexical_entry

# Class which stores and maintains the lexicon
class Lexicon:
    def __init__(self, settings):
        self.lexical_entries = dict()               #   The lexicon is a dictionary
        self.lexical_redundancy_rules = dict()      #   Lexical redundancy rules
        self.compose_lexicon(settings)              #   Creates the runtime lexicon by combining the lexicon and
                                                    #   the lexical redundancy rules

    # Composes the lexicon from the list of words and lexical redundancy rules
    def compose_lexicon(self, settings):
        self.load_lexicon(settings.lexicon_file_name)
        self.load_redundancy_rules(settings.lexical_redundancy_rules_file_name)
        for lex in self.lexical_entries.keys():
            for trigger_feature in self.lexical_redundancy_rules.keys():
                if trigger_feature in self.lexical_entries[lex]:
                    self.lexical_entries[lex] = self.lexical_entries[lex] | self.lexical_redundancy_rules[trigger_feature]

    # Retrieves lexical items from the lexicon and wraps them into zero-level phrase structure
    # objects
    def retrieve(self, name):
        X0 = PhraseStructure()
        X0.features = self.lexical_entries[name]        # Retrieves lexical features from the lexicon
        X0.phon = name                                  # Name for identification and easy recognition
        X0.zero = True                                  # True = zero-level category
        return X0

    def load_redundancy_rules(self, lexical_redundancy_file_name):
        lexical_redundancy_rules_file = open(lexical_redundancy_file_name, 'r', encoding='utf8')
        self.lexical_redundancy_rules = {}
        for line in lexical_redundancy_rules_file.readlines():
            line = line.strip()
            if not comment(line) and well_formed_lexical_entry(line):
                key, value = line.split('::')
                features = value.split(' ')
                self.lexical_redundancy_rules[key.strip()] = {feature.strip() for feature in features}

    def load_lexicon(self, lexical_file_name):
        lexicon_file = open(lexical_file_name, 'r', encoding='utf8')
        self.lexical_entries = {}
        for line in lexicon_file.readlines():
            line = line.strip()
            if not comment(line) and well_formed_lexical_entry(line):
                key, value = line.split('::')
                features = value.split(' ')
                self.lexical_entries[key.strip()] = {feature.strip() for feature in features}
