from language_data import LanguageData
from speaker_model import SpeakerModel
from settings import Settings

def run():
    settings = Settings()
    ld = LanguageData()
    ld.read_dataset(settings.dataset_file_name)
    ld.start_logging(settings.log_file_name)
    speakermodel = {'English': SpeakerModel(ld, 'English', settings)}
    n_dataset = 0
    n_total_errors = 0

    for numeration, gold_standard_dataset in ld.study_dataset:
        n_dataset += 1
        ld.prepare_experiment(n_dataset, numeration, gold_standard_dataset)
        speakermodel['English'].derive(numeration)
        n_total_errors += ld.evaluate_experiment(gold_standard_dataset)

    print(f'\nTOTAL ERRORS: {n_total_errors}\n')
    ld.log(f'\nTOTAL ERRORS: {n_total_errors}')

