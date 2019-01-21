import os
import pickle
import sc2reader

path = "D:\\thesis\\allReplays"
unitHeaders = list()
zergHeaders = list()
protossHeaders = list()
terranHeaders = list()
randomRacePick = list()
corruptReplays = list()

def add_by_race(race):
    return ''


def get_headers(replay):
    gameEvents = replay.events
    allObjects = list(replay.objects.values())
    unitObjects = {x.name for x in allObjects if (x.is_army == True or x.is_worker == True) and x.owner is not None and x.owner.pid in (1, 2) and x.name not in unitHeaders}
    buildingObjects = {x.name for x in allObjects if x.is_building == True and x.owner.pid in (1, 2)}
    upgradeCompleteEvents = {x.upgrade_type_name for x in gameEvents if
                             x.name == "UpgradeCompleteEvent" and x.player.pid in (1, 2) and x.frame > 0}
    unitHeaders.extend(unitObjects)
    unitHeaders.extend(buildingObjects)
    unitHeaders.extend(upgradeCompleteEvents)

def get_headers_by_race(replay, file):
    gameEvents = replay.events
    allObjects = list(replay.objects.values())
    for i in range(1,3):
        player_race = replay.players[i - 1].pick_race
        if player_race == "Zerg":
            unitObjects = {x.name for x in allObjects if (
                        x.is_army == True or x.is_worker == True) and x.owner is not None and x.owner.pid == i and x.name not in zergHeaders}
            buildingObjects = {x.name for x in allObjects if x.is_building == True and x.owner.pid == i and x.name not in zergHeaders}
            upgradeCompleteEvents = {x.upgrade_type_name for x in gameEvents if
                                     x.name == "UpgradeCompleteEvent" and x.player.pid == i and x.frame > 0 and x.upgrade_type_name not in zergHeaders}
            zergHeaders.extend(unitObjects)
            zergHeaders.extend(buildingObjects)
            zergHeaders.extend(upgradeCompleteEvents)
        elif player_race == "Protoss":
            unitObjects = {x.name for x in allObjects if (
                    x.is_army == True or x.is_worker == True) and x.owner is not None and x.owner.pid == i and x.name not in protossHeaders}
            buildingObjects = {x.name for x in allObjects if
                               x.is_building == True and x.owner.pid == i and x.name not in protossHeaders}
            upgradeCompleteEvents = {x.upgrade_type_name for x in gameEvents if
                                     x.name == "UpgradeCompleteEvent" and x.player.pid == i and x.frame > 0 and x.upgrade_type_name not in protossHeaders}
            protossHeaders.extend(unitObjects)
            protossHeaders.extend(buildingObjects)
            protossHeaders.extend(upgradeCompleteEvents)
        elif player_race == "Terran":
            unitObjects = {x.name for x in allObjects if (
                    x.is_army == True or x.is_worker == True) and x.owner is not None and x.owner.pid == i and x.name not in terranHeaders}
            buildingObjects = {x.name for x in allObjects if
                               x.is_building == True and x.owner.pid == i and x.name not in terranHeaders}
            upgradeCompleteEvents = {x.upgrade_type_name for x in gameEvents if
                                     x.name == "UpgradeCompleteEvent" and x.player.pid == i and x.frame > 0 and x.upgrade_type_name not in terranHeaders}
            terranHeaders.extend(unitObjects)
            terranHeaders.extend(buildingObjects)
            terranHeaders.extend(upgradeCompleteEvents)
        else:
            randomRacePick.extend(file)

for file in os.listdir(path):
    print(file)
    try:
        replay = sc2reader.load_replay(path+'/'+file, load_level=4, debug=True)
        get_headers_by_race(replay, file)
    except:
        corruptReplays.append(file)
        print("CORRUPT FILE " + file)

with open('D:\\thesis\\headersZerg.txt', 'wb') as fp:
    pickle.dump(zergHeaders, fp)


with open('D:\\thesis\\headersProtoss.txt', 'wb') as fp:
    pickle.dump(protossHeaders, fp)

with open('D:\\thesis\\headersTerran.txt', 'wb') as fp:
    pickle.dump(terranHeaders, fp)

with open('D:\\thesis\\randomRace.txt', 'wb') as fp:
    pickle.dump(randomRacePick, fp)