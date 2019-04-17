'''
A script to identify the encoding used inp a file, if unspecified.
'''

from encodings.aliases import aliases
from collections import defaultdict
import logging
import argparse

def main():
    '''
    parses available encoding types and checks
    if expected terms are present as such
    when decoded
    '''
    logging.basicConfig(level=logging.INFO, format='[%(levelname)8s]: %(message)s')
    infile = ARGS.infile
    expected_words = ARGS.exp
    available_encs = list(set(aliases.values()))
    for enc in available_encs:
        try:
            with open(infile, 'r', encoding=enc) as inp:
                try:
                    contents = inp.read()
                    found, missed = defaultdict(list), defaultdict(list)
                    for word in expected_words:
                        if word in contents:
                            found[enc].append(word)
                        else:
                            missed[enc].append(word)

                    if expected_words:
                        if missed[enc]:
                            logging.debug('%s: Missed %s', enc, missed[enc])
                        if found[enc]:
                            logging.info('%s: Found %s', enc, found[enc])
                    else:
                        logging.info('%s: readable. Use expected terms (--exp) to narrow results.',
                                     enc)


                except (UnicodeError, UnicodeDecodeError) as exception:
                    logging.debug('%s: %s', enc, type(exception).__name__)

        except LookupError as exception:
            logging.debug('%s: %s', enc, type(exception).__name__)



    return

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-i', '--infile', help='input file', required=True)
    PARSER.add_argument('--exp', help='expected terms (separate terms by a space)',
                        default=[], nargs='*', action='store')
    ARGS = PARSER.parse_args()
    main()
