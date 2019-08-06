from collections import OrderedDict

coref_pos = ['DET']

def coref_translate(tokens):
    """ Translates a list of tokens into a coreference resolved list of tokens.

    After some operations on the tokens with resolved coreferential bindings are done, the resultant positions
    can be retranslated with `coref_retranslate(indices)`

    :param tokens: list of tokens with optinally neuralcoref annotations
    :return: coref resolved token list
    """
    if not tokens:
        raise ValueError ('Can\'t corefresolve empty sequence')
    new_record = []
    pos_dict = OrderedDict()
    dist = 0
    for i, token in enumerate(tokens):
        if False and token['spacy']._.in_coref and token['pos_'] in coref_pos and token['dep_'] not in ['det']:
            main_cluster = list(token['spacy']._.coref_clusters[0].main)
            new_record.extend(main_cluster)
            dist += len(main_cluster) -1
            for virtual_i in range(len(main_cluster)+1):
                pos_dict[i + virtual_i] = i
        else:
            new_record.append(token['spacy'])
            pos_dict[i + dist] = i

    typ = type(new_record[0])
    assert (all(isinstance(t, typ) for t in new_record))
    return new_record, pos_dict


def coref_retranslate(pos, pos_dict):
    """ Translates list of indices of coreference resolved token list back to indices of non-resolved tokenlist.
    Must be called after coref_translate.

    :param pos:
    :param pos_dict:
    :return:
    """
    try:
        if pos not in pos_dict:
            return pos_dict[pos - 1] + 1
        else:
            return pos_dict[pos]
    except KeyError:
        ValueError('Coudn\'t map coreference position %d backwards in %s' % (pos, str(pos_dict)))
        return 0