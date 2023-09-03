import os
from dotenv import load_dotenv
from csv import DictWriter

from alive_progress import alive_bar
from googletrans import Translator as GTranslator
from deepl import Translator as DTranslator

from src.constants import CHOICES

from src.utils import get_env_var, detect_lang

DELIMITER = ';'


def main():
    filename = os.getenv('phrases_filename', 'phrases.txt')
    output_filename = os.getenv('output_filename', 'output.csv')
    choice = None
    choices_len = len(CHOICES)
    while choice is None:
        try:
            idx = int(input(
                'Выберите действие:\n' +
                '\n'.join(
                    [f'{i + 1}. {CHOICES[i]}' for i in range(choices_len)]) + '\nВыбор: '))
            assert 1 <= idx <= choices_len
            choice = CHOICES[idx - 1]
        except (ValueError, AssertionError):
            print(f'Должно быть введено число от 1 до {choices_len}')
        if (os.path.exists(output_filename) and
                input(f'Файл {output_filename} будет перезаписан. '
                      'Продолжить? (y\\n): ').lower() != 'y'):
            return
        if choice == 'Язык через Google':
            fieldnames = ['Phrase', 'G_lang']
            translators = [GTranslator()]
        elif choice == 'Язык через DeepL':
            fieldnames = ['Phrase', 'D_lang']
            translators = [DTranslator(get_env_var('deepl_token'))]
        elif choice == 'Язык через Google и DeepL':
            fieldnames = ['Phrase', 'G_lang', 'D_lang']
            translators = [GTranslator(), DTranslator(get_env_var('deepl_token'))]
        else:
            raise NotImplementedError(f'Режим "{choice}" ещё не реализован')
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            DictWriter(f, fieldnames, delimiter=DELIMITER).writeheader()
        with open(filename, encoding='utf-8') as f:
            is_empty = True
            lines = f.readlines()
            with alive_bar(len(lines)) as bar:
                for line in lines:
                    line = line.strip()
                    if not line:
                        bar()
                        continue
                    if is_empty:
                        is_empty = False
                    with open(output_filename, 'a', newline='', encoding='utf-8') as outp_f:
                        w = DictWriter(outp_f, fieldnames, delimiter=DELIMITER)
                        row = {'Phrase': line}
                        for t, key in zip(translators, fieldnames[1:3]):
                            row[key] = detect_lang(t, line)
                        w.writerow(row)
                    bar()
            if is_empty:
                return print(f'Файл {filename} пуст!')


if __name__ == '__main__':
    load_dotenv()
    main()
