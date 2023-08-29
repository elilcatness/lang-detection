import os
from dotenv import load_dotenv
from csv import DictWriter

from alive_progress import alive_bar
from googletrans import Translator


FIELDNAMES = ['phrase', 'lang']
DELIMITER = ';'


def main():
    filename = os.getenv('phrases_filename', 'phrases.txt')
    output_filename = os.getenv('output_filename', 'output.csv')
    if (os.path.exists(output_filename) and
            input(f'Файл {output_filename} будет перезаписан. '
                  'Продолжить? (y\\n): ').lower() != 'y'):
        return
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        DictWriter(f, FIELDNAMES, delimiter=DELIMITER).writeheader()
    t = Translator()
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
                    w = DictWriter(outp_f, FIELDNAMES, delimiter=DELIMITER)
                    w.writerow({'phrase': line, 'lang': t.detect(line).lang})
                bar()
        if is_empty:
            return print(f'Файл {filename} пуст!')


if __name__ == '__main__':
    load_dotenv()
    main()
