import itertools
import pprint
from helpers.color_logger import *
from collections import Counter
from time import sleep
from typing import Dict, Any, Tuple, List
from collections import OrderedDict as OD


def get_dict_diffs(a: Dict[str, Any], b: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    added_to_b_dict: Dict[str, Any] = {k: b[k] for k in set(b) - set(a)}
    removed_from_a_dict: Dict[str, Any] = {k: a[k] for k in set(a) - set(b)}
    common_dict_a: Dict[str, Any] = {k: a[k] for k in set(a) & set(b)}
    common_dict_b: Dict[str, Any] = {k: b[k] for k in set(a) & set(b)}
    return added_to_b_dict, removed_from_a_dict, common_dict_a, common_dict_b

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

from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty, NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup

class MessageBox(Popup):
    message = StringProperty()

class RecycleViewRow(BoxLayout):
    id = StringProperty()
    kind = StringProperty()
    start = NumericProperty()
    end = NumericProperty()
    length = NumericProperty()
    able = BooleanProperty()


class SliderView(RecycleView):
    def __init__(self, **kwargs):
        super(SliderView, self).__init__(**kwargs)

    def message_box(self, message):
        p = MessageBox()
        p.message = message
        p.open()
        print('test press: ', message)

class Sample_Screen(Screen):
    pass

def collect_data_from_box(b):
    return OD({
        'able': b.ids.active_or_not.active,
        'kind':b.kind,
        'start':int(b.ids.start.value),
        'end': int(b.ids.end.value),
        'length': int(b.ids.end.max),
        'id':'asdfgh'
    })

class SpanSlider(Slider):
    def on_touch_move(self, touch):
        self.parent.parent.parent.parent.parent.parent.update_manip_display()

    def on_touch_up(self, touch):
        root = self.get_root_window().children[0]
        boxes = list(self.parent.parent.children)
        new_data = [collect_data_from_box(b) for b in boxes]
        root.update_from_data(new_data)

class RootWidget(ScreenManager):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global samples_path
        global corpus_path
        self.last_data = [{}]

        self.client = Client(app=self)
        self.sampler = Sampler(samples_path) # expands the sample stack
        self.difference_pages = self.sampler.next_page()
        self.upmarker = UpMarker()
        self.corpus = Corpus(corpus_path)
        self.textstore = None

        self.sampler_proceed()

    def sampler_add(self):
        text = self.ids.sampl.ids.html_sample.selection_text.replace('\n', ' ').replace('  ', ' ')
        if not text:
            print ('Text must be selected... ')
            return None

        self.client.commander('save_sample', text=text)
        self.sampler.add_to_library(text)
        logging.info("adding sample to library")
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
        logging.info("Adding to corpus")
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
        self.display_sample()

    def adjust_slider_len(self, new_annotation):
        l = len(new_annotation)
        for sl in flatten(flatten(list(self.sliders.values()))):
            sl.range = (0, l)

    def display_sample(self):
        markedup_sentence = self.upmarker.markup(self.annotated_sample)
        self.ids.annot.ids.sample.text = markedup_sentence
        self.ids.manip.ids.sample.text = markedup_sentence

    def update_sliders_from_spans(self):
        paired_spans = list(Corpus.compute_structured_spans(self.final_version))
        length =  len(self.final_version)

        self.sliders = {}
        self.part_sliders = {}
        self.ids.manip.ids.spansliderview.data = []

        for g, spans in enumerate(paired_spans):
            self.ids.manip.ids.spansliderview.data.append(
                [
                    OD({
                        'kind': kind,
                        'id': str(g)+str(i),
                        'start':start,
                        'end': end,
                        'able':True,
                        'length':length,
                    })
                    for i, (kind, (start, end), annotation) in enumerate(spans)
                ])
        self.ids.manip.ids.spansliderview.data = flatten(self.ids.manip.ids.spansliderview.data)
        self.ids.manip.ids.spansliderview.refresh_from_data()

    def update_sliders(self):
        recent_data = list(self.ids.manip.ids.spansliderview.data_model.data)
        self.update_from_data(recent_data)

    def sort_data(self, data):
        return sorted(data, key=lambda x: x['start'])

    def update_from_data(self, data):
        print(data)
        data = self.sort_data(data)
        self.ids.manip.ids.spansliderview.data = data
        self.ids.manip.ids.spansliderview.refresh_from_data()
        tokens = [t[0] for t in self.final_version]
        paired_spans = self.corpus.pair_spans(data)
        new_annotation = self.corpus.annotation_from_spans(tokens=tokens, paired_spans=paired_spans)
        self.final_version = new_annotation
        self.annotated_sample = new_annotation
        self.check_annotation(new_annotation)
        self.display_sample()

    def check_annotation(self, annotation):
        span_delims = [t[1][0] for t in annotation]
        print(span_delims)
        count = Counter(span_delims)
        if not count['B'] == 2:
            print('Annotation contains wrong number of spanning tags!!! %s' % str(count))

    def take_next(self):
        if self.textstore == None:
            self.textstore = TextStore(samples_path)
        self.client.commander('deliver_sample')

    def got_sample(self, text=''):
        self.sentence = text
        if self.sentence == None:
            print('Thank you for working!')
            App.get_running_app().stop()
            return None
        self.client.commander ('make_prediction', text=self.sentence)

    def take_next_rest(self, annotation):
        self.annotated_sample = annotation
        self.doc = nlp(self.sentence)
        self.final_version = self.annotated_sample
        self.update_sliders_from_spans()
        self.display_sample()

Builder.load_file("HumanInLoop.kv")

class MainApp(App):
    def build(self):
        return RootWidget()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    MainApp().run()