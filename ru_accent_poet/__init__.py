import re
import sys
import os
import tensorflow as tf
from .rules import accent_line_rules
from .patch_russtress import PatchedAccent

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

# Initialize our patched version of the Accent class for TensorFlow/Keras compatibility
accent = PatchedAccent()
non_str = ['обо', 'изо', 'подо', 'нибудь']


def accent_line(line):
    words = line.split()
    words_rule = accent_line_rules(line).split()
    words_nacc = accent.put_stress(line).split()
    for j in range(len(words)):
        voc = re.findall('[аеиоуыэюяёАЕИОУЫЭЮЯЁ]', words[j])
        if voc and len(voc) < 2 or not voc or re.findall('[ёЁ]', words[j]) or words[j] in non_str:
            continue
        elif (len(re.findall("'", words_rule[j])) > 1) or \
                ("'" not in words_rule[j] and not re.findall('[ёЁ]', words_rule[j])) or \
                ("'" in words_rule[j] and re.findall('[ёЁ]', words_rule[j])):
            words[j] = words_nacc[j]
        else:
            words[j] = words_rule[j]
    new_line = ' '.join(words)
    return new_line


def write_file(files):
    for file in files:
        with open(file, encoding='utf-8') as clear_file:
            with open(re.sub(r'\.(?=[^.]+$)', '.accented.', file), 'w', encoding='utf-8') as file_write:
                for line in clear_file:
                    file_write.write(accent_line(line) + '\n')


def main():
    files = sys.argv[1:]
    if not files:
        print('No files to accent')
        exit()
    write_file(files)


if __name__ == '__main__':
    main()
