import socket
from multiprocessing.dummy import Pool as ThreadPool 

socket.setdefaulttimeout(0.001)

def tryport(address):
    """tryport(address) uses the socket module to test a given IP, Port 
       tuple for a successful connection, indicating that IP,port is open
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(s.connect_ex(address) == 0):
        return address
    s.close()    

def scanport(port, ip=None, subnet="192.168", threads=20):
    """scanport() calls tryport() on all possible addresses of the (default: 192.168)
       subnet in a multi-threaded implimentation to quickly detect if the port
       is up on a reachable local network. 
    """
    pool = ThreadPool(threads)
    addresses = []
    port_hosts = []
    if(ip == None):
        for i in range(1, 255):
            for k in range(1, 255):
                addresses.append(('{0}.{1}.{2}'.format(subnet, i, k), port))
        result = pool.map(tryport, addresses)
        pool.close()
        pool.join()
        port_hosts = [x for x in result if not x is None]
    else:
        if(tryport(ip, port)):
            print('Proxmox host found at {0}'.format(addr))
            port_hosts.append(addr)
    return port_hosts
