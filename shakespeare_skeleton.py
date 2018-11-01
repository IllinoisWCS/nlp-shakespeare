import re, random
from collections import defaultdict

# Constants
START_TAG = "<LINE>"
END_TAG = "</LINE>"

'''
Preprocess corpus
'''
def preprocess(corpus):

    with open("shakespeare/j_caesar.xml") as f:
        script = f.read()

    script = script.split("\n")
    script = [(line[:6] + " " + line[6:-7] + " " + line[-7:]) for line in script if len(line) > len(START_TAG) and line[:6] == START_TAG]

    # Pad punctuation with spaces
    script = [re.sub('([.,:;!?()])', r' \1 ', line) for line in script]
    script = [re.sub('\s{2,}', ' ', line) for line in script]

    return script

'''
Unigram language model
'''
class UnigramModel():
    def __init__(self, corpus):
        self.counts = defaultdict(float)
        self.total = 0.0
        self.train(corpus)

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        pass

    # Returns the probability of word in the distribution
    def prob(self, word):
        pass

    # Generate a single random word according to the distribution
    def draw(self):
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                    return word

    def generateSentence(self):
        pass

'''
Bigram language model
'''
class BigramModel():
    def __init__(self, corpus):
        self.uni_counts = defaultdict(float)
        self.counts = {}
        self.total = 0.0
        self.context = defaultdict(float)
        self.uniModel = UnigramModel(corpus)

        self.uniModel.train(corpus)
        self.train(corpus)

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        pass

    # Returns the probability of a bigram in the distribution
    def prob(self, word1, word2):
        pass

    # Given the previous word, generate a single random word according to the distribution
    def draw(self, prev_word):
        rand = random.random()
        for pair in self.counts.keys():
            if pair[0] != prev_word:
                continue
            rand -= self.prob(pair[0], pair[1])
            if rand <= 0.0:
                return pair[1]

    # Generate a single a sentence according to the distribution
    def generateSentence(self):
        pass

def main():
    corpus = preprocess("shakespeare/j_caesar.xml")

    uni = UnigramModel(corpus)
    print(uni.generateSentence())

    bi = BigramModel(corpus)
    print(bi.generateSentence())


if __name__ == "__main__":
    main()
