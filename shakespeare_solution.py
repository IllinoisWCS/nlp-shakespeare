import re, random
from collections import defaultdict


START_TAG = "<LINE>"
END_TAG = "</LINE>"

'''
Preprocess corpus
'''
def preprocess(play):

    with open(play) as f:
        corpus = f.read()

    corpus = corpus.split("\n")
    corpus = [(line[:6] + " " + line[6:-7] + " " + line[-7:]) for line in corpus if len(line) > len(START_TAG) and line[:6] == START_TAG]

    # Pad punctuation with spaces
    corpus = [re.sub('([.,:;!?()])', r' \1 ', line) for line in corpus]
    corpus = [re.sub('\s{2,}', ' ', line) for line in corpus]

    return corpus

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
        if self.counts:
            return
        for sen in corpus:
            sen = sen.split(" ")
            for word in sen:
                if word == START_TAG:
                    continue
                self.counts[word] += 1.0
                self.total += 1.0

    # Returns the probability of word in the distribution
    def prob(self, word):
        return self.counts[word]/self.total

    # Generate a single random word according to the distribution
    def draw(self):
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                    return word

    def generateSentence(self):
        sentence = [START_TAG]
        word = START_TAG
        while word != END_TAG:
            word = self.draw()
            sentence.append(word)
        
        sentence = " ".join(sentence)
        return sentence

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
        comb = []
        if self.counts:
            return
        for sen in corpus:
            sen = sen.split(" ")
            for word in sen:
                comb.append(word)
        for i in range(len(comb) - 1):
            key = (comb[i], comb[i+1])
            if key in self.counts:
                self.counts[key] += 1
            else:
                self.counts[key] = 1
            self.context[key[0]] += 1
            self.context[""] += 1

    # Returns the probability of a bigram in the distribution
    def prob(self, word1, word2):
        return self.counts[(word1, word2)]/self.context[word1]

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
        sentence = [START_TAG]
        prev_word, word = START_TAG, ""

        while word != END_TAG:
            word = self.draw(prev_word)
            sentence.append(word)
            prev_word = word

        sentence = " ".join(sentence)
        return sentence

def main():
    corpus = preprocess("shakespeare/j_caesar.xml")

    uni = UnigramModel(corpus)
    print(uni.generateSentence())

    bi = BigramModel(corpus)
    print(bi.generateSentence())


if __name__ == "__main__":
	main()
