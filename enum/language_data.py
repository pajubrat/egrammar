from phrase_structure import PhraseStructure
from support import print_constituent_lst

#
# This class maintains all data used in the simulation
#
class LanguageData:
    def __init__(self):
        self.study_dataset = []             # Datasets for one study
        self.log_file = None                # Handle for the log file (stored logging output)
        self.n_steps = 0                    # N of derivational steps
        self.output_data = set()            # Stored the output from each experiment
        self.n_accepted_sentences = 0       # Number of accepted sentences

    # Read the dataset
    def read_dataset(self, filename):
        numeration = []
        dataset = set()
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('END'):
                    line = line.strip()
                    if line.startswith('Numeration='):
                        if numeration:
                            self.study_dataset.append((numeration, dataset))
                            dataset = set()
                        numeration = [word.strip() for word in line.split('=')[1].split(',')]
                    else:
                        dataset.add(line.strip())
                if line.startswith('END'):
                    break
            self.study_dataset.append((numeration, dataset))

    def start_logging(self):
        self.log_file = open('language data/study 1/log.txt', 'w')
        PhraseStructure.logging = self.log_file

    def log(self, str):
        self.log_file.write(str)

    def log_resource_consumption(self, new_sWM, old_sWM):
        self.n_steps += 1
        self.log_file.write(f'{self.n_steps}.\n\n')
        self.log_file.write(f'\t{print_constituent_lst(old_sWM)}\n')
        self.log_file.write(f'{PhraseStructure.logging_report}')
        self.log_file.write(f'\n\t= {print_constituent_lst(new_sWM)}\n\n')
        PhraseStructure.logging_report = ''

    def evaluate_experiment(self, output_from_simulation, gold_standard_dataset):
        print(f'\tDerivational steps: {self.n_accepted_sentences}')
        overgeneralization = output_from_simulation - gold_standard_dataset
        undergeneralization = gold_standard_dataset - output_from_simulation
        errors = len(overgeneralization) + len(undergeneralization)
        print(f'\tErrors {errors}')
        if errors > 0:
            print(f'\tShould not generate: {overgeneralization}')
            print(f'\tShould generate: {undergeneralization}')
        return errors

    def report_results(self, output_sentence, semantic_interpretation, sWM):
        self.n_accepted_sentences += 1
        PhraseStructure.chain_index = 0
        print(f'\t({self.n_accepted_sentences}) {output_sentence} {print_constituent_lst(sWM)} {semantic_interpretation}')   # Print the output
        self.log(f'\t^ ACCEPTED: {output_sentence}')
        self.output_data.add(output_sentence.strip())
        self.log('\n\n')