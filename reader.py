import sc2reader
import numpy as np
import pickle
import os
from collections import Counter
from unitsList import UnitsList

path = "D:\\thesis\\allReplays"

ul = UnitsList()
unitHeaders = list()
datalist = list()
resultList = list()

count = 0
upgradeHeaders = set()
counter = Counter()
headersList = list()
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

def process_replay(replay):
    gameEvents = replay.events
    typesOfEvents = [x.name for x in gameEvents]
    typesOfEvents = set(typesOfEvents)
    player1Events = [x for x in replay.tracker_events if x.name=="UnitBornEvent"]

    parse_player_data(1, replay)
    parse_player_data(2, replay)

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


def parse_player_data(playerID, replay):
    gameEvents = replay.events
    winnerPid =  replay.winner.players[0].pid
    result = [1] if winnerPid == playerID else [0]
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
        datalist.append(cnt)
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

    j = 0
    cnt = Counter()

for file in os.listdir(path):
    try:
        print(file)
        replay = sc2reader.load_replay(path+'/'+file, load_level=4, debug=True)
        count +=1
        if len(replay.players) == 2 and replay.winner is not None:
            process_replay(replay)

        if count == 1000:
            count = 0
            resultsArray = np.array(resultList)

            dataListRefined = list()

            for c in datalist:
                count = 0
                tempList = list()
                for key in c:
                    value = [c[key]]
                    tempList.extend(value)
                dataListRefined.append(tempList)

            dataArray = np.array(dataListRefined)

            print(dataArray.shape)
            with open('D:\\thesis\\dataListall.txt', 'ab') as fp:
                np.save(fp, dataArray)

            with open('D:\\thesis\\resultsListall.txt', 'ab') as fp:
                np.save(fp, resultsArray)

            datalist.clear()
            resultList.clear()

    except (RuntimeError, TypeError, NameError):
        print("error occured")

    except Exception:
        print("error")


