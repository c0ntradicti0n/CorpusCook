class UpMarker:
    def __init__(self):
        pass

    annotation_dict = {
        'SUBJECT': ('b','58C550'),
        'CONTRAST': ('i', 'BD7A48'),
        'ASPECT': ('sub', '589ACC'),
        'MARKER': ('ref', 'A845B0')
    }

    def markup_word(self, word, anno_tag):
        for kind, (mark_tag, color) in self.annotation_dict.items():
            if kind in anno_tag:
                return "[{tag}][color=#{color}]{word}[/color][/{tag}]".format(tag=mark_tag, word=word, color=color)
        else:
           return word

    def markup(self, annotation):
        return " ".join([self.markup_word(*anno) for anno in annotation])

