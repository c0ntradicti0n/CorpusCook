from functools import wraps
import coloredlogs
from tok import Tok
coloredlogs.install()
import logging
logging.getLogger().setLevel(logging.INFO)
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
from spacy.tokens import Doc
from Levenshtein._levenshtein import ratio
from Bio import pairwise2
from difflib import SequenceMatcher
from collections import Iterable


def left_right_encircle(match_density):
    start, stop = 0, 1
    for p in range(len(match_density)):
        start = p
        stop = p + 1

        if match_density[p]<0.6 or (len(match_density[p:])>1 and (sum(match_density[p:]) / len(match_density[p:])
                < sum(match_density[p + 1:])
                / len(match_density[p + 1:]))):
            continue
        else:
            for q in range(len(match_density)-1, p, -1):
                if match_density[q]<0.6 or (sum(match_density[:q]) / len(match_density[:q])
                        > sum(match_density[:q + 1])
                        / len(match_density[:q + 1])):
                    continue
                else:
                    stop = q+1
                    break
            else:
                stop = p + 1
            break
    return start, stop


def fuzzy_search(search_key, text, strictness):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        words = line.split()
        for word in words:
            similarity = SequenceMatcher(None, word, search_key)
            if similarity.ratio() > strictness:
                return " '{}' matches: '{}' in line {}".format(search_key, word, i+1)


def match (hay, needle):
    needle_length  = len(needle.split())
    max_sim_val    = 0
    max_sim_string = u""

    for ngram in ngrams(hay.split(), needle_length + int(.2*needle_length)):
        hay_ngram = u" ".join(ngram)
        similarity = SM(None, hay_ngram, needle).ratio()
        if similarity > max_sim_val:
            max_sim_val = similarity
            max_sim_string = hay_ngram
    return max_sim_string, max_sim_val


def sort(word_list):
    """
    >>> sort (['Mammals', 'eat', 'sometimes', 'fish'])
    [(1, 3, 0, 2), ('eat', 'fish', 'Mammals', 'sometimes')]

    :param word_list:
    :return:
    """
    return list(zip(*sorted(list(enumerate(word_list)), key=lambda x: x[1].lower())))


def match():
    """
    >>> text1 = ['there', 'be', 'many', 'cause', 'of', 'heart', 'failure', 'include', 'have', 'have', 'a', 'myocardial', 'infarction', ',', 'have', 'hypertension', ',', 'heart', 'valve', 'problem', ',', 'cardiomyopathy', ',', 'coronary', 'artery', 'disease', 'and', 'diabetes']
    text1 = "There are many causes of heart failure including having had a myocardial infarction, having hypertension, heart valve problems, cardiomyopathy, coronary artery disease and diabetes".split()

    >>> text2 = ['most', 'often', 'genetic', ',', 'or', 'else', 'from', 'a', 'viral', 'infection', 'or', 't', ',', 'cruzi']

    >>> match_with_biopython(text1, text2)
    False

    >>> text2 = ['cardiomyopathy', ',', 'coronary', 'artery', 'problems', ',', 'heart', 'attack', ',', 'hypertension', ',', 'valve', 'conditions']
    >>> match_with_biopython(text1, text2)
    (0, 17, 78.60000000000011, 17)

    >>> text1[0:17]

    :return:
    """

