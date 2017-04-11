import scan.py

def write_status(output):
    try:
        file = open('.vmStatus', 'w')
    except:
        file = open('.vmStatus', 'w+')
    ##stuff for file here

def list_vms(address):
    
    