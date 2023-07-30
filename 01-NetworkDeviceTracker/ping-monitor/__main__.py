#####################################################
#  Module Name: Network Device Analyzer
#  Developer: Ritesh Sharma @ rsharma3499@gmail.com
#####################################################
import argparse
import textwrap
import os

from actions import *
from monitor import *

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

    parser.add_argument('-i', '--input', default='device_data.json')
    parser.add_argument('-o', '--output', default='output.csv')
    command = parser.parse_args()

    input_filename, output_filename = command.input, command.output
    # Creating Empty File
    if not os.path.isfile(input_filename):
        print(f"{input_filename} Not Found \n Creating... {input_filename}")
        file = open(input_filename, 'a')
        file.write('[]')
        file.close()
    if not os.path.isfile(output_filename):
        print(f"{output_filename} Not Found \n Creating... {input_filename}")
        file = open(output_filename, 'a')
        file.write('DeviceId, DeviceName, Status, Timestamp\n')
        file.close()
    try:
        match command.action:
            case 'list-devices':
                list_devices(input_filename)
            case 'add-device':
                add_device(input_filename)
            case "delete-device":
                delete_device(input_filename, int(command.id))
            case "edit-device":
                edit_device(input_filename, int(command.id))
            case None:
                monitor_device(input_filename, output_filename)
            case _:
                print(f"{command} is a invalid command ")
    except Exception as err:
        print(err)
        print("Terminated on Exception!")
        exit(1)


if __name__ == "__main__":
    main()
