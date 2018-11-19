import os
import pickle
import sc2reader

path = "D:\\thesis\\allReplays"
unitHeaders = list()
corruptReplays = list()

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


for file in os.listdir(path):
    print(file)
    try:
        replay = sc2reader.load_replay(path+'/'+file, load_level=4, debug=True)
        get_headers(replay)
    except:
        corruptReplays.append(file)
        print("CORRUPT FILE " + file)

with open('D:\\thesis\\headers2000.txt', 'wb') as fp:
    pickle.dump(unitHeaders, fp)