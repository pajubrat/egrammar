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
        return self.semantic_interpretation

    def interpret_(self, X):
        if X.referential_argument():
            self.semantic_interpretation['thematic roles'].add(self.thematic_roles.assign(X))
        if not X.zero_level():
            self.interpret_(X.left())
            self.interpret_(X.right())

