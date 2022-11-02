from pycomm3 import LogixDriver
from pycomm3 import CIPDriver
import csv

#TODO: communicate with PLC and get the tags

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
    with LogixDriver(plcip) as plc:
        pass


def filter_tags():
    pass