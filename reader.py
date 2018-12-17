import sc2reader
import numpy as np
import pickle
import os
from collections import Counter
from collections import Set

path = "D:/thesis/trainReplays"

unitHeaders = list()
datalist = list()
resultList = list()
count = 0
upgradeHeaders = set()
counter = Counter()
headersList = list()

maxFrame = 999999
with open('D:\\thesis\\headers2000.txt', 'rb') as f:
    headersList = pickle.load(f)

class ObserveEvent:
    def __init__(self, name, frame, value):
        self.name = name
        self.frame = frame
        self.value = value

class BornEvent:
    def __init__(self, buildingName, finishTime):
        self.name = buildingName
        self.frame = finishTime

class DeathEvent:
    def __init__(self, buildingName, destroyTime):
        self.name = buildingName
        self.frame = destroyTime

def getFrame(o):
    return o.frame

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def get_events(playerID, replay):
    gameEvents = replay.events
    # unitBornEvents = [x for x in gameEvents if x.name == 'UnitBornEvent' and x.control_pid == playerID and x.unit.name[0:4] != "Beac"]
    # unitDiedEvents = [x for x in gameEvents if x.name == 'UnitDiedEvent' and x.unit.owner != None and x.unit.owner.pid == playerID ]
    allObjects = list(replay.objects.values())
    buildingObjects = [x for x in allObjects if
                       x.is_building == True and x.owner is not None and x.owner.pid == playerID]
    buildingbornEvents = list()
    buildingDiedEvents = list()
    for bd in buildingObjects:
        if bd.finished_at != None:
            be = ObserveEvent(bd.name, bd.finished_at, 1)
            buildingbornEvents.append(be)
        if bd.died_at != None:
            bde = ObserveEvent(bd.name, bd.died_at, -1)
            buildingDiedEvents.append(bde)

    unitObjects = [x for x in allObjects if
                   (x.is_army == True or x.is_worker == True) and x.owner is not None and x.owner.pid == playerID]
    unitBornEvents = list()
    unitDiedEvents = list()
    for uo in unitObjects:
        if uo.finished_at != None:
            ue = ObserveEvent(uo.name, uo.finished_at, 1)
            unitBornEvents.append(ue)
        if uo.died_at != None:
            ude = ObserveEvent(uo.name, uo.died_at, -1)
            unitDiedEvents.append(ude)

    upgradeCompleteEvents = [x for x in gameEvents if
                             x.name == "UpgradeCompleteEvent" and x.player.pid == playerID and x.frame > 0]
    upgradeEvents = list()
    for uce in upgradeCompleteEvents:
        ude = ObserveEvent(uce.upgrade_type_name, uce.frame, 1)
        upgradeEvents.append(ude)

    allEvents = list()
    allEvents.extend(unitBornEvents)
    allEvents.extend(unitDiedEvents)
    allEvents.extend(buildingbornEvents)
    allEvents.extend(buildingDiedEvents)
    allEvents.extend(upgradeEvents)
    allEvents.sort(key=getFrame)
    return allEvents

def events_into_list(events, percentOfEvents):
    cnt = Counter(headersList)
    event_length = len(events)
    take_event = events[event_length - int(percentOfEvents * event_length)] #For last percentOfEvents
    #take_event = events[int(percentOfEvents * event_length) - 1] #For first percentOfEvents
    playerData = list()
    for key in cnt:
        cnt[key] = 0
    while len(events) > 0:
        cnt[events[0].name] += events[0].value
        event_frame = events[0].frame
        sub_cnt = Counter(cnt)
        sub_cnt["Frame"] = event_frame
        playerData.append(sub_cnt)
        events.pop(0)
    target_frame = take_event.frame
    p_data = [x for x in playerData if x['Frame'] >= target_frame] #For last percentOfEvents
    #p_data = [x for x in playerData if x['Frame'] <= target_frame] #For first percentOfEvents
    return p_data

def parse_replay(replay):
    allEvents = get_events(1,replay)
    allEvents.sort(key=getFrame)
    global maxFrame
    maxFrame = allEvents[len(allEvents) - 1].frame
    minFrame = allEvents[0].frame
    oppEvents = get_events(2,replay)
    if len(allEvents) > 50 and len(oppEvents) > 50:
        playerStats = events_into_list(allEvents,.03)

        oppStats = events_into_list(oppEvents, 1)
        winnerPid = replay.winner.players[0].pid
        result = [1, 0] if winnerPid == 1 else [0, 1]
        player1 = list()
        for e in playerStats:
            candidates = [x for x in oppStats if x["Frame"] <= e["Frame"]]
            tempList1 = list()
            tempList2 = list()
            if len(candidates) > 0:
                appendEntry = candidates[-1]
                for key,value in e.items():
                    tempList1.append(value)
                for key,value in appendEntry.items():
                    if key != "Frame":
                        tempList2.append(value)
                player1.append(tempList1+tempList2)
                resultList.append(result)
        datalist.extend(player1)
    else:
        print("Replay rejected due to low number of events")


def unique(list1):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
            # print list
    return unique_list

def get_headers(replay):
    gameEvents = replay.events
    allObjects = list(replay.objects.values())
    unitObjects = {x.name for x in allObjects if (x.is_army == True or x.is_worker == True) and x.owner.pid in (1, 2) and x.name not in unitHeaders}
    buildingObjects = {x.name for x in allObjects if x.is_building == True and x.owner.pid in (1, 2)}
    upgradeCompleteEvents = {x.upgrade_type_name for x in gameEvents if
                             x.name == "UpgradeCompleteEvent" and x.player.pid in (1, 2) and x.frame > 0}
    unitHeaders.extend(unitObjects)
    unitHeaders.extend(buildingObjects)
    unitHeaders.extend(upgradeCompleteEvents)


