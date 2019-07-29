class TextStore:
    def __init__(self, path):
        self.path = path
        self.sentences = self.read_samples_from_list()

    def next_one (self):
        try:
            return next(self.sentences)
        except StopIteration:
            return None

    def rest_ones(self):
        yield from self.next_one()

    def write_rest_samples (self):
        with open(self.path, "w+") as f:
            f.writelines(self.rest_ones())

    def read_samples_from_list(self):
        with open(self.path, "r") as f:
            for line in f.readlines():
                yield line.strip()