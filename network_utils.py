import subprocess
import platform
import re

def check_network_conditions(target_ip='127.0.0.1', max_loss_percent=5):
    count = 4
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', param, str(count), target_ip]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    loss_percent = 100 
    if platform.system().lower() == 'windows':
        m = re.search(r'Lost = \d+ \((\d+)% loss\)', output)
        if m:
            loss_percent = int(m.group(1))
    else:
        m = re.search(r'(\d+)% packet loss', output)
        if m:
            loss_percent = int(m.group(1))

    return loss_percent <= max_loss_percent
