from phrase_structure import PhraseStructure
from lexicon import Lexicon
from LF_interface import LFInterface
from PF_spellout import PFspellout
from narrow_semantics import NarrowSemantics
from support import print_lst, print_constituent_lst, tcopy, tset
import itertools


class SpeakerModel:
    def __init__(self, ld, language):

        # Composition of the speaker model
        self.language = language
        self.lexicon = Lexicon()
        self.LFInterface = LFInterface()
        self.PFspellout = PFspellout()
        self.narrow_semantics = NarrowSemantics()

        # Internal bookkeeping, data management and logging
        self.language_data = ld

        # List of all syntactic operations available in the grammar
        self.syntactic_operations = [(PhraseStructure.MergePreconditions, PhraseStructure.MergeComposite, 2, 'Merge'),
                                     (PhraseStructure.HeadMergePreconditions, PhraseStructure.HeadMerge_, 2, 'Head Merge'),
                                     (PhraseStructure.AdjunctionPreconditions, PhraseStructure.Adjoin_, 2, 'Adjoin')]

    # Wrapper function for the derivational search function
    # Performs initialization and maps the input into numeration
    def derive(self, numeration):
        self.derivational_search_function([self.lexicon.retrieve(item) for item in numeration])

    # Derivational search function
    def derivational_search_function(self, sWM):
        if self.derivation_is_complete(sWM):                                                                #   Only one phrase structure object in working memory
            self.process_output(sWM)                                                                  #   Terminate processing and evaluate solution
        else:
            for Preconditions, OP, n, name in self.syntactic_operations:                                    #   Examine all syntactic operations OP
                for SO in itertools.permutations(sWM, n):                                                   #   All n-tuples of objects in sWM
                    if Preconditions(*SO):                                                                  #   Blocks illicit derivations
                        PhraseStructure.logging_report += f'\t{name}({print_lst(SO)})'                      #   Add line to logging report
                        new_sWM = {x for x in sWM if x not in set(SO)} | tset(OP(*tcopy(SO)))               #   Update sWM
                        self.language_data.log_resource_consumption(new_sWM, sWM)                           #   Record resource consumption and write log entries
                        self.derivational_search_function(new_sWM)                                          #   Continue derivation, recursive branching

    @staticmethod
    def derivation_is_complete(sWM):
        return len({X for X in sWM if X.isRoot()}) == 1

    def process_output(self, sWM):
        # Log the solution that will be evaluated
        self.language_data.log(f'\t{print_constituent_lst(sWM)}\n')

        # LF_interface legibility test
        for X in sWM:
            if not self.LFInterface.legibility_conditions(X):
                self.language_data.log('\n\n')
                return

        # PF pathway
        output_sentence = f'{self.PFspellout.spellout(X)}'

        # LF pathway
        semantic_interpretation = f'{self.narrow_semantics.semantic_interpretation(X)}'

        # Report results
        self.language_data.report_results(output_sentence, semantic_interpretation, sWM)

