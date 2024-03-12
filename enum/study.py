from language_data import LanguageData
from speaker_model import SpeakerModel

def run():
    ld = LanguageData()                                                                     # Instantiate the language data object
    ld.read_dataset('language data/study 1/dataset1.txt')                                   # Name of the dataset file processed by the script, reads the file
    ld.start_logging()
    speakermodel = {'English': SpeakerModel(ld, 'English')}
    n_dataset = 0                                                                           # Number of datasets in the experiment (counter)
    n_total_errors = 0                                                                      # Number of errors in the experiment (counter)
    for numeration, gold_standard_dataset in ld.study_dataset:
        n_dataset += 1
        print(f'Dataset {n_dataset}:')
        ld.log('\n---------------------------------------------------\n')
        ld.log(f'Dataset {n_dataset}:\n')
        ld.log(f'Numeration: {numeration}\n')
        ld.log(f'Predicted outcome: {gold_standard_dataset}\n\n\n')
        speakermodel['English'].derive(numeration)
        n_total_errors += ld.evaluate_experiment(ld.output_data, gold_standard_dataset)
    print(f'\nTOTAL ERRORS: {n_total_errors}\n')
    ld.log(f'\nTOTAL ERRORS: {n_total_errors}')

