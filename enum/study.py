from language_data import LanguageData
from speaker_model import SpeakerModel
from lexicon import Lexicon
from settings import Settings

def run():
    settings = Settings()
    ld = LanguageData()
    Lexicon(settings)   #   Creates class properties for the Lexicon class
    ld.read_dataset(settings.dataset_file_name)
    ld.start_logging(settings.log_file_name)
    speaker_model = {lang: SpeakerModel(ld, lang, settings) for lang in Lexicon.languages_present}  #   Separate speaker model for each language
    n_dataset = 0
    n_total_errors = 0

    for numeration, gold_standard_dataset in ld.study_dataset:
        n_dataset += 1
        language = Lexicon.guess_language(numeration)   #   Language is determined on the basis of the words in the numeration
        ld.prepare_experiment(n_dataset, numeration, gold_standard_dataset, language)
        speaker_model[language].derive(numeration)
        n_total_errors += ld.evaluate_experiment(gold_standard_dataset)

    print(f'\nTOTAL ERRORS: {n_total_errors}\n')
    ld.log(f'\nTOTAL ERRORS: {n_total_errors}')

