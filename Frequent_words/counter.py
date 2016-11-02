
def loadwords(fname):
    import os
    if os.path.exists(fname):
        new_words = set()
        with open(fname) as conn:
            for line in conn:
                new_words.add(line.strip().lower())

        return new_words
    else:
        return None


def run(path):
    import os
    import re
    from nltk.corpus import stopwords

    all_senti_sent_words = []
    answer = set()

    if os.path.exists(path):

        poslex = loadwords("./positive-words.txt")
        neglex = loadwords("./negative-words.txt")
        stoplex = set(stopwords.words('english'))
        errMsg = None

        if poslex is None:
            errMsg =  'Positive words file path does not exist'
        if neglex is None:
            errMsg = 'Negative words file path does not exist'
        if not poslex:
            errMsg = 'Positive words file is empty'
        if not neglex:
            errMsg = 'Negative words file is empty'

        if not errMsg:
            with open(path) as fin:
                for texts in fin:
                    lines = texts.lower().strip().split('.')
                    for line in lines:
                        words = set(re.sub('[^a-z]', ' ', line).split())

                        if words.intersection(poslex) or words.intersection(neglex):
                            all_senti_sent_words.extend(words)

                all_senti_sent_words = filter(lambda x: x not in stoplex and x not in poslex and x not in neglex and x != '', all_senti_sent_words)

                for senti_sent_word in all_senti_sent_words:

                    if all_senti_sent_words.count(senti_sent_word) >= 4:
                        answer.add(senti_sent_word)
        else:
            print errMsg
    else:
        print "path does not exist"

    return answer



