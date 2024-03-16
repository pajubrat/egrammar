from thematic_roles import ThematicRoles

class NarrowSemantics:
    def __init__(self):
        self.thematic_roles = ThematicRoles()
        self.semantic_interpretation = dict()
        self.initialize()

    def initialize(self):
        self.semantic_interpretation = {'thematic roles': set()}

    def interpret(self, X):
        self.initialize()
        self.interpret_(X)
        return self.results()

    def interpret_(self, X):
        if X.referential_argument():
            interpretation = self.thematic_roles.assign(X)
            if interpretation:
                self.semantic_interpretation['thematic roles'].add(interpretation)
        if not X.zero_level():
            self.interpret_(X.left())
            self.interpret_(X.right())

    def results(self):
        for key in self.semantic_interpretation.keys():
            for v in self.semantic_interpretation[key]:
                if v and v.startswith('*'):
                    return False
        return True


