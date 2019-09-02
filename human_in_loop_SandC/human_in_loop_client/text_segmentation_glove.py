import spacy
import nltk
import os
from gensim.models import KeyedVectors
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import math
from scipy import spatial
import matplotlib.pyplot as plt
#import mpld3

import text_segmentation as ts

# the directory containing the Stanford GloVe model
# Change this to the proper path in your environment
glove_file = '/home/stefan/PycharmProjects/CorpusCook/glove.6B/glove.6B.100d.txt'

# the document to be segmented
file_name="/home/stefan/PycharmProjects/CorpusCook/diff0.ref"

# Instantiating the text segmetnation class object
seg_obj = ts.text_segmentation_class(file_name, glove_file)

#seg_boj.doc contains the text of the document to be segmented
print(seg_obj.doc)
seg_obj.greedy_text_segmentation(5)
print(seg_obj.get_segment_texts())