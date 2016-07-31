import pickle
import ranking
import core
import numpy
import collections
import datetime
import dateutil.parser


def getrankings(f):
    return ranking.getRankings(getmatches(f))


def getmatches(firebase):
    fMatches = firebase.get('/matches', None)
    matchObjs = []
    if fMatches:
        for match in fMatches.values():
            matchObjs.append(core.Match(
                match['players1'],
                match['players2'],
                match['score1'],
                match['score2'],
                dateutil.parser.parse(match['when'])
            ))
    return matchObjs


def getrecent(f, n=3):
    return sorted(getmatches(f), key=lambda x: x.when, reverse=True)[:n]


def getgamecounts(f):
    matches = getmatches(f)
    r = collections.defaultdict(int)
    for m in matches:
        for p in m.players1 + m.players2:
            r[p] += 1
    return r


def getlastgame(f, uid):
    matches = getmatches(f)
    times = []
    for m in matches:
        if uid in m.players1 + m.players2:
            times.append(m)
    return sorted(times, key=lambda x: x.when)[-1]


def getlastgameall(f):
    matches = getmatches(f)
    latest = collections.defaultdict(lambda: datetime.datetime(1900, 1, 1))
    for m in matches:
        for uid in m.players1 + m.players2:
            if m.when > latest[uid]:
                latest[uid] = m.when
    return latest


def addmatch(firebase, m):
    data = {
        'players1': m.players1,
        'players2': m.players2,
        'score1': m.score1,
        'score2': m.score2,
        'when': m.when
    }
    snapshot = firebase.post('/matches', data)
    return snapshot['name']


def deletematch(firebase, mid):
    firebase.delete('/matches', mid)