def match_with_biopython (text1, text2, ignore_order=False):
    ''' Let's match a string with biopython. It's not the fastest choice. But it solves a problem.

    It's hard, because one can normally either match strings against each other, or words, treating them as characters,
    but not a list of words fitting to another list of words. This here operates on fitting the string and then it
    searches a local optimum, where the word-borders fitting chars may belong.

    Python difflib can operate either on strings or on dilimited lists.

    :param text1: list of words
    :param text2: list of words
    :return: tuple of left pos, right pos, confidence score and length

    >>> match_with_biopython(['bid', 'be', 'make', 'by', 'buyer'], ['buyer'])
    (4, 5, 10.0, 1)

    >>> match_with_biopython(['heart', 'failure', 'can', 'be', 'treat', 'with', 'the', 'same', 'medication', 'as', 'cardiomyopathy', 'but', 'also', 'nitrate', 'and', 'diuretic', ',', 'and', 'sometimes', 'a', 'cardioverter', '-', 'defibrillator', 'or', 'a', 'transplanted', 'heart', 'may', 'be', 'necessary', 'for', 'survival'],
    ...                      ['cardiomyopathy'])
    (10, 11, 28.0, 1)

    >>> match_with_biopython(['a', 'positive', 'tb', 'skin', 'test', 'be', 'when', 'the', 'mantoux', 'tuberculin', 'skin', 'test', 'indicate', 'that', 'a', 'person', 'have', 'the', 'bacteria', 'or', 'have', 'be', 'expose', 'to', 'm.', 'tuberculosis'],
    ...                      ['negative', 'tb', 'skin', 'test'])
    (0, 5, 35.1, 5)

    >>> match_with_biopython(['cardiomyopathy', 'be', 'a', 'problem', 'in', 'the', 'heart', 'muscle'],
    ...                      ['this', 'condition', 'occur', 'when', 'there', 'be', 'a', 'problem', 'with', 'the', 'heart', 'muscle', ',', 'the', 'myocardium'])
    (1, 8, 70.2, 7)

    >>> match_with_biopython(['cardiomyopathy', 'can', 'be', 'treat', 'with', 'medication', 'such', 'as', 'beta', 'blocker', ',', 'digoxin', ',', 'and', 'calcium', 'channel', 'blocker'],
    ...                      ['treatment'])
    (3, 4, 14.400000000000007, 1)

    # handle empty token
    >>> match_with_biopython(['cardiomyopathy', 'but', 'also', 'nitrate', 'and', 'diuretic', ',', 'and', 'sometimes', 'a', 'cardioverter', '', 'defibrillator', 'or', 'a', 'transplanted', 'heart', 'may', 'be', 'necessary', 'for', 'survival'],
    ...                      ['cardiomyopathy'])
    (0, 1, 28.0, 1)

    >>> match_with_biopython(['cardiomyopathy', 'can', 'be', 'treat', 'with', 'medication', 'such', 'as', 'beta', 'blocker', ',', 'digoxin', ',', 'and', 'calcium', 'channel', 'blocker'],
    ...                      ['medication'])
    (5, 6, 20.0, 1)

    >>> match_with_biopython(['heart', 'failure', 'be', 'not', 'a', 'common', 'condition', 'find', 'in', 'child'],
    ...                      ['definition'])
    False

    >>> match_with_biopython('if they were normal Python strings, for example getting the length, or iterating over'.split(),
    ...                      'iterating over'.split())
    (12, 14, 28.0, 2)

    >>> match_with_biopython('if'.split(),
    ...                      'if'.split())
    (0, 1, 4.0, 1)

    >>> match_with_biopython('if'.split(),
    ...                      'then'.split())
    False

    >>> match_with_biopython('if they were normal Python strings, for example getting the length, or iterating over'.split(),
    ...                      'if they'.split())
    (0, 2, 14.0, 2)

    >>> match_with_biopython('if they were normal Python strings, for example getting the length, or iterating over'
    ...                          'the elements'.split(),
    ...                          'they are normal Python schrings, so example get th len'.split())
    (1, 8, 95.00000000000001, 7)

    >>> match_with_biopython(['We', 'bought', 'more', 'milk'], ['more'])
    (2, 3, 8.0, 1)

    '''
    if ignore_order:
        translation_list1, text1 = sort(text1)
        translation_list2, text2 = sort(text2)



    alignments = pairwise2.align.localms(
        list(" ".join(text1).lower()),
        list(" ".join(text2).lower()),
        2, -1, -.5, -.1, gap_char=['-'],
        one_alignment_only=True)

    if not alignments:
        return False

    dashed2 = alignments[0][0]
    dashed1 = alignments[0][1]
    alignment_score = alignments[0][2]

    # translate to dashed
    match_text = []
    match_density = []
    i_glob = 0

    # compute for each matched word a density, how well it fits based on the biopython alignment

    # go through the single words in the text, to match on
    for i, w in enumerate(text1):
        lw = list(w)

        # go through the single word
        for j, c in enumerate(w):
            try:
                # if its not matching, marked by a '-' dash, then shift the position in the dashed biopython result
                while j + i_glob < len(dashed2)-3 and dashed2[j + i_glob] == '-':
                    i_glob += 1

                if dashed1[j + i_glob] == '-':
                    lw[j] = dashed1[j + i_glob]
            except:
                # Todo, find out, why this gets to big, but it's not soo important
                pass

        if len(w) != 0:
            match_density.append((len(lw) - lw.count('-')) / len(lw))
        else:
            match_density.append(0.0)

        match_text.append("".join(lw))

        i_glob += len(w) + 1


    assert (len(text1) == len(match_text))
    assert (len(text1) == len(match_density))

    if max(match_density)<1:
        return False

    start, stop = left_right_encircle(match_density)

    if ignore_order:
        start = translation_list1[start]
        stop = translation_list1[stop]
    return start, stop, alignment_score


def match_word_strings(text1, text2):
    ''' This function matches two lists of words, depending on a fuzzy match of their words

    It it used for faster matching. It only starts the expensive matching with biopython, if there is some
    probability to find a good match. This decision is based, if there is not a bad fuzzy match.

    '''

    if not text1 or not text2:
        return None

    fit_score = ratio(" ".join(text1).lower(), " ".join(text2).lower())
    if fit_score:
        m =  match_with_biopython(text1, text2)
        if m:
            start, stop, alignment_score = match_with_biopython(text1, text2)
            length = stop-start
            return start, stop, alignment_score
        else:
            return None
    else:
        return None

def list_memoizer(func):

    mem = {}

    @wraps(func)
    def wrapped(*args, **kwargs):
        key = tuple((args, tuple(kwargs)))
        if key not in mem:
            mem[key] = []
            res = func(*args, **kwargs)
            if isinstance(res, Iterable):
                mem[key][:] = res
            else:
                mem[key] = res
        return mem[key]

    return wrapped



