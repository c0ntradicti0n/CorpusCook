#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random

import unicodedata

from helpers import nested_dict_tools

logging.getLogger().setLevel(logging.INFO)

import itertools
import operator
import numpy as np
import pprint
import addict

from bs4 import BeautifulSoup
from bs4 import NavigableString
from lxml.html.clean import Cleaner

import re
from nltk import flatten

from helpers.os_tools import *
import sys
sys.setrecursionlimit(5000) # for pickle
import pickle

from config import *

def pairwise(iterable):
    ''' 's -> (s0, s1), (s2, s3), (s4, s5), ... '''
    a = iter(iterable)
    return zip(a, a)

def tags_until_in (l, string):
    ''' from list of tags with NavStrings, cut this list after some element

    :param l:
    :param string:
    :return:
    '''
    for e in l:
        if isinstance(e, str) and string in e:
            yield NavigableString(e.split(string)[0])
            break
        yield e

def get_next (it, name):
    ''' get next element of the same kind '''
    for i in it:
        if i.name == name:
            return i
    else:
        return None


class DifferenceBetweenHtmlParser:
    def __init__(self,
                 input_dir,
                 process_dir,
                 output_dir,
                 input_html_file_filter,
                 tablepicture_data = True):
        self.input_dir = input_dir
        self.process_dir = output_dir
        self.output_dir = process_dir
        self.input_html_file_filter = input_html_file_filter
        self.tablepicture_data = tablepicture_data

    def zoom_to_real_html (self, html_snippet):
        ''' navigate to a the document containing tag '''
        if hasattr(html_snippet, 'name') and html_snippet.name in ['html', 'body', '[document]','div']:
            return list(self.zoom_to_real_html(list(html_snippet.children)))
        elif isinstance(html_snippet, list):
            return [self.zoom_to_real_html(t) for t in html_snippet]
        else:
            return [html_snippet]

    def split_subdivision_list (self, list_of_tags, conditional_tags):
        ''' split a list of anything based on a lambda, so that the splitting element is the first of each group '''
        groups = (list(g) for k, g in itertools.groupby(list_of_tags[::-1], lambda item: item.name in conditional_tags))
        reversed_groups =  (list(itertools.starmap(operator.add, zip(*[groups] * 2))))
        return [l[::-1] for l in reversed_groups[::-1]]


    def parse_tables (self, table_tags):
        ''' read tables into distinction list pattern '''
        for tag in table_tags:
            tab = np.array(
                [[td.get_text(strip=True) for td in tr.find_all('td') if td]
                for tr in tag.find_all('tr')]
                )
            yield tab

    def is_ocr_parsed_file(self, path, input_dir):
        ''' read ocr results from certain file in distinction list pattern '''
        textified = input_dir+  path + textified_extension
        if os.path.exists(textified) and os.path.getsize(textified) > 100:
            with open(textified, 'r') as f:
                return eval(f.read().replace('\n', ''))

    def parse_difference_between_table_pictures (self, image_tags, input_dir):
        ''' read ocr for every image tag '''
        for tag in image_tags:
            yield self.is_ocr_parsed_file(os.path.basename(tag['src']), input_dir)

    def entities_from (self, heading_string):
        ''' parse title to subject x and y '''
        # todo 'Differnece between Causes & Cure of Trade Cycle– Keynesian & Hayekian Views', 'Difference between Impeach, Veto, or Recall of a President'

        heading_string = re.sub('[\u202F\u00A0]', " ", heading_string) ## ... vs|VS ... -- lalala,     ...... x,y, and|or z
        m = re.match (r""".*([Dd]i?f[f]?eren[c]?e[s]?|Comparison) ([bB]etwee[nm]\s+(?P<a>.+) )?([Aa][Nn][Dd]|vs\.|&) (?P<b>.+)""", heading_string)
        try:
            return m['a'], m['b']
        except:
            return None

    def make_children_and_parents (self, groups):
        ''' the grouped headings with their content are beforehand a list of heading tags and following content,
        this finds the hierarchy based on the sequence and depth of the tags

        :param groups: list of dicts with heading tags first
        :return: dictionary with indices of the groups, which key is hierarchichally superior to the values
        '''
        d = addict.Dict()
        for parent_i, group in enumerate(groups[:-1]):
            this_depth      = self.tag_no_of_first(group)
            following_depth = self.tag_no_of_first(groups[parent_i + 1])
            matches =  this_depth == following_depth -1
            if matches:
                d[parent_i] = [parent_i+1]
                for n in range(2, len(groups) - parent_i - 1):
                    follower_of_follower = self.tag_no_of_first(groups[parent_i + n])
                    matches_again = following_depth == follower_of_follower
                    if matches_again:
                        d[parent_i].extend([parent_i + n])
                    else:
                        break
        return d


    def sanitize(self, dirty_html):
        ''' The html needs to be cleaned from cluttering tags '''
        cleaner = Cleaner(page_structure=True,
                      meta=True,
                      embedded=True,
                      links=True,
                      style=True,
                      processing_instructions=True,
                      inline_style=True,
                      scripts=True,
                      javascript=True,
                      comments=True,
                      frames=True,
                      forms=True,
                      annoying_tags=True,
                      remove_unknown_tags=True,
                      safe_attrs_only=True,
                      safe_attrs=frozenset(['src','color', 'href', 'title', 'class', 'name', 'id']),
                      remove_tags=('span', 'font', 'ul', 'li', 'ol','div','a', 'label', 'p', 'header', 'ins',  'time', 'article', 'aside')
                      )

        return cleaner.clean_html(dirty_html)


    header_re = re.compile("((?P<tag_name>\w)(?P<tag_no>\d)|(?P<strong>strong))")
    def tag_no_of_first (self, group):
        ''' how to treat non-numbered-heading tags in the hierarchy like 'strong'?
        string is pyt between h4 and h5
        '''
        assert group[0].name in self.heading_tags
        m = self.header_re.match(group[0].name).groupdict()
        if m['strong']:
            return 4
        if m['tag_name'] and m['tag_no']:
            return int(m['tag_no'])
        return 10


    def extract_dictintion_annotations (self, title, tables, images):
        ''' Collect abstracted information,that is given in the document

        :param title: Title of the page
        :param tables: content of table-tags
        :param images: content of ocr-read images
        :return:
        '''
        subjects = self.entities_from(title)
        aspects_constrastives = self.extract_aspects_contrastives(tables, images)
        return subjects, aspects_constrastives


    def join_group (self, g):
        ''' join list of tags to a string

        :param g: some list pf tags
        :return: string
        '''
        return " ".join(t.get_text() if hasattr(t, 'get_text') else t for t in g).strip()

    def denewline(self, string):
        ''' join list of tags to a string

        :param g: some list pf tags
        :return: string
        '''
        return  re.sub(r'\n{2, 10}', '', string).strip()

    def extract_differencebetween_paragraph (self, groups, dependence_dict):
        ''' Get the important paragraph and its subheadings, returns two versions:

        :param groups: list of tags, first one is a heading
        :param dependence_dict: dependence of these heading structures
        :return: tuple of full text   and    list of tuples with headings and text, bot as string

        '''
        db_header_tags = groups[0][0].parent.find_all(self.heading_tags[1:], text=re.compile(r'([dD]ifference| vs\.? )'))
        if not db_header_tags:
            logging.warning('No distinction paragraph here, that can be recognized by heading!')
            try:
                return self.join_group(groups[1][2:]), None
            except IndexError:
                return None, None


        for i, group in enumerate(groups):
            if group[0] in db_header_tags:
                sub_paragraphs = [groups[x] for x in dependence_dict[i]]
                subheadings = [(db_group[0].text, self.denewline(self.join_group(db_group[1:]).strip())) for db_group in sub_paragraphs]
                combined_text = "\n".join (g[1] for g in subheadings)
                return combined_text, subheadings

    def extract_aspects_contrastives(self, tables, images):
        ''' aspects are common point of view, that the contrast is seen from

        For example, if we have a distinction between Ego and Self Respect, this can be distinguished
        on the aspect of the 'underlying feeling':
        'Ego' features as its contrastive definition 'pride, insecurity, self-doubt'.
        In contrast 'Self Respect' featrues 'underlying causes' as contrastive definition.

        This is collected from the tabular information.
        If no aspect is given, it is set to 'no_aspect'
        '''

        try:
            aspects_contrastives = []
            if tables:
                for tab in tables:
                    if len(tab) > 1 and  len(tab[0]) == 1 and len(tab[1]) == 2:
                        aspects_contrastives.extend([[*a, *cs] for a, cs in pairwise(tab.tolist())])

                    if len(tab.shape) > 1:
                        if tab.shape[1] == 3:
                            # First row is heading
                            aspects_contrastives.extend([tab[n,:].tolist() for n in range (1,tab.shape[0])])
                        if tab.shape[1] == 2:
                            # First row is heading
                            aspects_contrastives.extend([["NO_ASPECT"] + tab[n,:].tolist() for n in range (1,tab.shape[0])])

            if images:
                for img in images:
                    if isinstance(img, dict):
                        img = np.array(list(img.values()))
                    if isinstance(img, list):
                        img = np.array(list(img))
                    # If there are three columns, we have contrastives and aspects
                    if img.shape[1] == 3:
                        # First row is heading
                        aspects_contrastives.extend([img[n,:].tolist() for n in range (1,img.shape[0])])
                    if img.shape[1] == 2:
                    # First row is heading
                        aspects_contrastives.extend([["NO_ASPECT"] + img[n,:].tolist() for n in range (1,img.shape[0])])

        except IndexError:
            raise
            logging.error('table or image has not enough cols or rows')
        return [[p.lower() for p in s] for s in aspects_contrastives]

    # What are headings?
    heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong']
    # What kind of headings are meaningless to us?
    unwanted_headings =  \
        re.compile(r'(.*Search DifferenceBetween\.net.*|'
                     r'.*Comment.*|.*References.*|'
                     r'.*See more about.*|'
                     r'.*Get New Comparisons in your inbox.*|'
                     r'.*Most Emailed Comparisons.*|'
                     r'.*Editor.s Picks.*|'
                     r'.*More in.*|'
                     r'.*Editor.s Picks.*|'
                     r'.*Follow Us.*|'
                     r'Related posts.+|'
                     r'Leave a Reply)')
    def process(self, path):
        ''' HTML cleaning and extracting the wanted difference-information from the page

        :param path: where to look for the html
        :return: dictionary with        with open(gold_path, 'w') as f:
            f.write(str(res)) abstacted difference information, nested dict with tuples of headings and headings
            corresponding to the heading hierarchy
        '''

        with open(path) as fp:
            html = fp.read()

        soup = BeautifulSoup(html, features="lxml")
        post = soup.select_one("body")
        post = BeautifulSoup(self.sanitize(str(post)), features='lxml')

        try:
            title = soup.select_one("h1.posttitle").text
        except AttributeError:
            logging.error('Page %s with no title' % path)
            return None

        # find, extract and decompose all tables/pictures with tables
        table_tags = post.find_all('table')
        tables = list(self.parse_tables(table_tags))
        image_tags = post.find_all('img')
        images = list(x for x in self.parse_difference_between_table_pictures(image_tags, input_dir=input_dir) if x)
        for t in table_tags + image_tags:
            t.decompose()

        # Split whole html body into groups to generate a table of contents
        tag_list = flatten(self.zoom_to_real_html(post))
        # Cut list of tags/strings on information about the article itself
        tag_list = list(tags_until_in(tag_list, 'About Latest Posts'))
        groups   = self.split_subdivision_list(tag_list, self.heading_tags)

        # eliminate elements and groups, that govern groups with just propaganda headings
        for elem in post(
            self.heading_tags,
            text=self.unwanted_headings
            ):
            try:
                elem.decompose()
            except AttributeError:
                logging.error('deleting unwanted sections failed')
        groups = [group for group in groups if not group[0].name == None ] # Take all groups without that empty tag

        # generate subdivision structure of the table of contents
        dependence_dict = self.make_children_and_parents (groups)

        # Find the paragraph, where differences are presented
        try:
            difference_text, sub_headings_difference = self.extract_differencebetween_paragraph (groups, dependence_dict)
            difference_text = re.sub(r'\n{2, 10}', '', difference_text)
        except TypeError:
            logging.error ('no difference between paragraphs for %s' % path)
            return None

        # extract the abstracted information
        subjects, aspects_contrastives = self.extract_dictintion_annotations(title=title, tables=tables, images=images)

        # number of distinctions needed to multiply the strings of the different aspect information of x,y
        no_distinctions = len(aspects_contrastives)
        distinctions_list = list(zip([subjects] * no_distinctions, aspects_contrastives))
        try:
            dictinction_patterns = [
                (
                    {'subject': d_cell[0][0], 'contrast':d_cell[1][1], 'aspect' :d_cell[1][0]},
                    {'subject': d_cell[0][1], 'contrast':d_cell[1][2], 'aspect' :d_cell[1][0]}
                )   for d_cell in distinctions_list
            ]
        except:
            logging.error ('Strange shape of distinction pattern! There seems to be no for %s' % path)
            return None


        res = {
                'path'    : path,
                'title'   : title,
                'difference_text'          : difference_text,
                'subdivion_difference_text': sub_headings_difference,
                'distinction_patterns'     : dictinction_patterns
                }
        nested_dict_tools.apply(res, lambda x: unicodedata.normalize("NFKD", x) if x is not None else "")

        return res

    def output_file_name(self, path, name, extension):
        ''' generate filename from path, name, extension '''
        return "".join([path, name, extension])

    def process_generator(self):
        # iterate randomly through the differencebetween backup and give some structured textversion of that pages
        relevant_files_paths = list(get_files_from_recursive_path(self.input_dir + self.input_html_file_filter))
        random.shuffle(relevant_files_paths)

        for path in relevant_files_paths:
            # ignore some files
            if any("%2F{prod}%2F".format(prod=s) in path for s in ['tag', 'emailpopup', 'author', 'feed']):
                continue
            try:
                # try to process the file
                html_dist_parsed = self.process(path)
            except UnicodeDecodeError:
                print ("%d: couldn't read that file %s" % (i, path))
                continue


            # with no results, no need to save something
            if not isinstance(html_dist_parsed, dict):
                print('nothing parsed for %s' % input_html_file_filter.replace('/', '_'))
                continue

            if html_dist_parsed['difference_text']:
                yield html_dist_parsed


    def process_all(self):
        # generate the output directories
        make_fresh_dir(self.process_dir)
        make_fresh_dir(self.output_dir)

        not_parsed = 0
        parsed = 0
        # iterate through all the content and files, that fit the desired location and kind of files
        for i, path in enumerate(list(get_files_from_recursive_path(self.input_dir + self.input_html_file_filter))):
            # ignore some files
            if any("%2F{prod}%2F".format(prod=s) in path for s in ['tag', 'emailpopup', 'author', 'feed']):
                continue
            try:
                # try to process the file
                html_dist_parsed = self.process(path)
            except UnicodeDecodeError:
                print ("%d: couldn't read that file %s" % (i, path))
                continue

            # with no results, no need to save something
            if not isinstance(html_dist_parsed, dict):
                print ('nothing parsed for %s' % input_html_file_filter.replace('/', '_'))
                not_parsed +=1
                continue

            # if there are results, save them
            if html_dist_parsed['distinction_patterns'] and html_dist_parsed['difference_text']:
                page_name = html_dist_parsed['title'].replace('/', ' or ')

                # once as dump to do annotation later
                with open (self.output_file_name(process_dir, page_name, '.dump'), 'wb') as path:
                    try:
                        pickle.dump(html_dist_parsed, path)
                    except RecursionError:
                        logging.error("Pickle recursion error?")
                        return None

                # once as a textfile to inspect
                with open(self.output_file_name(output_dir, page_name, ' distinction patterns.txt'), 'w') as out:
                    nice_string = pprint.pformat(html_dist_parsed['distinction_patterns'], indent=4, width=140)
                    out.write(nice_string)
                parsed +=1
            else:
                not_parsed += 1

            # how much was processed succesfully?
            print('file %s ' % path)
            parsing_percentage = parsed/(parsed+not_parsed)
            print ('parsed percentage: {:{width}.{prec}f}'.format(parsing_percentage, width=5, prec=2))


