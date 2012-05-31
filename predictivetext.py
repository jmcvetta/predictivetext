# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.
#
# The logic in this program was derived from the code posted at
# https://gist.github.com/1686815.


import re
import sys
import optparse


class PredictiveText:
    '''
    A predictive text input system as used by cellphones using a numeric keypad
    '''
    
    def __init__(self):
        keys = ('abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz') # Letters on phone keypad
        self.charnum = dict((l, str(n)) for n, letters in enumerate(keys, start=2) for l in letters)
        self.data = {}
        self.ocurrences = {}
        self.wmatch = re.compile('[^a-z]+')

    def learn(self, word):
        '''
        @param word: A word to be analyzed and added to text prediction data
        @type word:  String
        @rtype: None
        '''
        # Make a numeric representation of word
        num = ''.join(self.charnum[c] for c in word) 
        for i in xrange(1, len(word) + 1):
            inp = num[:i]
            if inp not in self.data:
                self.data[inp] = set([word])
            else:
                self.data[inp].add(word)
    
    def train(self, filepath):
        '''
        Add all the words in a file to text prediction data
        @param filepath: Path to the file
        @type filepath:  String
        @rtype: None
        '''
        with open(filepath, 'r') as f:
            for word in self.wmatch.split(f.read().lower()):
                if word in self.ocurrences:
                    self.ocurrences[word] += 1
                else:
                    self.learn(word)
                    self.ocurrences[word] = 1

    def search(self, numstring):
        '''
        Searches for possible words represented by a numeric string
        @param num: Telephone keypad representation of a word
        @type num:  String where all characters are integers
        '''
        if not numstring in self.data:
            return None
        results = ([], [])
        for match in self.data[numstring]:
            results[int(len(match) != len(numstring))].append((match, self.ocurrences[match]))
        k = lambda m: m[1]
        return (sorted(results[0], key=k, reverse=True),
                sorted(results[1], key=k, reverse=True))
    
if __name__ == '__main__':
    usage = "usage: %prog [options] training_file numeric_string"
    parser = optparse.OptionParser(usage=usage)
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.print_usage()
        sys.exit(2)
    filepath, numstring = args
    pt = PredictiveText()
    pt.train(filepath)
    results = pt.search(numstring)
    if not results:
        print "No match found"
        sys.exit(1)
    for i, t in ((0, 'Exact'), (1, 'Prefix')):
        print "%s matches for %s:" % (t, sys.argv[1])
        for match, oc in results[i]:
            print match