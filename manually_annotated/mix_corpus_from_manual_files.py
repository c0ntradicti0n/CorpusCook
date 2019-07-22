import random
import regex as re
from nltk import flatten

from helpers.os_tools import get_files_from_recursive_path


from numpy import cumsum

manual_samples_dir = "./manually_annotated/"

def percentage_split(seq, percentages):
    cdf = cumsum(percentages)
    assert cdf[-1] == 1.0
    stops = list(map(int, cdf * len(seq)))
    return [seq[a:b] for a, b in zip([0]+stops, stops)]

conll_line = re.compile(r"([^\s]+)  ([^\s]+)  ([^\s]+)  ([^\s]+)")
conll_line_sanitizer = re.compile(r"([^\s]*)  ([^\s]*)  ([^\s]+)  ([^\s]+)")

def sanitize_conll(path):
    with open(path, 'r') as f1:
        with open(path+'x', 'w') as f2:
            for l in f1.readlines():
                if l:
                    match = conll_line_sanitizer.match(l)
                    if match and not conll_line.match(l):
                        token, pos, tag_wod, tag_annot = match.groups()

                        if not conll_line.match(l):
                            if not pos:
                                # bad tag for spacy
                                pos = "UKN"

                            elif pos == 'SP':
                                # del newline tokens
                                continue
                        l = "  ".join([token, pos, tag_wod+pos, tag_annot])
                        print (l)
                    f2.write(l)

def read_conll_file (path):
    with open(path, 'r') as f:
        all_lines = f.read()
    splitted = all_lines.split(sep='\n\n')
    random.shuffle(splitted[1:])
    return splitted[1:]

def write_conll_file (path, samples):
    with open(path, 'w+') as f:
        f.write("-DOCSTART- -X- -X- O\n\n")
        f.write("\n\n".join(samples))

set_layout = {'train':0.8,
              'test':0.2}

def mix_files():
    relevant_files_paths = list(get_files_from_recursive_path(manual_samples_dir + "hil*.conll3"))
    all_samples = list(flatten([read_conll_file(path) for path in relevant_files_paths]))
    random.shuffle(all_samples)
    tvt = percentage_split(all_samples, list(set_layout.values()))
    names = list(set_layout.keys())
    for name, samples in zip (names, tvt):
        print ("%s-set contains %d samples" %(name, len(samples)) )
        write_conll_file(manual_samples_dir + name + '.conll3', samples)

mix_files()

