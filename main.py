import psyco
psyco.full()

import consensus

def consensusformat(source):
    out = {}
    for user, repo in source:
        out.setdefault(user, {})[repo] = 1
    return out

def getdata():
    for line in file('download/data.txt'):
        yield line.strip().split(':') # user, repo

def userbasket(baskets, n):
    if n not in baskets: return []
    pgroups = suggest.intArray(len(baskets[n]))
    for n, k in enumerate(sorted(baskets[n])):
        pgroups[n] = k
    return pgroups

def initsuggest(source):
    import suggest
    userids = []
    repoids = []
    for user, repo in getdata():
        userids.append(int(user))
        repoids.append(int(repo))
    
    nusers = max(userids)
    nitems = max(repoids)
    ntrans = len(userids)
    
    users = suggest.intArray(ntrans)
    items = suggest.intArray(ntrans)
    for n, k in enumerate(userids):
        users[n] = k
    
    for n, k in enumerate(repoids):
        items[n] = k
    
    rhandle = suggest.SUGGEST_Init(nusers, nitems, ntrans, users, items, 2, 1, .4)
    
    baskets = {}
    for user, repo in getdata():
        baskets.setdefault(int(user), set()).add(int(repo))
    
    return (rhandle, baskets)

def recsuggest((rhandle, baskets), userid):
    userid = int(userid)
    pgroups = userbasket(baskets, userid)
    if not pgroups: return []
    npgroups = len(baskets[userid])
    results = suggest.intArray(10)
    n = suggest.SUGGEST_TopN(rhandle, npgroups, pgroups, 10, results)
    out = []
    for i in range(n):
        out.append(results[i])
    return [str(x) for x in out]

def harness(init, recommend):
    data = getdata()
    handle = init(data)
    fh = file('results.txt', 'w')
    for line in file('download/test.txt'):
        recs = recommend(handle, line.strip())
        out = '%s:%s\n' % (line.strip(), ','.join(recs))
        print out
        fh.write(out)
        fh.flush()

def tryconsensus():
    return harness(
      lambda x: consensus.SMSimilarityModel(consensusformat(x)),
      lambda m, x: (x for x,y in m.getRecommendations(x, limit=10))
    )

def trysuggest():
    return harness(initsuggest, recsuggest)

if __name__ == "__main__":
    import suggest
    trysuggest()
