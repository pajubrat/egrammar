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

    for input_data in ld.batch_dataset:
        n_dataset += 1
        language = Lexicon.guess_language(input_data['numeration'])
        ld.prepare_experiment(n_dataset, input_data, language)
        output_data = speaker_model[language].derive(input_data['numeration'])
        n_total_errors += ld.evaluate_experiment(input_data, output_data)

        #   ^ we need to send the dataset and the whole output (including semantics) for this function

    print(f'\nTOTAL ERRORS: {n_total_errors}\n')
    ld.log(f'\nTOTAL ERRORS: {n_total_errors}')

