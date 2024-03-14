from phrase_structure import PhraseStructure
from support import comment, well_formed_lexical_entry

# Class which stores and maintains the lexicon
class Lexicon:
    root_lexicon = dict()       #   Root lexicon contains all lexical items
    redundancy_rules = dict()   #   Redundancy rules
    languages_present = set()   #   Languages present in the root lexicon

    def __init__(self, settings, language=None):
        Lexicon.initialize_root_lexicons(settings)
        self.speaker_lexicon = dict()
        self.compose_speaker_lexicon(language)

    @classmethod
    def initialize_root_lexicons(cls, settings):
        if not cls.redundancy_rules:
            cls.load_redundancy_rules(settings.lexical_redundancy_rules_file_name)
        if not cls.root_lexicon:
            cls.load_root_lexicon(settings.root_lexicon_file_name)
            cls.compose_set_of_languages()

    @classmethod
    def compose_set_of_languages(cls):
        for key in cls.root_lexicon.keys():
            cls.languages_present.update({f for f in cls.root_lexicon[key] if f.startswith('LANG:')})

    @classmethod
    def guess_language(cls, numeration):
        for word in numeration:
            if word in cls.root_lexicon.keys() and cls.language(cls.root_lexicon[word]):
                return cls.language(cls.root_lexicon[word])[0]
        return 'LANG:EN'    #   Default language

    @staticmethod
    def language(features):
        return [f for f in features if f.startswith('LANG:')]

    # Composes the speaker lexicon from the list of words and lexical redundancy rules
    def compose_speaker_lexicon(self, language):
        if language:
            for item in Lexicon.root_lexicon.keys():
                if language in Lexicon.root_lexicon[item] or \
                        not self.language(Lexicon.root_lexicon[item]):
                    self.speaker_lexicon[item] = Lexicon.root_lexicon[item].copy()
                    self.speaker_lexicon[item].add(language)    #   Adds language feature (relevant if no language is specified)
            for lex in self.speaker_lexicon.keys():
                for trigger_features in Lexicon.redundancy_rules.keys():
                    if trigger_features <= self.speaker_lexicon[lex]:
                        self.speaker_lexicon[lex] = self.speaker_lexicon[lex] | Lexicon.redundancy_rules[trigger_features]

    # Retrieves lexical items from the lexicon and wraps them into zero-level phrase structure
    # objects
    def retrieve(self, name):
        X0 = PhraseStructure()
        X0.features = self.speaker_lexicon[name]        # Retrieves lexical features from the lexicon
        X0.phon = name                                  # Name for identification and easy recognition
        X0.zero = True                                  # True = zero-level category
        return X0

    @classmethod
    def load_redundancy_rules(cls, lexical_redundancy_file_name):
        lexical_redundancy_rules_file = open(lexical_redundancy_file_name, 'r', encoding='utf8')
        for line in lexical_redundancy_rules_file.readlines():
            line = line.strip()
            if line and not comment(line) and well_formed_lexical_entry(line):
                key, value = line.split('::')
                features = value.split(' ')
                key = frozenset({feature.strip() for feature in key.split(' ')})    #   Frozenset is immutable set and can therefore be the key in the dictionary
                cls.redundancy_rules[key] = {feature.strip() for feature in features}

    @classmethod
    def load_root_lexicon(cls, lexical_file_name):
        lexicon_file = open(lexical_file_name, 'r', encoding='utf8')
        for line in lexicon_file.readlines():
            line = line.strip()
            if not comment(line) and well_formed_lexical_entry(line):
                key, value = line.split('::')
                features = value.split(' ')
                cls.root_lexicon[key.strip()] = {feature.strip() for feature in features}

