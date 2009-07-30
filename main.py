import psyco
psyco.full()

import consensus

def loaddata():
    out = {}
    for line in file('download/data.txt'):
        user, repo = line.strip().split(':')
        out.setdefault(user, {})[repo] = 1
    return out

def calculate():
    m = consensus.SMSimilarityModel(loaddata())
    fh = file('results.txt', 'w')
    for line in file('download/test.txt'):
        recs = m.getRecommendations(line.strip(), limit=10)
        out = '%s:%s\n' % (line.strip(), ','.join(x for x,y in recs))
        print out
        fh.write(out)
        fh.flush()

if __name__ == "__main__":
    calculate()