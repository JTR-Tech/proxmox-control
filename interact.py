import paramiko
import os
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def ssh_init(host, user="root"):
    if(type(get_auth_key()) == paramiko.rsakey.RSAKey):
        if(test_pkey_connection(host, user, get_auth_key())):
            print('RSA key accepted. SSH connection established')
            #ssh.connect(host, pkey=get_auth_key())
            return True
    print('RSA key denied. Password authentication required')
    user_creds = get_user_creds(user)
    if(test_cred_connection(host, user_creds)):
        print('Creds accepted. SSH connection established')
        #ssh.connect(host, username=user_creds[0], password=user_creds[1])
        return True
    else:
        print('All authetication methods failed, try again')
        return False
            
def get_user_creds(user=None):
    if(user != None):
        print('Assuming username {0}'.format(user), end="")
        if(input(" (Y/N): ").lower() == "y"):
            passwd = get_user_pass(user)
            #print('DEBUG: user = {0} pass = {1}'.format(user, passwd))
        else:
            get_user_creds()
    else:
        user = get_username()
        passwd = get_user_pass(user)
    user_creds = (user, passwd)
    #print('DEBUG: user={0},pass={1}'.format(user_creds[0],user_creds[1]))
    return user_creds

def get_username():
    user = input('enter username for ssh connection')
    try:
        user = str(user)
        return user
    except:
        print("invaild username, must be string")
        get_username()
            
def get_user_pass(user):
    passwd = input('Please enter password for "{0}": '.format(user))
    try:
        passwd = str(passwd)
        return passwd
    except:
        print('invaild password, must be string')
        get_user_pass(user)

def get_auth_key():
    homedir = os.environ['HOME']
    priv_key_file = '{0}/.ssh/id_rsa'.format(homedir)
    try:
        priv_key = paramiko.RSAKey.from_private_key_file(priv_key_file)
        return priv_key
    except:
        return None    

def test_pkey_connection(host, user, auth_key):
    try:
        ssh.connect(host, username=user, pkey=auth_key)
        #stdin, stdout, stderr = ssh.exec_command("echo 'pkey connection Successful'")
        #stdin.close()
        #for line in stdout.read().splitlines():
            #print(host + ': %s: %s' % (host[0], line))
        return True
    except:
        print("failed pkey connection") 
        return False
    
def test_cred_connection(host, user_creds):
    print('DEBUG: {0} {1} {2}'.format(host, user_creds[0], user_creds[1]))
    try:
        #print('DEBUG: {0} {1} {2}'.format(host, user_creds[1], user_creds[2]))
        ssh.connect(host, username=str(user_creds[0]), password=str(user_creds[1]))
        #stdin, stdout, stderr = ssh.exec_command("echo 'cred connection Successful'")
        #stdin.close()
        #for line in stdout.read().splitlines():
        #    print(host + ': %s: %s' % (host[0], line))
        return True
    except:
        print("failed cred connection") 
        return False
    
def run_command(host, command):
    if(ssh_init(host) == True):
        stdin, stdout, stderr = ssh.exec_command(command)
        stdin.close()
        for line in stdout.read().splitlines():
            print(host + ': %s: %s' % (host[0], line))
    else:
        ssh_init(host)
        
if __name__ == '__main__':
    if(len(sys.argv) == 3):
        run_command(sys.argv[1], sys.argv[2])
    elif(len(sys.argv) == 4):
        ssh_init(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("host, command argument required")



    