import pandas as pd
import re


def add_device(input_filepath):
    """
    Add Device to the Given File
    Args:
        input_filepath: file path

    Returns:

    """
    device_name = ''
    device_ip = ''
    validate_ip = False
    df = pd.read_json(input_filepath)
    print("Enter Device Details")
    while True:
        device_id: int = int(input("Device Id: "))
        if ('id' not in df.columns) or ('id' in df.columns and device_id not in df['id'].values):
            break
        print('Id is already Present Try Another one')
    while True:
        device_name: str = input('Device Name: ')
        if device_name != '':
            break
        print(" Name Cannot be Empty")
    while True:
        device_ip: str = input("Device Ip: ")
        validate_ip = re.compile(
            "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$").match(
            device_ip)
        if validate_ip:
            break
        print("Enter a Valid Ip")

    df = pd.concat([df, pd.DataFrame({"id": [device_id], "name": [device_name], "ip": [device_ip]})], ignore_index=True)
    df.to_json(input_filepath, orient='records')
    print('Device Added Succesfful!')
    print('---------------------------')


def delete_device(input_filepath, _id):
    """
    Delete a record from file
    Args:
        input_filepath: input file path
        _id: device_id

    Returns:

    """

    df = pd.read_json(input_filepath)
    print(f"Deleting Device with ID: {_id}")
    df.drop(df.index[df['id'] == _id], inplace=True)

    df.to_json(input_filepath, orient='records')
    print('Device Deleted Succesfful!')
    print('---------------------------')


def edit_device(input_filepath, _id):
    """
    Edit a Existing Device
    Args:
        input_filepath: input file
        _id: device id

    Returns:

    """
    df = pd.read_json(input_filepath)
    if df.empty:
        raise ValueError('No devices to edit add some to begin with')
    idx = df.index[df['id'] == _id]
    device = df.loc[idx]
    if len(device) == 0:
        raise ValueError('Invalid Device Id')

    device_name = device.values[0][1]

    device_name = input(f"Updated Device Name ({device_name}): ")
    while True:
        device_ip = input(f"Updated Device Ip ({device.values[0][2]}): ")
        validate_ip = (device_ip == '' or re.compile(
            "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$").match(
            device_ip))
        if validate_ip:
            break
        print("Enter a Valid Ip")

    print(device_name, device_ip)
    df.loc[idx] = [device.values[0][0], (device_name if device_name != '' else device.values[0][1]),
                   (device_ip if device_ip != '' else device.values[0][2])]
    df.to_json(input_filepath, orient='records')
    print("Device Updated Successfully!")
    print('---------------------------')


def list_devices(file_name):
    """
    List all Devices
    Args:
        file_name: file path

    Returns:

    """
    print("All Devices on to Monitor are:")
    df = pd.read_json(file_name)
    print(df)
    print('---------------------------')