def doc_from_indexed_doc(doc, i_s):
    np_array = doc.to_array([LOWER, POS, ENT_TYPE, IS_ALPHA])
    np_array_2 = np_array[i_s]
    doc2 = Doc(doc.vocab, words=[t.text for i, t in enumerate(doc) if i in i_s])
    doc2.from_array([LOWER, POS, ENT_TYPE, IS_ALPHA], np_array_2)
    return doc2

@list_memoizer
def wmd_similarity(span1, span2):
    if not span1.vector_norm or not span2.vector_norm:
        logging.error('Spacy tries to compute similarity on non vectorized word in %s' % str((span1, span2)))
        return 0
    if not span1 or not span2:
        return 0
    try:
        return span1.similarity(span2)
    except ZeroDivisionError:
        logging.error('Spacy tries to compute similarity on strange vectorized word, fallback to biobython')
        span1.similarity(span2)
        text1 = [x.lemma_ for x in span1]
        text2 = [x.lemma_ for x in span2]
        return match_with_biopython(text1, text2)



#@list_memoizer
def find_border (hay_doc=None, needle_doc=None):
    if not hay_doc or not needle_doc:
        raise ValueError('Empty doc for hay_doc or needle_doc!')

    if len(needle_doc) < len(hay_doc)*0.5:
        confs = []
        for p in range (len(hay_doc)-len(needle_doc)):
            conf = needle_doc.similarity(hay_doc[p:p+len(needle_doc)])
            confs.append((p, conf))
        best = max(confs, key=lambda x: x[1])
        return best[0], best[0]+len(needle_doc), best[1]

    l_steps, r_steps = iter(range(len(hay_doc))), iter(range(len(hay_doc), -1, -1))

    l = next(l_steps)
    r = next(r_steps)
    max_sim = wmd_similarity(hay_doc[l:r], needle_doc)
    best = False
    left_shift = True
    right_shift = True
    while not best:
        #print (hay_doc[l:r])
        if left_shift and l < len(hay_doc)-1:
            try:
                l_next = next(l_steps)
            except StopIteration:
                return l,r
            new_sim_l = max ([wmd_similarity(hay_doc[l_next:r], needle_doc), wmd_similarity(hay_doc[l_next + (r-l_next)/2:r], needle_doc)])
            if new_sim_l < max_sim:
                left_shift = False
            else:
                l = l_next
                max_sim = new_sim_l
        else:
            left_shift = False
        if right_shift and r > -1:
            try:
                r_next = next(r_steps)
            except StopIteration:
                return l, r, max_sim
            new_sim_r = max([wmd_similarity(hay_doc[l:r_next], needle_doc), wmd_similarity(hay_doc[l:r_next - (r_next-l)/2], needle_doc)])
            if new_sim_r < max_sim:
                right_shift = False
            else:
                r = r_next
                max_sim = new_sim_r
        else:
            right_shift = False
        if not left_shift and not right_shift:
            best = True

    return l, r, max_sim


import wmd
from token_parsing import nlp
nlp.add_pipe(wmd.WMD.SpacySimilarityHook(nlp), last=True)


def doc_sample(text):
    return nlp(text)


def doc_from_tokens(tokens_spacy):
    if isinstance(tokens_spacy[0], Tok):
        i_s = [v['i'] for v in tokens_spacy]
        doc = doc_from_indexed_doc(tokens_spacy[0]['spacy'].doc, i_s)
    else:
        i_s = [v.i for v in tokens_spacy]
        doc = doc_from_indexed_doc(tokens_spacy[0].doc, i_s)
    return doc


#@list_memoizer
def match_by_embeddings (hay_doc=None, needle_doc=None):
    """

    >>> needle_doc = doc_sample("cardiomyopathy")
    >>> hay_doc = doc_sample('heart failure can cause symptom such as swollen ankle , fatigue , trouble breathing , low cardiac output , palpitation and a feeling of faintness , cardiomyopathy be not limited to exercise')
    >>> match_by_embeddings(hay_doc, needle_doc)
    [26, 27, 1.0]

    >>> needle_doc = doc_sample("heart failure")
    >>> match_by_embeddings(hay_doc, needle_doc)
    [0, 2, 1.0]

    :param doc11:
    :param doc22:
    :return:
    """
    if not hay_doc or not needle_doc:
        print('one of the strings is empty!')
        return 0, 0, 0

    try:
        hay_doc = doc_from_tokens(hay_doc)
        needle_doc = doc_from_tokens(needle_doc)

        # shortcut for pure text
        needle_text = [t.lemma_ for t in needle_doc]
        hay_text    = [t.lemma_ for t in hay_doc]
        if all(l in hay_text for l in needle_text):
            indices = []
            for l in needle_text:
                indices.append(hay_text.index(l))

            if sorted(indices) == list(range(min(indices), max(indices)+1)):
                return min(indices), max(indices)+1, 1.0

        start, stop, conf = find_border(hay_doc=hay_doc, needle_doc=needle_doc)

        conf = round(conf, 2)
    except ZeroDivisionError:
        logging.error('Obscure Zero Division generating spacy span')
        start, stop, conf = 0, 0, 0

    return start, stop, conf