dataPath = 'D:\\thesis\\datatrainlast3perc.npy'
LabelsPath = 'D:\\thesis\\dataOuttrainlast3perc.npy'
maxFrame = 0
minFrame = 10000

for file in os.listdir(path):
    try:
        replay = sc2reader.load_replay(path+'/'+file, load_level=4, debug=True)
        if len(replay.players) == 2 and replay.winner is not None:
            print(file)
            parse_replay(replay)
            count += 1
        '''
        if count == 500:
            count = 0
            resultsArray = np.array(resultList)
            dataArray = np.array(datalist)
            with open(dataPath, 'a') as fp:
                for dl in datalist:
                    fp.write(dl)
            with open(LabelsPath, 'a') as fp:
                for rl in resultList:
                    fp.write(rl)
            datalist.clear()
            resultList.clear()
        '''
    except Exception:
        print("error")


resultsArray = np.array(resultList)
dataArray = np.array(datalist)

with open(dataPath, 'ab') as fp:
    pickle.dump(datalist,fp)
with open(LabelsPath, 'ab') as fp:
    pickle.dump(resultList,fp)

'''

def events_into_list(events):
    cnt = Counter(headersList)
    playerData = list()
    for key in cnt:
        cnt[key] = 0
    while len(events) > 0:
        cnt[events[0].name] += events[0].value
        eventFrame = events[0].frame
        sub_cnt = Counter(cnt)
        sub_cnt["Frame"] = eventFrame
        playerData.append(sub_cnt)
        events.pop(0)
    return playerData

def process_replay(replay):
    gameEvents = replay.events
    typesOfEvents = [x.name for x in gameEvents]
    typesOfEvents = set(typesOfEvents)
    player1Events = [x for x in replay.tracker_events if x.name=="UnitBornEvent"]

    parse_player_data(1, replay)
    parse_player_data(2, replay)


def parse_player_data(playerID, replay):
    gameEvents = replay.events
    winnerPid =  replay.winner.players[0].pid
    result = [1,0] if winnerPid == playerID else [0,1]
    #unitBornEvents = [x for x in gameEvents if x.name == 'UnitBornEvent' and x.control_pid == playerID and x.unit.name[0:4] != "Beac"]
    #unitDiedEvents = [x for x in gameEvents if x.name == 'UnitDiedEvent' and x.unit.owner != None and x.unit.owner.pid == playerID ]
    allObjects = list(replay.objects.values())
    buildingObjects = [x for x in allObjects if x.is_building == True and x.owner is not None and x.owner.pid == playerID]
    buildingbornEvents = list()
    buildingDiedEvents = list()
    for bd in buildingObjects:
        if bd.finished_at != None:
            be = ObserveEvent(bd.name,bd.finished_at, 1)
            buildingbornEvents.append(be)
        if bd.died_at != None:
            bde = ObserveEvent(bd.name,bd.died_at, -1)
            buildingDiedEvents.append(bde)

    unitObjects = [x for x in allObjects if (x.is_army == True or x.is_worker == True)and x.owner is not None and x.owner.pid == playerID]
    unitBornEvents = list()
    unitDiedEvents = list()
    for uo in unitObjects:
        if uo.finished_at != None:
            ue = ObserveEvent(uo.name, uo.finished_at, 1)
            unitBornEvents.append(ue)
        if uo.died_at != None:
            ude = ObserveEvent(uo.name, uo.died_at, -1)
            unitDiedEvents.append(ude)

    upgradeCompleteEvents = [x for x in gameEvents if x.name == "UpgradeCompleteEvent" and x.player.pid == playerID and x.frame > 0]
    upgradeEvents = list()
    for uce in upgradeCompleteEvents:
        ude= ObserveEvent(uce.upgrade_type_name, uce.frame, 1)
        upgradeEvents.append(ude)

    allEvents = list()
    allEvents.extend(unitBornEvents)
    allEvents.extend(unitDiedEvents)
    allEvents.extend(buildingbornEvents)
    allEvents.extend(buildingDiedEvents)
    allEvents.extend(upgradeEvents)
    allEvents.sort(key=getFrame)

    cnt = Counter(headersList)
    for key in cnt:
        cnt[key] = 0

    while len(allEvents) > 0:
        cnt[allEvents[0].name] += allEvents[0].value
        cnt["Frame"] = allEvents[0].frame
        eventFrame = allEvents[0].frame
        sub_cnt = Counter(cnt)
        sub_cnt["Frame"] = eventFrame
        if (eventFrame > 12000):
            datalist.append(sub_cnt)
            resultList.append(result)
        allEvents.pop(0)

    # Events saved for future analysis, not used at the moment
    playerStatsEvents = [x for x in gameEvents if x.name == "PlayerStatsEvent" and x.player.pid == playerID]
    basicCommandEvents = [x for x in gameEvents if x.name == "BasicCommandEvent" and x.player.pid == playerID]
    targetPointCommandEvents = [x for x in gameEvents if x.name == "TargetPointCommandEvent" and x.player.pid == playerID]
    selectionEvents = [x for x in gameEvents if x.name == "SelectionEvent" and x.player.pid == playerID]
    unitDoneEvents = [x for x in gameEvents if x.name == "UnitDoneEvent" and x.unit.owner.pid == playerID ]
    progressEvents = [x for x in gameEvents if x.name == "ProgressEvent" ]
    lenUnitDiedEvents = len(unitDiedEvents)
    # End of unused events
'''
