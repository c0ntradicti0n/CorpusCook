import itertools
from collections import Counter
from time import sleep

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import kivy
from kivy.uix.slider import Slider
from nltk import flatten

from human_in_loop.sampler import Sampler

kivy.require('1.9.0')
from kivy.config import Config
Config.set('graphics', 'width', '2000')
Config.set('graphics', 'height', '1000')

from human_in_loop.corpus import Corpus, nlp
from human_in_loop.textstore import TextStore
from human_in_loop.upmarker import UpMarker
from human_in_loop.client import Client

samples_path = None
corpus_path = None

class Annotation_Screen(Screen):
    pass

class Manipulation_Screen(Screen):
    pass

class Sample_Screen(Screen):
    pass

class SpanSlider(Slider):

    def on_touch_move(self, touch):
        self.parent.parent.manager.update_manip_display()

    def on_touch_up(self, touch):
        self.parent.parent.manager.update_manip_display()
        self.parent.parent.manager.final_version = self.parent.parent.manager.new_annotation

class RootWidget(ScreenManager):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global samples_path
        global corpus_path

        self.client = Client(app=self)

        self.sliders = \
            {'SUBJECT': [(self.ids.manip.ids.sliderS1A, self.ids.manip.ids.sliderS2A),
                         (self.ids.manip.ids.sliderS1B, self.ids.manip.ids.sliderS2B)],
             'CONTRAST': [(self.ids.manip.ids.sliderC1A, self.ids.manip.ids.sliderC2A),
                         (self.ids.manip.ids.sliderC1B, self.ids.manip.ids.sliderC2B)]
            }
        self.part_sliders = \
            {'A': [('SUBJECT', self.ids.manip.ids.sliderS1A, self.ids.manip.ids.sliderS2A),
                   ('CONTRAST', self.ids.manip.ids.sliderC1A, self.ids.manip.ids.sliderC2A)
                   ],
             'B': [('SUBJECT', self.ids.manip.ids.sliderS1B, self.ids.manip.ids.sliderS2B),
                   ('CONTRAST', self.ids.manip.ids.sliderC1B, self.ids.manip.ids.sliderC2B)]
             }

        self.sampler = Sampler(samples_path) # expands the sample stack
        self.difference_pages = self.sampler.next_page()
        self.upmarker = UpMarker()
        self.corpus = Corpus(corpus_path)

        self.textstore = None # diminishes the sample stack

        self.sampler_proceed()

    def sampler_add(self):
        text = self.ids.sampl.ids.html_sample.selection_text.replace('\n', ' ').replace('  ', ' ')
        if not text:
            print ('Text must be selected... ')
            return None

        self.client.commander('save_sample', text=text)
        self.sampler.add_to_library(text)
        print("Adding to sample corpus")
        self.current = "Sample_Screen"

    def sampler_proceed(self):
        try:
            self.ids.sampl.ids.html_sample.text = next(self.difference_pages)['difference_text'].replace('\n', ' ').replace('  ', ' ')
        except StopIteration:
            raise FileNotFoundError("text files to choose samples from have not been detected. Changing root directory may help.")
        self.current = "Sample_Screen"

    def go_annotating(self):
        self.take_next()
        sleep(0.2)
        self.current = "Annotation_Screen"

    def ok(self):
        self.client.commander('save_annotation',annotation=self.final_version)
        ok = self.corpus.write_sample(self.final_version)
        if ok==None:
            print ('There was a problem with the annotation. Tagged was:\n\n %s' % (self.final_version))
            self.current = "Manipulation_Screen"
        print("Adding to corpus")
        self.take_next()
        sleep(0.2)
        self.current = "Annotation_Screen"

    def complicated_sample(self):
        self.complicated(" ".join([word for word, _ in self.final_version]))
        self.take_next()
        self.current = "Annotation_Screen"

    def complicated_selection(self):
        self.complicated(self.ids.sampl.ids.html_sample.selection_text)
        self.current = "Sample_Screen"

    def complicated(self, text):
        self.client.commander('save_a_complicated_sample', text=text)
        with open("./complicated.txt", 'a+') as f:
            f.writelines([text])

    def shit(self):
        self.take_next()
        self.current = "Annotation_Screen"

    def manipulate(self):
        self.update_sliders()
        self.update_manip_display()
        self.current = "Manipulation_Screen"

    def update_manip_display(self):
        self.spans = [
            (group, [(kind, int(start_sl.value), int(end_sl.value)) for kind, start_sl, end_sl in sliders])
           for group, sliders in self.part_sliders.items()
        ]
        new_annotation = [(token.text,'O') for token in self.doc]

        self.adjust_slider_len(new_annotation)

        for g, spans in self.spans:

            # get the minimum position of the span to make the beginning span tag in the BIO-annotation scheme
            all_starts_of_span = [start for kind, start, end in spans]
            beginning = min(all_starts_of_span)
            print (beginning, spans)

            for kind, start, end in spans[::-1]:
                print (kind, start == beginning)
                # read slist of spans backwards to overwrie the contrast with the subject tags
                for i in range(start, end):
                    if i < len(new_annotation):
                        new_annotation[i] = (new_annotation[i][0], "-".join(['B' if i == beginning else 'I', kind]))
                    else:
                        print ('out of range span annotation> %d >= %d' % (i, len(new_annotation)))

        span_delims = [t[1][0] for t in new_annotation]
        print (span_delims)
        count = Counter(span_delims)
        if not count['B'] == 2:
            print('Annotation contains wrong number of spanning tags!!! %s' % str(count))

        self.new_annotation = new_annotation
        self.ids.manip.ids.spans.text = str(self.spans)
        self.ids.manip.ids.sample.text = self.upmarker.markup(new_annotation)

    def adjust_slider_len(self, new_annotation):
        l = len(new_annotation)
        for sl in flatten(flatten(list(self.sliders.values()))):
            sl.range = (0, l)

    def display_sample(self):
        markedup_sentence = self.upmarker.markup(self.annotated_sample)
        self.ids.annot.ids.sample.text = markedup_sentence
        self.ids.manip.ids.sample.text = markedup_sentence

    def update_sliders(self):

        spans = list(Corpus.compute_spans(self.final_version))
        print ([sp[1] for sp in spans])
        spans = sorted(spans, key= lambda x: x[0])
        span2slider = (
            itertools.zip_longest(self.sliders[g], l)
            for g, l in
            itertools.groupby(spans, key=lambda x: x[0])
        )

        self.adjust_slider_len(self.doc)

        l = len(self.doc)
        for annotation_group in span2slider:
            for start_end_slider, span in annotation_group:

                # if there are more annotations than sliders, the default is non, that is no tuples and so it would
                # interrupt here
                if not start_end_slider:
                    continue
                (slider_start, slider_end) = start_end_slider

                if span:
                    (g, (start, end), annotation) = span
                    slider_start.value = start
                    slider_end.value = end
                else:
                    slider_start.value = l-3
                    slider_end.value = l-1

    def take_next(self):
        if self.textstore == None:
            "First we have to load the model... that may take long time"
            self.textstore = TextStore(samples_path)

        while True:
            self.sentence = self.textstore.next_one()
            if self.sentence == None:
                print('Thank you for working!')
                App.get_running_app().stop()
                return None
            self.client.commander ('make_prediction', text=self.sentence)
            break

    def take_next_rest(self, annotation):
        self.annotated_sample = annotation
        self.doc = nlp(self.sentence)
        self.final_version = self.annotated_sample
        self.update_sliders()
        self.display_sample()


Builder.load_file("HumanInLoop.kv")

class MainApp(App):
    def build(self):
        return RootWidget()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    MainApp().run()