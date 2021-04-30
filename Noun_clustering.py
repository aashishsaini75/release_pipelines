import sys
import paramiko as pm
sys.stderr = sys.__stderr__
HOST = '52.38.74.114'
USER = 'ubuntu'
# PKEY = 'C:/Users/Shorthillstech/Downloads/Rohit-NLP.pem'
client = pm.SSHClient()
client.load_system_host_keys()
# client.load_host_keys(os.path.expanduser('~/.ssh/authorized_keys'))

class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

client.set_missing_host_key_policy(AllowAllKeys())
client.connect(HOST, username=USER, key_filename='C:/Users/Shorthillstech/Documents/Rohit-NLP.pem',banner_timeout=106400,timeout=106400)
channel = client.invoke_shell()
channel.settimeout(106400)
stdin = channel.makefile('wb',106400)
stdout = channel.makefile('rb',106400)

stdin.write(
    '''export PYTHONPATH=/home/ubuntu/bvrblackbox && source ~/venv/bin/activate && cd bvrblackbox/helios/ml_models && python ml_task_manager_for_noun_cluster.py ../../configs/helios.ini''')

stdin.write('''
    exit
    ''')
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        stdoutLines = stdout.readlines()
        for i in stdoutLines:
            print(str(str(i)+'\n').replace("\r","").replace('\n',''))
stdout.close()
stdin.close()
client.close()

