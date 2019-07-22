import coloredlogs

from tok import Tok

coloredlogs.install()
import logging
logging.getLogger().setLevel(logging.INFO)

import itertools

import parsley
from ometa.runtime import EOFError, ParseError
from string_matcher import match_word_strings, match_by_embeddings

from helpers.nested_dict_tools import reverseDict
from helpers.time_tools import timeit_context

def maxelements(seq): # @SilentGhost
    ''' Return list of position(s) of largest element '''
    m = max(seq)
    return [i for i, j in enumerate(seq) if j == m]

from grammar import grammar
import grammar_funs
import coref_resolver


class probsyntgreed_parser:
    def __init__(self):
        self.parser_globals = {'myself': self,
                               'grammar_functions': grammar_funs}
        self.parser = parsley.makeGrammar(
               grammar,
               self.parser_globals
           )
        self.parser_globals.update({'parser': self.parser})



    def parse(self, tokens, rule):
        return self.parser(tokens).__getattr__(rule)()

    def match (self, tokens, match_dict, rule='text'):
        self.tokens = tokens
        self.layers = set()

        best_annotations_all_layers = []
        self.len_set_ids = len(match_dict)
        self.match_dict = match_dict

        # Iterate through difference-aspect sets
        for    self.set_id, self.to_match_phrases_embeddings    in    enumerate(match_dict):
            logging.info ('parsing %s' % str
                          (self.to_match_phrases_embeddings))

            with timeit_context('parsing') as t:
                try:
                    all_possible_annotations = self.parse(self.tokens, rule=rule)
                    if rule=='text':
                        best_annotations = self.argmax_score(all_possible_annotations)
                    else:
                        best_annotations = all_possible_annotations
                except EOFError:
                    raise
                    logging.error ("Some tokens until the end of the text could not be matched.")
                    continue
                except ParseError:
                    raise
                    logging.error("Error in grammar definition!")
                    continue
            best_annotations_all_layers.append(best_annotations)
        return best_annotations_all_layers

    def update_start_end_token(self, toks, keys, **kwargs):
        conf = kwargs['conf']
        toks[0].update_token(start_end=True, keys=keys, conf=conf)
        toks[-1].update_token(start_end=False, keys=keys, conf=conf)

    def update_every_token(self, toks, keys, **kwargs):
        conf = kwargs['conf']
        for tok in toks:
            tok.update_token(start_end=True, keys=keys, conf=conf)

    def annotate_tagml(self, tokens_to_annotate):
        import alexandria_wrapper.tagml
        for d in tokens_to_annotate:
            reverseDict(d, end_key='annotations', extra_keys=['conf'], call=self.update_start_end_token)
        new_text = " ".join([tok.tagml_repr() for tok in self.tokens])
        tagml = tagml.writer.wrap_with_tagml_tags(keys=['TAGML'], content=new_text)
        return tagml

    def annotate_conll03_all(self, tokens_to_annotate):
        for d in tokens_to_annotate:
            reverseDict(d, end_key='annotations', extra_keys=['conf'], call=self.update_every_token)
        conll_line = "\n".join([t.conll03_repr() for t in self.tokens])
        return conll_line

    def relabel_annotations(self, annotation_dicts=None, side=None, extra_label=None):
        diffd = annotation_dicts[side]
        old_diffd_items = list(diffd.items())
        # copying, because iteration over modified dict won't work

        for key, annotation in old_diffd_items:
            new_key = key + extra_label
            diffd[new_key] = diffd[key]
            del diffd[key]
        return diffd

    def delete_annotations(self, diffd, labels):
        old_diffd_items = list(diffd.items())
        # copying, because iteration over modified dict won't work

        for side, annotations in old_diffd_items:
            old_annotations_items = list(annotations.items())
            for kind, annotation in old_annotations_items:
                if kind in labels:
                    del diffd[side][kind]
        return diffd

    def annotate_conll03_single(self, tokens_to_annotate, grammar_tester, text):

        conll_lines = []
        for d_no, d in enumerate(tokens_to_annotate):
            grammar_tester.add_sample(text, self.match_dict[d_no], number=d_no)

            difference_dict = list(d.values())[0]
            if not all(side in difference_dict for side in ['s0', 's1']):
                grammar_tester.add_comment('annotation missing a side')
                logging.error ('annotation missing a side')
                continue

            annotation_occurrences =[what in annotation for what in ['subject', 'contrast'] for annotation in difference_dict.values()]
            if not all(annotation_occurrences) or len(annotation_occurrences)!=4:
                grammar_tester.add_comment('annotation missing a match')
                logging.error ('annotation missing a match')
                continue

            if len(difference_dict['s0']['subject']['annotations']) < 1  or len(difference_dict['s1']['subject']['annotations']) <  1 or \
               len(difference_dict['s0']['contrast']['annotations']) < 1 or len(difference_dict['s1']['contrast']['annotations']) < 1:
                grammar_tester.add_comment('annotation is empty')
                logging.error('annotation is empty')
                continue

            min_conf = 2.5
            if difference_dict['s0']['subject']['conf']  < min_conf   or   difference_dict['s1']['subject']['conf'] < min_conf:
                grammar_tester.add_comment('annotation is not safe enough')
                logging.error('annotation is not safe enough')
                continue

            i1 = difference_dict['s0']['subject']['annotations'][0]['i']
            i2 = difference_dict['s1']['subject']['annotations'][0]['i']
            il = min([i1,i2])
            ir = max([i1,i2])

            if i1 < i2:
                first_side = 's0'
                second_side = 's1'
            else:
                first_side = 's1'
                second_side = 's0'

            self.delete_annotations (difference_dict, labels=['aspect'])
            self.relabel_annotations (difference_dict, side=first_side, extra_label='_A')
            self.relabel_annotations (difference_dict, side=second_side, extra_label='_B')


            if il>len(self.tokens) or ir> len(self.tokens):
                grammar_tester.add_comment('annotation exceeds text')
                logging.error('annotation exceeds text')
                continue

            # Find left corner
            for i in range(il-1,-1, -1):
                print (i)
                if self.tokens[i]['text'] == '.':
                    il = i+1
                    break

            # Find right corner
            for i in range(ir, len(self.tokens)):
                if self.tokens[i]['text'] == '.':
                    ir = i
                    break

            if len([i for i in range (il, ir) if self.tokens[i]['text'] == '.']) > 2:
                grammar_tester.add_comment('annotation spans more than two sentences')
                logging.error ('annotation spans more than two sentences')
                continue

            if ir - ir > 30:
                grammar_tester.add_comment('annotation too long to be realistic')
                logging.error ('annotation too long to be realistic')
                continue

            reverseDict(d, end_key='annotations', extra_keys=['conf'], call=self.update_every_token)
            Tok.conll03_layer_repr.dependenceA = False
            Tok.conll03_layer_repr.dependenceB = False
            conll_line = "\n".join([t.conll03_layer_repr(layer=d_no) for t in self.tokens[il:ir+1]] + ['\n'])
            conll_lines.append(conll_line)
            grammar_tester.add_comment('good annotation')

        conll_line = "\n".join(conll_lines)
        return conll_line


    def idx_list(self, l, idx):
        return [t for t in l if t['i'] in idx]

    def assign_to(self, key, val):
        self.layers.add(str(key) + str(val))
        return str(key) + str(val)

    def tokens_expansions(self, yet_parsed):
        tokens = list(set(itertools.chain.from_iterable([a1a2 for a1a2, yet in yet_parsed])))
        tokens =  sorted(tokens, key=lambda x: x['i'])
        expansions = [yet for a1a2, yet in yet_parsed]
        return  {
                'difference': tokens,
                'expansion': expansions
                }

    def marker_annotation(self, name, tokens):
        ''' Annotation the markers with name, tokens and confidence of 1

        It's a tuple, representing non-existing interpretations
        '''
        return {
            'marker': name,
            'tokens': tokens,
            'conf'  : 1}


    def get_to_match(self, side_no=None, what=None):
        return self.to_match_phrases_embeddings[side_no][what]

    def generate_dummy_solution(self, record, min_sol):
        if not min_sol:
            return ( 0, len(record)-1, None, -1, len(record)-1)
        else:
            return (0, 0, None, -1, 0)

    def delimit_by_match(
            self,
            search_in = None,
            what = None,
            basic_factor=1,
            cant_fail=False,
            side_constraint=None,
            min_sol=False):
        """ Match some input to a given construction from strings with respect to other spellings and lacks within
        the input.

        That means, if you want to match from a set of six interrelated labels, this function chooses the one, that
        fits in this position.

        Say, if there are three kinds of labels: 'subject', 'aspect', 'contrast'     (called what)
             and they are interellated to another 'subject', 'aspect' and 'contrast' (called side)

        It has the capability of working with lacks within the input, that has to be regarded while matching.
        If you have some input like this:

        >>> text = "Mammals except dolphins and whales live on dry land or they are not the only animals on earth"

        And you want to match:

        >>> to_look_for = "Mammals live on Mainland"

        You can first parse "except dolphines and whales" as something, that has to be excluded from the outer matching.
        In the end you match:

        >>> match_dict = ( \
                           {'some_wanted_info':        "Fish live only in water", \
                           'subject' :  'Fish and chips'}, \
                           {'some_wanted_info':        "Mammals live on Mainland", \
                           'subject'    :             "dolphins and whales"} \
                            )

        Prepare the text and matching data to obtain some structured data...
        >>> from token_parsing import prepare_text, prepare_labels
        >>> from probsyntgreed_parsing import probsyntgreed_parser
        >>> tokens = prepare_text(text)
        >>> match_dict = prepare_labels([match_dict])

        Call the parser on the rule that is used to generate the expansions before operating with this function
        >>> parser = probsyntgreed_parser(tokens)
        >>> rule = 'expanded_text'
        >>> search_in = parser.match(match_dict=match_dict, rule=rule)
        >>> search_in
        [(['Mammals', 'live', 'on', 'dry', 'land', 'or', 'they', 'are', 'not', 'the', 'only', 'animals', 'on', 'earth'], {'s1': {'subject': {'annotation': ['dolphins', 'and', 'whales'], 'conf': 34.0}}})]

        This is the record, that can be used to search in it, the dict in this list-tuple, is information that is yet parsed, this
        can is forwarded by this function, only working on the first list of tokens.

        See that the tokens between 'Mammals' and 'live' are missing in this representation.

        Now calling `delimit_by_match` produces:
        >>> res = parser.delimit_by_match(search_in=search_in[0], what='some_wanted_info')
        >>> from pprint import pprint
        >>> pprint(res)
        {'conf': 36.39999999999999,
         'idx': [0, 5, 6, 7, 8],
         'len': 5,
         'len_expr': 14,
         'pos': 0,
         'side': 1,
         'yet': {'s1': {'subject': {'annotation': ['dolphins', 'and', 'whales'],
                                    'conf': 34.0}}}}

        This result means, that with a confidence of 36.4, the tokens with ids [0, 5, 6, 7, 8] should be annotated and
        they are 5 tokens, starting from position 0. And this annotation is taken from the construction set side 1.

        >>> [t for t in tokens if t['i'] in res['idx']]
        ['Mammals', 'live', 'on', 'dry', 'land']

        :param what:            what label to match here to
        :param side_constraint: what side of the label construction to match here to

        :param search_in:       what to match onto
        :param basic_factor:    score multiplyer for the confidence, if you want to rate 'subject' over 'contrast'
        :param cant_fail:       if the match fails, stipulate a parse error or pass
        :return: dict with keys:
                {"pos": where to start,
                 "len": where to stop,
                 "idx" : set of indices (good if there are lacks in the match, by lacks in the search_in-record,
                 "side": the index of the construction set list index taken the match from,
                 "conf": confidence, that is this annotation to be made,
                 "len_expr": len_expressions length of the original expression to match}
        """

        # choose the annotation directives by side and kind
        if not (search_in):
            return False

        what_to_fit_from = {i:side[what]
                            for i, side in enumerate(self.to_match_phrases_embeddings)
                            if not side_constraint or isinstance(side_constraint, str) or i in side_constraint}

        # bin for results to compare maximizing score
        choices = []

        # coreference resolution on the text
        solving_record, coref_translate_dict = coref_resolver.coref_translate(search_in [:])

        # determin the string to match onto and its len
        text1 = ([tok.lemma_.lower().replace('-', '') for tok in solving_record])
        len_expressions = len(solving_record)

        # iterate through sets to match possibly from and save all these solutions, whether they are good or bad
        for side, phrase_to_match in what_to_fit_from.items():

            # if phrase to match is missing, create dummy solution
            if phrase_to_match == None:
                choices.append(self.generate_dummy_solution(solving_record, min_sol=min_sol))
                continue

            text2 = ([tok['lemma_'].lower().replace('-', '')
                      for tok in phrase_to_match])

            m = match_by_embeddings (hay_doc=tuple(solving_record), needle_doc=tuple(phrase_to_match))
            if m:
                l_pos, r_pos, conf = m
                choices.append((l_pos, r_pos, conf * basic_factor, side, (text1, text2)))

        # If nothing greatly fitting was found, decide whether to stipulate parsley to work on something else
        # or to be ok with a dummy solution
        if not choices:
            if not cant_fail:
                return False
            else:
                return self.generate_dummy_solution(solving_record, min_sol=min_sol)

        try:
            choices = [
                {
                    'start':  coref_resolver.coref_retranslate(l_pos_, coref_translate_dict),
                    'stop':   coref_resolver.coref_retranslate(r_pos_, coref_translate_dict),
                    'conf':   conf,
                    'side':   side,
                    'what':   what,
                    'tokens': [search_in[coref_resolver.coref_retranslate(p, coref_translate_dict)] for p in range(l_pos_,r_pos_)]
                }
                for l_pos_, r_pos_, conf, side, _ in choices]
        except TypeError:
            print (coref_resolver.coref_translate(search_in[:]))
            raise
        except IndexError:

            print (coref_resolver.coref_translate(search_in[:]))
            raise
        return choices

    def exclude_sides(self, sides, side_constraint):
        return [s for s in sides if s[0] not in side_constraint]

    def compute_conf_from_solution(self, solution):
        side_confs = []
        try:
            for choice in solution[1]:
                side_confs.append (self.recursive_conf_optimizer(choice))
            return sum(side_confs)
        except TypeError:
            x=1
            raise

    def best_of (self, choice_construction, interpretation=0, side_constraint=[]):
        # Solution without markers
        # ========================
        if isinstance(choice_construction, str):
            raise ValueError("choice construction is string")

        conf = 0
        side = None
        unmarked_solution = None

        # Try sorting the sides again, sometimes they get shuffled
        if 'difference' in choice_construction and choice_construction['difference']:
            try:
                zipped = zip(*choice_construction['difference'])
            except TypeError:
                raise
            except KeyError:
                raise

            sides = list(enumerate([choice for i, choice in enumerate(zipped)]))

            if side_constraint:
                sides = self.exclude_sides(sides, side_constraint)

            confs_sides = [(self.compute_conf_from_solution(x), x) for x in sides]

            if not confs_sides:
                raise ValueError('Got empty sequence to compare')
            conf_side = max(confs_sides, key=
                  lambda x: self.compute_conf_from_solution(x[1]))

            conf, side_solution = conf_side
            side, unmarked_solution = side_solution

        # Solution within markers
        # =======================
        marked_solution = []
        markers = []
        try:
            if choice_construction['expansion']:
                for annotation in choice_construction['expansion']:
                    if 'marker' in annotation:
                        markers.append(annotation)
                    else:
                        try:
                            if any(annotation):
                                m = self.best_of(annotation, side_constraint=[side])
                                yet_conf, yet_side, yet_interpretation, yet_unmarked_solution, yet_marked_solution, yet_markers = m
                                marked_solution.append((yet_side, yet_unmarked_solution))
                                markers.extend(yet_markers)
                        except:
                            raise
        except TypeError:
            raise

        return conf, side, interpretation, unmarked_solution, marked_solution, markers

    def best_len(self, dicts):
        try:
            best = self.best_of({'difference': [dicts], 'expansion': []})
            res_len = best [3][0]['stop']
        except KeyError:
            logging.error('Grammar internal type error')
            return False
        return res_len

    def argmax_score(self, dicts):
        seen_sides = []
        seen_interpretations = []

        how_many_to_match = len(self.to_match_phrases_embeddings)
        len_dicts = len(dicts)
        #range_fits = [1 - abs(self.set_id / self.len_set_ids - i / len_dicts) for i, d in enumerate(dicts)]

        solutions = []
        markers = []
        while len(solutions) < how_many_to_match:
            conf_side_interpretation_annotation = []
            for interpretation, d in enumerate(dicts):
                if interpretation not in seen_interpretations:
                    conf_side_interpretation_annotation.append(
                        self.best_of(
                            choice_construction=d,
                            interpretation=interpretation,
                            side_constraint=seen_sides
                        )
                    )
            if not conf_side_interpretation_annotation:
                logging.error('Empty interpretation dicts')
                return {}
            m  = max (conf_side_interpretation_annotation, key=lambda x: x[0])
            conf, side, interpretation, unmarked_annotation, marked_annotation, marker = m
            seen_sides.append(side)
            seen_interpretations.append(interpretation)
            solutions.append((side, unmarked_annotation))
            solutions.extend(marked_annotation)
            markers.extend(marker)

        res = \
        {
            self.assign_to('d', self.set_id):
                {
                    self.assign_to('s', side):
                        {
                            annotation['what']:
                                {
                                    'annotations': annotation['tokens'],
                                    'conf': annotation['conf']
                                }
                            for annotation in annotations if isinstance(annotation, dict)
                        }
                    for side, annotations in solutions if isinstance(side, int)
                }
        }

        res['markers']= markers

        return res


    def recursive_conf_optimizer(self, choice):
        if 'expansion' in choice and choice['expansion']:
            return self.best_of(choice['expansion'])
        else:
            if choice['conf'] == None:
                return 0
            return choice['conf']


