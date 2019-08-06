import argparse

from human_in_loop.GUI import MainApp
from human_in_loop import GUI

parser = argparse.ArgumentParser(description='let the human work in the loop, checking model annotations')
parser.add_argument('samples_path', type=str,
                   help='what to make predictions on')
parser.add_argument('corpus_path', type=str,
                   help='where to write the humans good decisions and manipulations')
args = parser.parse_args()

GUI.samples_path = args.samples_path
GUI.corpus_path = args.corpus_path


def main():
    ui = MainApp().run()

if __name__ == "__main__":
    main()

