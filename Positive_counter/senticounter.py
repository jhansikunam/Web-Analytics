import pprint
import os


def loadwords(fname):
    if os.path.exists(fname):
        new_words = set()
        with open(fname) as conn:
            for line in conn:
                new_words.add(line.strip().lower())

        return new_words
    else:
        return None


def run(path):
    d = {}

    if os.path.exists(path):
        positive_words = loadwords("./positive-words.txt")
        if positive_words is None:
            print 'path does not exist for positive words file'
        elif not positive_words:
            print 'Positive words file is empty'
        else:
            with open(path) as fin:
                for lines in fin:
                    temp = lines.lower().strip().split()
                    if temp:
                        for positive_word in list(positive_words):
                            if positive_word in temp:
                                if d.get(positive_word) is not None:
                                    d[positive_word] += 1
                                else:
                                    d[positive_word] = 1

    else:
        print "path does not exist for reviews file"

    return d

if __name__ == "__main__":
    pprint.pprint(run("./textfile"))
