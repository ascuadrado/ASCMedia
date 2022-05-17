from youtubesearchpython import VideosSearch

videoName = "my ex's best friend (with blackbear) Machine Gun Kelly lyrics"
timeS = 139460/1000

videosSearch = VideosSearch(videoName, limit = 5)

r = videosSearch.result()

for video in r['result']:
    print(video['duration'] + ' ' + video['title'] + ' - ' + video['link'])

def getTimeDif(ts, v):
    timeV = v['duration'].split(':')
    timeV = int(timeV[0])*60 + int(timeV[1])

    t_diff = abs(timeV-timeS)
    return t_diff


bestV = r['result'][0]
bestTime = getTimeDif(timeS, r['result'][0])

for v in r['result']:
    timeV = getTimeDif(timeS, v)
    if (bestTime > timeV):
        bestTime = timeV
        bestV = v

print(getTimeDif(timeS, bestV))
bestV['link']

def returnLink(T, lyrics=True):
    # Create name for search
    name = ''
    name.append(T['track']['name'])
    for artist in T['track']['artists']:
        name.append(' ' + artist['name'])

    # Search for video
    videosSearch = VideosSearch(name, limit = 5)
    r = videosSearch.result()

    # Find best time match
    bestV = r['result'][0]
    bestTime = getTimeDif(timeS, r['result'][0])

    for v in r['result']:
        timeV = getTimeDif(timeS, v)
        if (bestTime > timeV):
            bestTime = timeV
            bestV = v

    # If there is a big difference (3s), raise alert
    if bestTime > 3:
        print("Big difference: %s %d" % (T['track']['name'], bestTime))

    return bestV['link']
