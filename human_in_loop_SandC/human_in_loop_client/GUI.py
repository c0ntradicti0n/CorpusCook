from helpers.color_logger import *
from collections import Counter
from time import sleep
from collections import OrderedDict as OD
from nltk import flatten

import kivy
kivy.require('1.9.0')
from kivy.config import Config
Config.set('graphics', 'width', '2000')
Config.set('graphics', 'height', '1500')
Config.write()
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView

from human_in_loop_server.sampler import Sampler
from human_in_loop.corpus import Corpus, nlp
from human_in_loop_server.textstore import TextStore
from human_in_loop.upmarker import UpMarker
from human_in_loop.client import AnnotationClient
from human_in_loop.annotation_protocol import *


samples_path = None
corpus_path = None

class Annotation_Screen(Screen):
    pass

class Manipulation_Screen(Screen):
    pass
class Sample_Screen(Screen):
    pass


class RecycleViewRow(BoxLayout):
    id = StringProperty()
    kind = StringProperty()
    start = NumericProperty()
    end = NumericProperty()
    length = NumericProperty()
    able = BooleanProperty()

class AnnotationManipulationRow(BoxLayout):
    kind = StringProperty()

    def more_annotation_of(self, kind):
        self.get_root_window().children[0].more_annotation_of(kind)

    def less_annotation_of(self, kind):
        self.get_root_window().children[0].less_annotation_of(kind)


class SliderView(RecycleView):
    pass

class AnnotationManipulationView(RecycleView):
    pass


class SpanSlider(Slider):
    def on_touch_up(self, touch):
        root = self.get_root_window().children[0]
        boxes = list(self.parent.parent.children)
        new_data = [SpanSlider.collect_data_from_box(b) for b in boxes]
        root.update_from_data(new_data)

    def collect_data_from_box(b):
        return OD({
            'able': b.ids.active_or_not.active,
            'kind': b.kind,
            'start': int(b.ids.start.value),
            'end': int(b.ids.end.value),
            'length': int(b.ids.end.max),
            'id': 'hach'
        })

class RootWidget(ScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global samples_path
        global corpus_path
        self.me_as_client = AnnotationClient()
        self.sampler = Sampler(samples_path) # expands the sample stack
        self.difference_pages = self.sampler.next_page()
        self.upmarker = UpMarker()
        self.corpus = Corpus(corpus_path)
        self.textstore = None

        self.sampler_proceed()

    def sampler_add(self):
        text = self.ids.sampl.ids.html_sample.selection_text.replace('\n', ' ').replace('  ', ' ')
        if not text:
            logging.error('Text must be selected')
            return None
        logging.info("Adding sample to library")
        self.me_as_client.commander(Command=SaveSample, text=text)
        self.sampler.add_to_library(text)
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
        self.me_as_client.commander(Command=SaveAnnotation, annotation=self.final_version)
        ok = self.corpus.write_annotation(self.final_version)
        if ok == None:
            logging.error ('There was a problem with the annotation. Tagged was:\n\n %s' % (self.final_version))
            self.current = "Manipulation_Screen"
        logging.info("Adding to corpus")
        self.take_next()
        self.current = "Annotation_Screen"

    def complicated_sample(self):
        self.complicated(" ".join([word for word, _ in self.final_version]))
        self.take_next()
        self.current = "Annotation_Screen"

    def complicated_selection(self):
        self.complicated(self.ids.sampl.ids.html_sample.selection_text)
        self.current = "Sample_Screen"

    def complicated(self, text):
        self.me_as_client.commander(Command=SaveComplicated, text=text)
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
        self.ids.manip.ids.annotationmanipulationview.refresh_from_data()
        logging.warning(self.ids.manip.ids.annotationmanipulationview.data)


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
        logging.info(data)
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

    def more_annotation_of(self, kind):
        length = len(self.final_version)
        self.ids.manip.ids.spansliderview.data.append(
            OD({
                'kind': kind,
                'id': kind,
                'start': length - 2,
                'end': length - 1,
                'able': True,
                'length': length,
            }))

    def less_annotation_of(self, kind):
        try:
            for annotation in self.ids.manip.ids.spansliderview.data[::-1]:
                if annotation['kind'] == kind:
                    data_was = self.ids.manip.ids.spansliderview.data
                    data_was.remove(annotation)
                    self.ids.manip.ids.spansliderview.data = data_was
                    self.ids.manip.ids.spansliderview.refresh_from_data()
                    break
        except ValueError:
            logging.warning('no %s annotation was in used annotations' % kind)

    def check_annotation(self, annotation):
        span_delims = [t[1][0] for t in annotation]
        logging.info(span_delims)
        count = Counter(span_delims)
        if not count['B'] == 2:
            logging.error('Annotation contains not at least the minimum number of annotations!!! %s' % str(count))

    def take_next(self):
        if self.textstore == None:
            self.textstore = TextStore(samples_path)
        self.me_as_client.commander(ProceedLocation=self.got_sample, Command=DeliverSample)

    def got_sample(self, text=''):
        self.sentence = text
        print(text)
        if self.sentence == None:
            logging.info('Thank you for working!')
            App.get_running_app().stop()
            return None

        self.me_as_client.commander(ProceedLocation=self.take_next_rest, Command=MakePrediction, text=text)

    def take_next_rest(self, annotation=''):
        print (annotation)
        self.annotated_sample = annotation
        self.doc = nlp(self.sentence)
        self.final_version = self.annotated_sample

        print (annotation)
        print (annotation)
        print (annotation)
        print (annotation)
        print (annotation)

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