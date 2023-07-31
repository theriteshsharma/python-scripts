#####################################################
#  Module Name: Network Device Analyzer
#  Developer: Ritesh Sharma @ rsharma3499@gmail.com
#####################################################
import argparse
import textwrap

from device_manager import Device,DeviceManger
from device_monitor import DeviceMonitor

HEADER = """
            +-------------------------+ 
            Python Device Analyzer 
            Ritesh Sharma @ rsharma3499@gmail.com 
            +-------------------------+
            Usage: 
            python main.py <action> <args>
            Available action:
            | action | Args | Description              |
            --------------------------------------------
            | ping           | <ip> | ping a specific ip
            | log-status     |      | Log status
            | list-devices   |      | list all devices
            | add-device     |      | add a New Device
            | delete-device  | <id> | To Delete an device by id
            | edit-device    | <id> | To Edit a give device
          """


def main() -> None:
    # Setting up the Parser for Arguments
    parser = argparse.ArgumentParser(prog="python ping-monitor",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(HEADER))
    sub_parser = parser.add_subparsers(dest='action')

    sub_parser.add_parser('list-devices')
    sub_parser.add_parser('add-device')
    sub_parser.add_parser('delete-device').add_argument('id', type=int)
    sub_parser.add_parser('edit-device').add_argument('id', type=int)
    sub_parser.add_parser('ping').add_argument('ip', type=str)
    sub_parser.add_parser('log-status')

    parser.add_argument('-i', '--input', default='device_data.json')
    parser.add_argument('-o', '--output', default='output.csv')

    # Pars
    command = parser.parse_args()
    input_filename, output_filename = command.input, command.output

    device_manger: DeviceManger = DeviceManger(input_filename)

    match command.action:
        case 'ping':
            device = Device('', '', command.ip)
            print(f"Status for ip: {command.ip} is {device.ping()}")
        case 'list-devices':
            device_manger.list_devices()
        case 'add-device':
            device_manger.add_device()
        case "delete-device":
            device_manger.delete_device(command.id)
        case "edit-device":
            device_manger.edit_device(command.id)
        case "log-status":
            monitor_device = DeviceMonitor(device_manger.devices, output_filename)
            monitor_device.log_status()
        case None:
            monitor_device = DeviceMonitor(device_manger.devices, output_filename)
            monitor_device.start(delay=10);
        case _:
            print(f"{command} is a invalid command ")


if __name__ == "__main__":
    main()
