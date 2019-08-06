from grammer_text_fit.alexandria_wrapper import tagml_writer
import regex as re

def tok_list_to_string(tokens, delim=''):
   return delim.join(t['text'] for t in tokens)

class Tok (dict):
    ''' Structured Data token as Dictionary

    Tok is a class with appendable attributes for tokens by inheriting dict

    '''
    def __init__ (self, *args, writer=tagml_writer, **kwargs):
        super(Tok, self).__init__(*args, **kwargs)
        self['annotations'] = []
        self['start_end'] = []
        self['conf'] = []
        self.writer = writer

    def __str__(self):
        if 'text' in self:
            return "text={text} (i={i})".format(
                i=str(self['i']),
                text=self['text'])
        else:
            return super.__str__(self)

    def __repr__(self):
        if 'text' in self:
            return "'{text}'".format(
                i=str(self['i']),
                text=self['text'])
        else:
            return super.__str__(self)



    def __hash__(self):
        if 's_id' in self and 'i' in self:
            return hash(self['text']+str(self['i']))
        else:
            return hash(str(self))

    def set_property(self, prop, val):
        self.__setattr__(prop, val)
        return self

    def get_annotation_props (self):
        if 'annotations' in self:
            return self['annotations'], self['start_end'], self['conf']
        else:
            return [], [], []

    def update_token(self, start_end, keys, conf=0):
        """ Updates one tokens tag information

        :param keys: liOst of kind and attributes
        :param start_end:  bool 1 for start, 0 end
        :return: None
        """
        before_an1, before_start_end, before_conf = self.get_annotation_props()
        self.update(
            {'annotations': [keys, *before_an1],
             'start_end': [start_end, *before_start_end],
             'conf': [conf, *before_conf]
             })

    int_regex = re.compile(r'\d+')

    def int_in_string(self, i, string):
        match_or_not = self.int_regex.search(string)
        if match_or_not and int(match_or_not.group()) == i:
            return True
        else:
            return False


    def conll03_layer_repr(self, layer=None):
        if not hasattr(Tok.conll03_layer_repr, 'dependenceA'):
            Tok.conll03_layer_repr.dependenceA = False
            Tok.conll03_layer_repr.dependenceB = False

        text = self['text']
        tag = self['spacy'].tag_

        if 'annotations' in self and self['annotations'] and (not layer or any(a for a in self['annotations'] if self.int_in_string(layer, a[0]))):
            annotations = [keys for keys in self['annotations'] if (not layer or self.int_in_string(layer, keys[0]))]
            best_annotation = sorted(annotations, key=lambda x: self.importance_dict[x[-1]])
            annotation_tag = [a for a in best_annotation if a][0][-1]
            annotation_suffix = annotation_tag[-2:]
            annotation_tag = annotation_tag[:-2]
            tag_inside_beginning_tag = ""
            if  annotation_suffix == '_A':
                if not Tok.conll03_layer_repr.dependenceA:
                    dependence_tag = 'B'
                    tag_inside_beginning_tag = "-".join([dependence_tag, tag])
                    annotation_tag = "-".join([dependence_tag,annotation_tag])
                    Tok.conll03_layer_repr.dependenceA = True
                else:
                    dependence_tag = 'I'
                    tag_inside_beginning_tag = "-".join([dependence_tag, tag])
                    annotation_tag = "-".join([dependence_tag, annotation_tag])
            if annotation_suffix == '_B':
                if not Tok.conll03_layer_repr.dependenceB:
                    dependence_tag = 'B'
                    tag_inside_beginning_tag = "-".join([dependence_tag, tag])
                    annotation_tag = "-".join([dependence_tag, annotation_tag])

                    Tok.conll03_layer_repr.dependenceB = True
                else:
                    dependence_tag = 'I'
                    tag_inside_beginning_tag = "-".join([dependence_tag, tag])
                    annotation_tag = "-".join([dependence_tag, annotation_tag])
        else:
            tag_inside_beginning_tag = 'O'
            annotation_tag = 'O'
        return "\t".join([text, tag, tag_inside_beginning_tag.upper(), annotation_tag.upper()])


    importance_dict = {
        'subject':1,
        'contrast':2,
        'aspect':3,
        'subject_A': 1,
        'contrast_A': 3,
        'aspect_A': 4,
        'subject_B': 1,
        'contrast_B': 3,
        'aspect_B': 4,
        'marker':0
    }
    def conll03_general_repr(self):
        if not hasattr(Tok.conll03_repr, 'dependence'):
            Tok.conll03_repr.dependence = False
        text = self['text']
        tag = self['spacy'].tag_
        if 'annotations' in self and self['annotations'] and any(a for a in self['annotations']):
            i
            annotations = sorted(self['annotations'], key=lambda x: self.importance_dict[x[-1]])
            annotation_tag = [a for a in annotations if a][0][-1]
            if not Tok.conll03_repr.dependence:
                dependence_tag = 'B'
                tag_inside_beginning_tag = "-".join([dependence_tag, tag])
                annotation_tag = "-".join([dependence_tag,annotation_tag])

                Tok.conll03_repr.dependence = True
            else:
                dependence_tag = 'I'
                tag_inside_beginning_tag = "-".join([dependence_tag, tag])
                annotation_tag = "-".join([dependence_tag, annotation_tag])
        else:
            Tok.conll03_repr.dependence = False
            tag_inside_beginning_tag = 'O'
            annotation_tag = 'O'
        return "\t".join([text, tag, tag_inside_beginning_tag.upper(), annotation_tag.upper()])


    def tagml_repr(self):
        res = self['text']
        for annotation, start_end, conf in zip(self['annotations'], self['start_end'], self['conf']):
            if annotation:
                if start_end:
                    if 'conf' in self:
                        attributes = {'conf': conf}
                    else:
                        attributes = None
                    res = "".join ( [
                        self.writer.create_tagml_tag(keys=annotation, mark='start', attributes=attributes),
                        res
                        ] )
                else:
                    res = "".join([
                        res,
                        self.writer.create_tagml_tag(keys=annotation, mark='end'),
                        ] )
        return res
