import os

class Tagml_writer:
    def __init__(self):
        pass

    def create_tagml_tag (self, keys, mark, attributes=None, *args, **kwargs):
        ''' The TagML language described here. It's like HTML tags, but with overlapping tags, layers and the possibility
        to check single states with git-like commands.

        The last key is taken as the main key, the other keys are used to create the layering information.

        See for the language details: https://www.balisage.net/Proceedings/vol19/html/Dekker01/BalisageVol19-Dekker01.html#d310795e1633

        :param keys: list of strings
        :param mark: 'start' or 'end'
        :return: string with tagml-tag

        '''
        if mark=='start':
            start, end="[", ">"
            kwargs.update({'add_layer':'+'})
        elif mark=='end':
            start, end="<", "]"

        return "".join([
            start,
            str("".join([keys[-1], self.create_tagml_layers(keys[:-1], *args, **kwargs), self.create_attribute(attributes)])),
            end
        ])


    def wrap_with_tagml_tags(self, keys, content=None, joiner='\n', *args, **kwargs):
        ''' wraps some string withing a starting and ending tagml-tag

            :param keys: list of strings, building layers
            :param content: what (annotated) text to wrap
            :param joiner: use newline or what you want
            :return: wrapped text as string
        '''
        return joiner.join([
            self.create_tagml_tag(keys, mark='start', *args, **kwargs),
            content,
            self.create_tagml_tag(keys, mark='end'),
        ])


    def create_tagml_layers(self, keys, add_layer="", *args, **kwargs):
        ''' Layers are appended to the tags (start and and) with '|+?Layername'
            the optional '+' serves to register this layer, that must happen, if tags overlap and does nothing special, if
            they don't overlap.

        '''
        if not keys:
            return ""
        else:
            return '|' + add_layer + "".join(k.upper() for k in keys)


    def create_attribute(self, attributes):
        ''' attributes are a attribute name with '=' and a value, that is sometimes a enquoted value, but not
            for numers and floats and bools.

            attributes are not shown in export formats currently.

        '''
        if not attributes:
            return ""
        else:
            return " " + " ".join(["".join ([k,'=',self.value_to_tagml_str(v)]) for k,v in attributes.items()])


    def value_to_tagml_str(self, v):
        ''' convert this value to alexandria values for attributes, enquote some, some not '''
        if isinstance(v, float):
            return '{:{width}.{prec}f}'.format(v, width=5, prec=2)
        if isinstance(v, int):
            return "%d" % v
        if isinstance(v, str):
            return "'%s'" % v

tagml_writer = Tagml_writer()

class alexandria_api:
    ''' Simple wrapper for alexandria, the TextAsGraphMarkupLanguage -- Git.

        It's nothing more, than executing the commands with os.system() and keeping some history about the commands
        for debugging.

        The workflow is:
        ================

        * adding a tagml-file

        * commiting this file

        * commiting views on this file (for displaying certain layer, you define by a view)

        * checking these views out or not with 'checkout'

        * exporting them to svg, dot, xml, png


        See for the language details: https://www.balisage.net/Proceedings/vol19/html/Dekker01/BalisageVol19-Dekker01.html#d310795e1633

    '''
    def __init__(self, alexandria_path='./alexandria-app/bin'):
        ''' Initialize alexandria folder, that means creating the 'tagml' folder and some hidden alexandria folder,
            that is like .git

        :param alexandria_path: where to find alexandria

        '''
        os.environ["PATH"] += ":" + alexandria_path
        self.history = []
        os.system("alexandria init")

    def get_history(self):
        ''' get the commands, that the API called '''
        return self.history

    def ossystem(self, command):
        ''' run the command and add the command to the history '''
        self.history.append(command)
        return os.system(command)

    def checkout_name_from_path(self, path):
        ''' after commiting the file, it's registered and can not be checked out by its filename, but by this
            registering name, that is the base filename, you can get it by this function here

        :param path: what file


        '''
        return os.path.splitext(os.path.basename(path))[0]

    def add(self, path):
        ''' you can add full TagML files, as well as views with add.

        :param path: what file

        '''
        self.ossystem('alexandria add "%s"' % path)

    def commit(self, path=None, args='-a'):
        ''' commit a file or all added files. '''
        if path:
            self.ossystem('alexandria commit "%s"' % path)
        elif args:
            self.ossystem("alexandria commit %s" % args)

    def about(self):
        ''' What's about now, which file is checked out '''
        return self.ossystem("alexandria about")

    def status(self):
        ''' Which states are registered to check them out '''
        return self.ossystem("alexandria status")

    def checkout(self, what):
        ''' what branch to checkout, if what=='-', it goes to the main branch

            :param what: string with path or '-'
            :return: succesfulness output

        '''
        return self.ossystem('alexandria checkout "%s"' % what)

    def diff(self, what):
        ''' how the actual branch differs to another

            :param what: main state to different state compared,
            :return: get a nice diff

        '''
        return self.ossystem('alexandria diff "%s"' % what)

    def export(self, format, what, where):
        ''' export actual state to formatted file '''
        self.ossystem('alexandria export-{format} -o "{where}" "{what}"'.format(format=format, where=where, what=what))

    def help(self):
        ''' Get alexandrias help '''
        return self.ossystem('alexandria -h')

    def revert(self, what):
        ''' Revert the changes made by the tagml-file

            :param what: checkout state to revert
            :return:
        '''
        self.ossystem("alexandria revert '%s'" % what)







