#! /usr/bin/env python3
"""A Pronunciation Trainer to help language learners improve"""


from .components.main_window import MainWindow
from .trainer import Trainer

LESSON_PATH = "lessons"


class App:
    """Speech Recognition app from improving pronunciation"""

    def __init__(self, lang="en-US", phrasepack="greetings.txt"):
        self.trainer = Trainer()
        self.window = MainWindow(
            self,
            trainer=self.trainer,
        )

        self.window.load_phraselist(phrasepack)
        self.window.change_sr("sphinx")
        self.window.change_language(lang)

    def ulog(self, message):
        """Log a message to the info box"""
        self.window.ulog(message)

    def main(self):
        """Start the mainloop"""
        self.window.mainloop()


def main():
    """Run the pronunciation trainer app"""
    app = App(lang="en-US")
    app.main()


if __name__ == "__main__":
    main()
