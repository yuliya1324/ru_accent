import re
from collections import defaultdict
import sys


def read_dict(filename, dic):
    with open(filename) as file_read:
        for line in file_read:
            if line.split():
                word, acc = line.split()
            dic[re.sub(r'\(.+$', '', word)] += fr'\x1{word}={acc}'
    return dic


def normalize(s):
    if re.match('^[А-Я]', s):
        caps = '!'
    else:
        caps = ''
    return s.lower(), caps


def accentw(word):
    voc = "([аеиоуыэюяёАЕИОУЫЭЮЯЁ])"
    if not re.match('[А-я]', word) or not re.search(voc, word) or re.search('[ёЁ]', word):
        return word
    key, caps = normalize(word)
    vals = None
    for i in range(len(key), -1, -1):
        val = di[key[0:i]]
        if not val:
            continue
        ar = val.split(r'\x1')
        for v in ar:
            if v:
                regex, acc = v.split('=')
                if re.match('^'+regex+'$', key):
                    if caps != '!' and '!' in acc:
                        continue
                    vals = acc
                    break
        if vals:
            break
    if not vals or (caps == '' and re.match('!', vals)):
        return word
    vals = set(re.split('[,;]', vals.replace('\n', '')))
    chars = re.sub(voc, r'\1|', word).split('|')
    for val in vals:
        pos, acc = re.findall(r'(\d+)(.*)', val)[0]
        if acc == '' or acc == '!':
            acc = "'"
        pos = int(pos)
        if pos > 0:
            chars[pos-1] += acc
    word = re.sub('Е"', 'Ё', re.sub('е"', 'ё', "".join(chars)))
    return word


def accent_line_rules(line):
    words = re.findall('[А-яЁё-]+', line)
    for word in words:
        new_word = accentw(word)
        if (not re.search(fr"{word}'", line)) and (word != new_word):
            line = re.sub(word, new_word, line)
    return line


def accent_rules(files):
    for file in files:
        with open(file, encoding='utf-8') as file_read:
            with open(re.sub(r'\.(?=[^.]+$)', '.acc.', file), 'w', encoding='utf-8') as file_write:
                for line in file_read:
                    file_write.write(accent_line_rules(line))


def main():
    files = sys.argv[1:]
    if not files:
        print('No files to accent')
        exit()
    accent_rules(files)


di = defaultdict(str)
di = read_dict('accent1.dic', di)
di = read_dict('accent.dic', di)


if __name__ == '__main__':
    main()
