

class PFspellout:
    def __init__(self):
        pass

    def spellout(self, X, spellout_all=False):
        return self.linearize(X, spellout_all)[:-1]     #   Remove extra space at the end

    def linearize(self, X, spellout_all=False):
        linearized_output_str = ''
        # Linearization of left adjuncts
        for x in (x for x in X.adjuncts if x.linearizes_left()):
            linearized_output_str += self.linearize(x)
        # Linearization of regular constituents
        if spellout_all or not X.silent:
            if X.zero_level():
                linearized_output_str += self.linearize_word(X, '') + ' '
            else:
                for x in X.const:
                    linearized_output_str += self.linearize(x)
        # Linearization of right adjuncts
        for x in (x for x in X.adjuncts if x.linearizes_right()):
            linearized_output_str += self.linearize(x)
        return linearized_output_str

    # Spellout algorithm for words, creates morpheme boundaries marked by symbol #
    def linearize_word(self, X, word_str):
        if X.terminal():
            if word_str:
                word_str += '#'
            word_str += X.phon
        else:
            for x in X.const:
                word_str = self.linearize_word(x, word_str)
        return word_str

