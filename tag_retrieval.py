from pycomm3 import LogixDriver
from pycomm3 import CIPDriver




def discoverPLC():
    discovered_plc = CIPDriver.discover()
    if discovered_plc:
        print("plc's available")
        with open('plcinfo.txt', 'w') as file:
            print(discovered_plc, file=file)
        return True
    else:
        return True


def get_tags(plcip):
    plc = LogixDriver(plcip)
    taglist = plc.get_tag_list()
    if taglist:
        with open ('taglist', 'w+') as f:
            print(taglist, file=f)
        return True
    else:
        return False

def filter_tags():
    pass