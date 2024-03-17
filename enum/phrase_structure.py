# Asymmetric binary-branching phrase structure formalism
# together with several dependencies
#

# Major lexical categories assumed in this grammar
major_lexical_categories = ['C', 'N', 'v', 'V', 'T/inf', 'A', 'D', 'Adv', 'T', 'P', 'a', 'b', 'c', 'd']


class PhraseStructure:
    logging = None
    chain_index = 1
    logging_report = ''
    def __init__(self, X=None, Y=None):
        self.const = (X, Y)       # Left and right daughter constituents
        self.adjuncts = set()     # Adjunct pointers, for bookkeeping during derivation, not part of the theory
        self.phon = ''            # Name
        self.features = set()     # Lexical features
        self.zero = False         # Zero-level categories
        self.silent = False       # Phonological silencing
        self.copied_ = False       # Constituent is a copy of something else
        self.chain_index = 0      # Marking chains in the output, not part of the theory
        self.mother_ = None       # Mother node
        if X:
            X.mother_ = self
        if Y:
            Y.mother_ = self

    # Definition for left constituent (abstraction)
    def left(X):
        return X.const[0]

    # Definition for right constituent (abstraction)
    def right(X):
        return X.const[1]

    # Definition for left sibling
    def isLeft(X):
        return X.sister() and X.mother().left() == X

    # Definition for right sibling
    def isRight(X):
        return X.sister() and X.mother().right() == X

    # Definition for motherhood
    def mother(X):
        return X.mother_

    def copied(X):
        return X.copied_

    def copy(X):
        if not X.terminal():
            Y = PhraseStructure(X.left().copy(), X.right().copy())
        else:
            Y = PhraseStructure()
        Y.copy_properties(X)
        return Y

    def copy_properties(Y, X):
        Y.phon = X.phon
        Y.features = X.features
        Y.zero = X.zero
        Y.chain_index = X.chain_index
        Y.silent = X.silent
        Y.copied_ = X.copied_
        Y.adjuncts = X.adjuncts.copy()

    # Copying operation with phonological silencing
    # Implement chain numbers (if needed) inside this function
    def chaincopy(X):
        Y = X.copy()
        X.silent = True
        Y.copied_ = True
        return Y

    # Zero-level categories are phrase structure objects with less that two daughter constituents
    # or they are marked as zero-level objects; these two are still kept separate since the
    # latter is currently an independent stipulation
    def zero_level(X):
        return (X.zero or X.terminal()) and not X.sublexical()

    # Terminal elements do not have daughter constituents
    # Note: a constituent can be None, hence the search
    def terminal(X):
        for x in X.const:
            if x:
                return False
        return True

    # Preconditions for Merge
    def MergePreconditions(X, Y):
        if X.isRoot() and Y.isRoot():
            if Y.terminal() and Y.obligatory_wcomplement_features():
                return False
            if X.zero_level():                                                              #   Test if X selects Y
                return X.complement_subcategorization(Y)
            elif Y.zero_level():
                return Y.complement_subcategorization(None)                                 #   Test if Y requires a complement
            else:
                return Y.head().specifier_subcategorization(X)                              #   Test specifier subcategorization

    # Merge, with head and phrasal repair functions
    # Assumes that Move is part of Merge and derives the relevant
    # constructions without countercyclic operations
    def MergeComposite(X, Y):
        return X.HeadMovement(Y).Merge(Y).PhrasalMovement()

    # Standard bare Merge
    def Merge(X, Y):
        return PhraseStructure(X, Y)

    def HeadMovementPreconditions(X, Y):
        return X.zero_level() and X.bound_morpheme() and not X.mandateDirectHeadMerge()

    # Head repair for X before Merge
    def HeadMovement(X, Y):
        if X.HeadMovementPreconditions(Y):
            PhraseStructure.logging_report += f'\n\t\t + Head chain by {X}° targeting {Y.head()}°'
            return Y.head().chaincopy().HeadMerge_(X)
        return X

    def PhrasalMovement(X):
        if X.head().EPP() and X.head().complement() and X.head().Agree(X.head().EPP()):
            return X.head().Agree(X.head().EPP()).babtize_chain(X).chaincopy().Merge(X)
        return X

    def Agree(X, feature_set):
        if X.complement().minimal_search(feature_set):
            return X.complement().minimal_search(feature_set)
        if X.complement().minimal_search({'D'}):    #   Last resort
            return X.complement().minimal_search({'D'})

    # Searches for a goal for phrasal movement, feature = target feature to be searched
    # This is also the kernel for Agree/probe-goal operation
    def minimal_search(X, feature_set):
        while X:
            if X.zero_level():
                if feature_set == {'D'}:
                    break
                X = X.complement()
            else:
                for c in X.const:
                    if feature_set <= c.head().features:
                        return c
                    if c.head() == X.head():
                        X = c

    # Preconditions for Head Merge (X Y)
    def HeadMergePreconditions(X, Y):
        return X.zero_level() and Y.zero_level() and Y.w_selects(X) and not Y.blockDirectHeadMerge()

    # Head Merge creates zero-level categories and implements feature inheritance
    def HeadMerge_(X, Y):
        Z = X.Merge(Y)
        Z.zero = True
        Z.features = Y.features
        Z.adjuncts = Y.adjuncts
        return Z

    # Preconditions for adjunction
    def AdjunctionPreconditions(X, Y):
        return X.isRoot() and \
               Y.isRoot() and \
               X.head().license_adjunction() and \
               X.head().license_adjunction() in Y.head().features

    # Adjunct Merge is a variation of Merge,
    # but creates a parallel phrase structure
    def Adjoin_(X, Y):
        X.mother_ = Y
        Y.adjuncts.add(X)
        return {X, Y}

    def FeatureMergePreconditions(X, Y):
        return X.sublexical() and Y.terminal() and X.obligatory_fcomplement_features() <= Y.features

    def FeatureMerge(X, Y):
        Y.features = Y.features | X.features
        Y.features.discard('sublexical')
        return Y

    def obligatory_fcomplement_features(X):
        return {f.split(':')[1] for f in X.features if f.startswith('!fCOMP')}

    # Word-internal selection between X and Y under (X Y), where
    # Y selects for X
    def w_selects(Y, X):
        return Y.leftmost().obligatory_wcomplement_features() and Y.leftmost().obligatory_wcomplement_features() <= X.rightmost().features

    def leftmost(X):
        while X.left():
            X = X.left()
        return X

    def rightmost(X):
        while X.right():
            X = X.right()
        return X

    def babtize_chain(X, probe):
        if X.chain_index == 0:
            PhraseStructure.chain_index += 1
            X.chain_index = PhraseStructure.chain_index
            PhraseStructure.logging_report += f'\n\t\t + Phrasal chain by {probe}° targeting {X})'
        return X

    # Determines whether X has a sister constituent and returns that constituent if present
    def sister(X):
        if X.mother():
            return next((const for const in X.mother().const if const != X), None)

    # Determines whether X has a right sister and return that constituent if present
    def complement(X):
        if X.zero_level() and X.isLeft():
            return X.sister()

    # Left sister
    def left_sister(X):
        if X.sister() and X.mother().right() == X:
            return X.sister()

    # Calculates the head of any phrase structure object X ("labelling algorithm")
    # Returns the most prominent zero-level category inside X
    def head(X):
        for x in (X,) + X.const:            #   Order is from left to right
            if x and x.zero_level():        #   Returns the first zero-level object
                return x
        return x.head()                     #   Recursion

    def container(X):
        if X.max().mother():
            return X.max().mother().head()

    # Verifies (recursively) that the configuration satisfies complement and
    # specifier subcategorization; only zero-level categories have subcategorization
    # requirements
    def subcategorization(X):
        if X.zero_level():
            return X.complement_subcategorization(X.complement()) and \
                   X.specifier_subcategorization() and \
                   X.w_subcategorization()
        return X.left().subcategorization() and X.right().subcategorization()    #   Recursion

    # Word-internal subcategorization that models morphotactic/morphological regularities
    # The recursive function looks for violations, otherwise returns True
    def w_subcategorization(X):
        if X.terminal():
            if X.obligatory_wcomplement_features():
                return False
        if X.left() and X.right():
            if not X.right().w_selects(X.left()):
                return False
        if X.left() and not X.left().terminal():
            if not X.left().w_subcategorization():
                return False
        if X.right() and not X.right().terminal():
            if not X.right().w_subcategorization():
                return False
        return True

    # Complement subcategorization under [X Y]
    def complement_subcategorization(X, Y):
        if not Y:
            return not X.positive_comp_selection()
        return (X.positive_comp_selection() <= Y.head().features) and \
               not (X.negative_comp_selection() & Y.head().features)

    # Specifier subcategorization under [_YP XP YP]
    # Returns False if subcategorization conditions are not met
    def specifier_subcategorization(X, Spec=None):
        if not Spec:
            if not X.specifier():
                return not X.positive_spec_selection()
            Spec = X.specifier()
        return X.positive_spec_selection() <= Spec.head().features and \
               not (X.negative_spec_selection() & Spec.head().features)

    # A generalized definition for the notion of specifier based on
    # head algorithm, allows specifier stacking and includes
    # left-adjoined phrases (if adjunction is part of the grammar)
    def specifier(X):
        x = X.head()
        while x and x.mother() and x.mother().head() == X:
            if x.mother().left() != X:
                return x.mother().left()
            x = x.mother()

    def max(X):
        while X:
            if X.mother() and X.mother().head() == X.head():
                X = X.mother()
            else:
                return X

    def referential_argument(X):
        return 'D' in X.head().features and not X.zero_level()

    def thematic_head(X):
        return 'θ' in X.features and not X.EPP()

    def verbal(X):
        return 'V' in X.features

    # Definition for bound morpheme
    def bound_morpheme(X):
        return 'PC:#X' in X.features

    # Definition for EPP
    def EPP(X):
        return next((set(f.split(':')[1].split(',')) for f in X.features if f.startswith('EPP')), None)

    def sublexical(X):
        return 'sublexical' in X.features

    # Definition for operators
    def operator(X):
        return 'WH' in X.features

    # Definition for scope markers
    def scope_marker(X):
        return 'SCOPE' in X.features

    def linearizes_left(X):
        return 'λ:L' in X.head().features

    def linearizes_right(X):
        return 'λ:R' in X.head().features

    def isRoot(X):
        return not X.mother() and not X.sublexical()

    def mandateDirectHeadMerge(X):
        return 'ε' in X.features

    def blockDirectHeadMerge(X):
        return '-ε' in X.features

    def obligatory_wcomplement_features(X):
        return {f.split(':')[1] for f in X.features if f.startswith('!wCOMP')}

    def positive_spec_selection(X):
        return {f.split(':')[1] for f in X.features if f.startswith('!SPEC')}

    def negative_spec_selection(X):
        return {f.split(':')[1] for f in X.features if f.startswith('-SPEC')}

    def positive_comp_selection(X):
        return {f.split(':')[1] for f in X.features if f.startswith('!COMP')}

    def negative_comp_selection(X):
        return {f.split(':')[1] for f in X.features if f.startswith('-COMP')}

    def license_adjunction(X):
        for f in X.features:
            if f.startswith('α:'):
                return f.split(':')[1]

    def __repr__(X):
        str = ''
        if X.mother() and X not in X.mother().const:                    # Adjunct printout, add the adjunction link
            if X.mother().zero_level():
                str += f'{X.mother().head().lexical_category()}|'
            else:
                str += f'{X.mother().head().lexical_category()}P|'
        if X.terminal():                #   Terminal constituents are spelled out
            str += X.phon
        else:
            if X.zero_level():          #   Non-terminal zero-level categories use different brackets
                bracket = ('(', ')')
            else:
                bracket = ('[', ']')
            str += bracket[0]
            if not X.zero_level():
                str += f'_{X.head().lexical_category()}P '  #   Print information about heads and labelling
            for const in X.const:
                str += f'{const} '
            str = str[:-1]
            str += bracket[1]
            if X.chain_index != 0:
                str += f':{X.chain_index} '
        for x in X.adjuncts:
            str += '^'
        return str

    # Auxiliary printout function, to help eyeball the output
    def __str__(X):
        str = ''
        if X.silent:                    #   Phonologically silenced constituents are marked by __
            if X.zero_level():
                return '_'
            else:
                return f'_:{X.chain_index}'
        if X.mother() and X not in X.mother().const:                    # Adjunct printout, add the adjunction link
            if X.mother().zero_level():
                str += f'{X.mother().head().lexical_category()}|'
            else:
                str += f'{X.mother().head().lexical_category()}P|'
        if X.terminal():                #   Terminal constituents are spelled out
            str += X.phon
        else:
            if X.zero_level():          #   Non-terminal zero-level categories use different brackets
                bracket = ('(', ')')
            else:
                bracket = ('[', ']')
            str += bracket[0]
            if not X.zero_level():
                str += f'_{X.head().lexical_category()}P '  #   Print information about heads and labelling
            for const in X.const:
                str += f'{const} '
            str = str[:-1]
            str += bracket[1]
            if X.chain_index != 0:
                str += f':{X.chain_index}'
        for x in X.adjuncts:
            str += '^'
        return str

    # Defines the major lexical categories used in all printouts
    def lexical_category(X):
        return next((f for f in major_lexical_categories if f in X.features), '?')