import unittest

class TestHtmlParser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHtmlParser, self).__init__(*args, **kwargs)
        self.html_parser = DifferenceBetweenHtmlParser()

    def run_htmlparser (self, path, gold_path):
        res = self.html_parser.process(path)
        pprint.pprint(res)
        with open(gold_path, 'r') as f:
            gold = eval(f.read())
        self.assertEqual(res, gold)
        self.assertTrue(res['distinction_patterns'])
        self.assertTrue(res['difference_text'])

    # Check different layouts of the pages for tables with 3 or 2 columns and if they come from
    # html-tables, picture-tables with 3 or 2 columns

    # VERSUS 3,2
    #    3: http%3A%2F%2Fwww.differencebetween.net%2Flanguage%2Fdifference-between-conference-and-seminar%2F.html
    #    2: http%3A%2F%2Fwww.differencebetween.net%2Flanguage%2Fdifference-between-desert-and-dessert-2%2F.html
    # VS 3,2
    #    3: http%3A%2F%2Fwww.differencebetween.net%2Fscience%2Fdifference-between-beaker-and-graduated-cylinder%2F.html
    #    2: http%3A%2F%2Fwww.differencebetween.net%2Fobject%2Fdifference-between-daylight-and-soft-white-led-bulbs%2F.html
    # tr-tl 3,2
    #    3: http%253A%252F%252Fwww.differencebetween.net%252Fscience%252Fhealth%252Fdifference-between-tumors-and-polyps%252F.html
    #    2: http%253A%252F%252Fwww.differencebetween.net%252Fscience%252Fhealth%252Fdifference-between-pork-and-bacon%252F%253Freplytocom%253D7343477.html

    def test_VERSUS_3(self):
        path      = "./tests/htmlparser/http%3A%2F%2Fwww.differencebetween.net%2Flanguage%2Fdifference-between-conference-and-seminar%2F.html"
        gold_path = path + '.gold'
        self.run_htmlparser(path, gold_path)
    def test_VERSUS_2(self):
        path      = "./tests/htmlparser/http%3A%2F%2Fwww.differencebetween.net%2Flanguage%2Fdifference-between-desert-and-dessert-2%2F.html"
        gold_path = path + '.gold'
        self.run_htmlparser(path, gold_path)

    def test_vs_3(self):
        path      = "./tests/htmlparser/http%3A%2F%2Fwww.differencebetween.net%2Fscience%2Fdifference-between-beaker-and-graduated-cylinder%2F.html"
        gold_path = path + '.gold'
        self.run_htmlparser(path, gold_path)
    def test_vs_2(self):
        path      = "./tests/htmlparser/http%3A%2F%2Fwww.differencebetween.net%2Fobject%2Fdifference-between-daylight-and-soft-white-led-bulbs%2F.html"
        gold_path = path + '.gold'
        self.run_htmlparser(path, gold_path)

    def test_tab_3(self):
        path      = "./tests/htmlparser/http%3A%2F%2Fwww.differencebetween.net%2Fscience%2Fhealth%2Fdifference-between-tumors-and-polyps%2F.html"
        gold_path = path + '.gold'
        self.run_htmlparser(path, gold_path)
    def test_tab_2(self):
        path      = "./tests/htmlparser/http%3A%2F%2Fwww.differencebetween.net%2Fscience%2Fhealth%2Fdifference-between-pork-and-bacon%2F.html"
        gold_path = path + '.gold'
        self.run_htmlparser(path, gold_path)

    def test_muhammad(self):
        path = "./tests/htmlparser/http%3A%2F%2Fwww.differencebetween.net%2Fmiscellaneous%2Fsports-miscellaneous%2Fdifference-between-ali-and-frazier%2F.html"
        gold_path = path + '.gold'
        self.run_htmlparser(path, gold_path)

if __name__ == '__main__':
    #unittest.main()

    html_parser = DifferenceBetweenHtmlParser()
    html_parser.process_all(
        input_dir=input_dir,
        output_dir=output_dir,
        process_dir=process_dir,
        input_html_file_filter=input_html_file_filter)




