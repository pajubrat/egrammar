from PF_spellout import PFspellout

class ThematicRoles:
    def __init__(self):
        self.spellout = PFspellout()        #   Auxiliary structure for printing the output

    def assign(self, X):
        assigner = X.container()
        role = '*'
        if assigner and assigner.thematic_head():
            if X.max() == assigner.complement():
                role = 'patient'
            if X.max() == assigner.specifier():
                role = 'agent'
            return f'{role} of {self.spellout.linearize_word(X.container(), "")}({self.spellout.spellout(X.max(), True)})'
        if not X.max().copied():
            return f'*??({self.spellout.spellout(X.max(), True)})'   #   Projection principle
