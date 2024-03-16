from phrase_structure import PhraseStructure
from support import print_constituent_lst, print_dictionary

#
# This class maintains all data used in the simulation
#
class LanguageData:
    def __init__(self):
        self.batch_dataset = []             # Datasets for one study
        self.log_file = None                # Handle for the log file (stored logging output)
        self.n_steps = 0                    # N of derivational steps
        self.output_data = dict()           # Stored the output from each experiment
        self.n_accepted_sentences = 0       # Number of accepted sentences
        self.n_accumulated_total_steps = 0  # Number of derivational steps in a batch dataset

    # Read the dataset
    def read_dataset(self, filename):
        def reset():
            return {'numeration': [], 'targets': set(), 'thematic roles': set()}

        def parse(line):
            line = line.strip()
            key, value = line.split('=')
            values = value.split(';')
            values_ = [v.strip() for v in values]
            return values_

        input_data = reset()
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('END'):
                    line = line.strip()
                    if line.startswith('numeration='):
                        # If we encounter the numeration field, then the current dataset (if it exists) will
                        # be stored into the batch dataset and we start collecting new
                        if input_data['numeration']:
                            self.batch_dataset.append(input_data)
                            input_data = reset()
                        input_data['numeration'] = parse(line)
                    if line.startswith('targets='):
                        input_data['targets'].update(set(parse(line)))
                    if line.startswith('thematic roles='):
                        input_data['thematic roles'].update(set(parse(line)))
                if line.startswith('END'):  #   This command can be used to limit the amount of data examined
                    break
            self.batch_dataset.append(input_data)

    def start_logging(self, log_file_name):
        self.log_file = open(log_file_name, 'w', encoding='utf8')
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

    def log_lexical_content(self, numeration):
        self.log_file.write('\n\nLexical content:\n')
        for lex in numeration:
            self.log_file.write(f'\n{lex}: ')
            for feature in sorted(list(lex.features)):
                self.log_file.write(f'[{feature}] ')
        self.log_file.write('\n\n')

    def prepare_experiment(self, n_dataset, input_data, language):
        self.output_data = {'targets': set(), 'thematic roles': set()}
        self.n_accepted_sentences = 0
        self.n_steps = 0
        print(f'\nNumeration {n_dataset} ({language}): {input_data["numeration"]} -------------------------------\n')
        self.log('\n---------------------------------------------------\n')
        self.log(f'Dataset {n_dataset}:\n')
        self.log(f'{input_data}')

    def evaluate_experiment(self, input_data, output_data):
        print(f'\tDerivational steps: {self.n_steps}')
        self.n_accumulated_total_steps += self.n_steps
        thematic_errors = 0
        grammaticality_overgeneralization = output_data['targets'] - input_data['targets']
        grammaticality_undergeneralization = input_data['targets'] - output_data['targets']
        grammaticality_errors = len(grammaticality_overgeneralization) + len(grammaticality_undergeneralization)
        print(f'\tGrammaticality errors: {grammaticality_errors}')
        if grammaticality_errors > 0:
            print(f'\tShould not generate sentence(s): {grammaticality_overgeneralization}')
            print(f'\tShould generate sentences(s): {grammaticality_undergeneralization}')
        if input_data['thematic roles']:
            thematic_overgeneralization = output_data['thematic roles'] - input_data['thematic roles']
            thematic_undergeneralization = input_data['thematic roles'] - output_data['thematic roles']
            thematic_errors = len(thematic_undergeneralization) + len(thematic_overgeneralization)
            print(f'\tThematic role errors: {thematic_errors}')
            if thematic_errors > 0:
                print(f'\tShould not find interpretation: {thematic_overgeneralization}')
                print(f'\tShould find interpretation: {thematic_undergeneralization}')

        return grammaticality_errors + thematic_errors

    def report_result_to_console(self, output_sentence, semantic_interpretation, sWM):
        self.n_accepted_sentences += 1
        PhraseStructure.chain_index = 0
        print(f'\t({self.n_accepted_sentences}) {output_sentence}\n\t{print_constituent_lst(sWM)}\n\t{print_dictionary(semantic_interpretation)}\n')   # Print the output
        self.log(f'\t^ ACCEPTED: {output_sentence}')
        self.log('\n\n')