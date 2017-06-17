__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import argparse
import pyttsx

from random import sample


WORDS_PER_TEST = 10
TICK = u'\u2714'
CROSS = u'\u2715'
REPETITIONS = 2

# TODO: record and feedback misspellings


def setup_engine():
    engine = pyttsx.init(debug=True)
    voices = [
        voice
        for voice in engine.getProperty('voices')
        if voice.name.startswith('english_rp')
    ]
    english_voice = voices[0]
    engine.setProperty('voice', english_voice.id)
    engine.setProperty('rate', 120)
    return engine


def say_phrase(engine, phrase, word):
    engine.say(phrase, word)
    engine.runAndWait()


def read_words(words_file):
    for line in words_file:
        yield line.strip().lower()


def do_test(engine, words_in_test, test_words):
    misspellings = []

    def onWordSaid(name, completed):
        word = name
        spelling = raw_input("> ").strip().lower()
        if spelling != word:
            print(u"{} {}".format(CROSS, word))
            misspellings.append(word)
        else:
            print(TICK)

    engine.connect('finished-utterance', onWordSaid)

    print("Starting test")
    for word in test_words:
        phrase = ', '.join([word] * REPETITIONS)
        say_phrase(engine, phrase, word)

    print("\nYour score is {}/{}".format(
        words_in_test - len(misspellings),
        words_in_test,
        '\n'.join(misspellings)
    ))
    if misspellings:
        print("""
The spellings you need to work on are:
{}
""".format('\n'.join(misspellings)))
    else:
        print("100% correct")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Spelling tests'
    )
    parser.add_argument('words_file', type=argparse.FileType('r'))
    parser.add_argument('--words_per_test', type=int, default=WORDS_PER_TEST)
    args = parser.parse_args()

    engine = setup_engine()
    test_words = sample(list(read_words(args.words_file)), args.words_per_test)

    do_test(engine, args.words_per_test, test_words)
