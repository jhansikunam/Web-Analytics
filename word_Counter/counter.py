
def run(path):
    import os
    if os.path.exists(path):
        words = []
        count = {}

        with open(path) as fin:
            for lines in fin:
                words.extend(lines.lower().strip().split(' '))
        words=filter(lambda x:x != '',words)
        for k in words:
            if count.get(k):
                count[k] += 1
            else:
                count[k] = 1
        return count
    else:
        return 'path does not exist'


print run("/Users/Janu/PycharmProjects/First_Python/textfile")

