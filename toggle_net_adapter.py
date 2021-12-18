# pip install pyinstaller
# pyinstaller toggle_net_adapter.py --onefile --uac-admin --distpath ./ --name ToggleNetworkAdapter
from subprocess import Popen, PIPE
from time import sleep

network_adapter_name = "Ethernet"


def powershell_command(command):
    command_return = Popen(f"powershell.exe {command}", stdout=PIPE)
    command_return.wait()
    command_return = command_return.communicate()[0].decode('utf-8').strip()
    return command_return


if __name__ == "__main__":
    status = powershell_command(f"(Get-NetAdapter -Name '{network_adapter_name}').Status")
    if status == "Disabled":
        status = powershell_command(f"Enable-NetAdapter -Name '{network_adapter_name}' -Confirm:$false")
    elif status == "Up":
        status = powershell_command(f"Disable-NetAdapter -Name '{network_adapter_name}' -Confirm:$false")

    status = powershell_command(f"(Get-NetAdapter -Name '{network_adapter_name}').Status")
    if status is None or status == "":
        print(f"Toggling adapter {network_adapter_name} failed!")
    else:
        if status == "Disconnected":
            status += " (Enabled and Connecting)"
        print(f"Net-Adapter {network_adapter_name} is now {status}")

    sleep(2)
    raise SystemExit
