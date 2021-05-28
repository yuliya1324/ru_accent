from russtress import Accent
import sys
import re

accent = Accent()


def accent_neuro(files):
    for file in files:
        new_file = re.sub(r'\.(?=[^.]+$)', '.nacc.', file)
        with open(file, encoding='utf-8') as file_read:
            with open(new_file, 'w', encoding='utf-8') as file_write:
                for line in file_read:
                    accented_line = accent.put_stress(line)
                    file_write.write(accented_line)


def main():
    files = sys.argv[1:]
    if not files:
        print('No files to accent')
        exit()
    accent_neuro(files)


if __name__ == '__main__':
    main()
