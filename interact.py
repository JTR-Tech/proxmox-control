import paramiko
import os
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def ssh_init(host, user="root"):
    """Initialize RSA key authentication, if this fails.
       fall back to password authentication.
    """
    if(type(get_auth_key()) == paramiko.rsakey.RSAKey):
        if(test_pkey_connection(host, user, get_auth_key())):
            print('DEBUG: RSA key accepted. SSH connection established')
            return True
    print('DEBUG: RSA key denied. Password authentication required')
    user_creds = get_user_creds(user)
    if(test_cred_connection(host, user_creds)):
        print('Credentials accepted. SSH connection established')
        return True
    else:
        print('All authetication methods failed, try again')
        return False
            
def get_user_creds(user=None):
    """Prompt the user for the password for the given user name.
       if the function is not given a name, prompt the user to 
       enter one.
    """
    if(user != None):
        print('Assuming username {0}'.format(user), end="")
        if(input(" (Y/N): ").lower() == "y"):
            passwd = get_user_pass(user)
        else:
            get_user_creds()
    else:
        user = get_username()
        passwd = get_user_pass(user)
    user_creds = (user, passwd)
    return user_creds

def get_username():
    """Get username from input
    """
    user = input('enter username for ssh connection')
    try:
        user = str(user)
        return user
    except:
        print("invaild username, must be string")
        get_username()
            
def get_user_pass(user):
    """Get password from input
    """
    passwd = input('Please enter password for "{0}": '.format(user))
    try:
        passwd = str(passwd)
        return passwd
    except:
        print('invaild password, must be string')
        get_user_pass(user)

def get_auth_key():
    """UNIX ONLY(needs updating for windows paths)
       Find the default ssh key, use this for RSA authentication
    """
    homedir = os.environ['HOME']
    priv_key_file = '{0}/.ssh/id_rsa'.format(homedir)
    try:
        priv_key = paramiko.RSAKey.from_private_key_file(priv_key_file)
        return priv_key
    except:
        return None    

def test_pkey_connection(host, user, auth_key):
    """Attempt to connect to server with provided RSA key
    """
    try:
        ssh.connect(host, username=user, pkey=auth_key)
        return True
    except:
        print("failed pkey connection") 
        return False
    
def test_cred_connection(host, user_creds):
    """Attept to connect to server with provided credentials
    """
    try:
        ssh.connect(host, username=str(user_creds[0]), password=str(user_creds[1]))
        return True
    except:
        print("failed Credentials connection") 
        return False
    
def run_command(host, command):
    """if ssh initialization was successful, run command on remote
       and print its output (this should be returned instead for 
       further processing)
    """
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



    