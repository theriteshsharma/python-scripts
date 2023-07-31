from pythonping import ping
from pythonping.executor import ResponseList, SuccessOn
from utils import logger, FileHandler
import pandas as pd
import re


class Device:
    """
    Device Class for all the Devices on Network
    id: str - Device_id
    name: str - Device Name
    ip: str - Ip Address for the Device
    """

    def __init__(self, device_id: str, name: str, ip: str) -> None:
        self.id = device_id
        self.name = name
        self.ip = ip

    def update(self, device_name: str, device_ip: str) -> None:
        """
        Update the Current instance of Device
        Args:
            device_name: Updated Name
            device_ip: Updated Ip

        Returns: None
        """
        self.name = device_name
        self.ip = device_ip

    def to_json(self) -> dict:
        """Convert Device class to JSON Object"""
        return {"id": self.id, "name": self.name, "ip": self.ip}

    def __str__(self) -> str:
        return "{0:<7}{1:20}{2:5}".format(self.id, self.name, self.ip)

    def __repr__(self):
        return "Device({},{},{})".format(self.id, self.name, self.ip)

    def ping(self) -> bool:
        """Ping Current Device
        Returns: bool
        """
        try:
            response: ResponseList = ping(self.ip, count=1)  # ping to ip
            return response.success(SuccessOn.All)  # Status Retrival
        except OSError as err:
            logger.info(f"Invalid Ip {self.ip}:")
            logger.info(err)
            return False


class DeviceManger:
    """
    Manger Class to manage list of Device and Perform Actions on it
    """

    def __init__(self, data_filepath: str) -> None:

        self.file_handler = FileHandler(data_filepath, file_type='json', default_data='[]')
        file_data: pd.DataFrame = self.file_handler.read_file()
        self.devices: list[Device] = [Device(*row) for row in file_data.values.tolist()]
        logger.info(f"{len(self.devices)} devices listed Successfully!")

    def save(self) -> None:
        """
        Save Devices list to the input File
        """
        data = [device.to_json() for device in self.devices]
        self.file_handler.rewrite_file(data)

    def find_by_id(self, device_id: str) -> Device | None:
        """
        Find a Device by device_id
        Args:
            device_id: Device id to find
        Returns: Device | none
        """
        try:
            #  filter event with give id and return the first element
            return next(filter(lambda device: str(device.id) == str(device_id), self.devices))
        except StopIteration:
            return None

    def list_devices(self) -> None:
        """List all Devices"""
        print("{0:<7}{1:20}{2:5}".format("id", "name", "ip"))
        for device in self.devices:
            print(device)

    def add_device(self) -> None:
        """Takes user input and adds a device to the device manager"""
        print("Enter Device Details")
        while True:
            device_id = input("Device Id: ")
            if device_id != '' and self.find_by_id(device_id) is None:
                break
            print('Id is already Present Try Another one')
        while True:
            device_name: str = input('Device Name: ').strip()
            if device_name != '':
                break
            print("Name Cannot be Empty")
        while True:
            device_ip: str = input("Device Ip: ").strip()
            validate_ip = re.compile(
                "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$") \
                .match(device_ip)
            if validate_ip:
                break
            print("Enter a Valid Ip!")

        print(Device(device_id, device_name, device_ip))
        self.devices.append(Device(device_id, device_name, device_ip))
        self.save()
        print('Device Added Successfully!')
        print('---------------------------')

    def delete_device(self, device_id: str) -> bool:
        """
        Delete a Device with given Id
        Args:
            device_id: Device id to be deleted
        """
        device = self.find_by_id(device_id)
        if device:
            choice = input(f"Deleting: {repr(device)}\n  Are you sure ? (y/n): ")
            if choice.lower() == 'y':
                self.devices.remove(device)
                self.save()
                logger.info(f"Device with Id {device_id} deleted Successfully!")
                return True
            else:
                return False
        else:
            print(f"Device with id {device_id} Not Found!")
            return False

    def edit_device(self, device_id: str) -> None:
        """
        Edit Device with Given id
        Args:
            device_id: Device id to be edited
        """
        device = self.find_by_id(device_id)
        if device:
            print(f"Editing Device with Id {device_id}")
            device_name = input(f"Updated Device Name ({device.name}): ")
            while True:
                device_ip = input(f"Updated Device Ip ({device.ip}): ")
                validate_ip = (device_ip == '' or re.compile("^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}"
                                                             "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$").match(
                    device_ip))
                if validate_ip:
                    break
                print("Enter a Valid Ip")

            device_name = device.name if device_name == "" else device_name
            device_ip = device.ip if device_ip == "" else device_ip
            device.update(device_name, device_ip)
            self.save()
            logger.info(f"Device id {device_id} Updated Successfully!")
        else:
            print(f"Device with id {device_id} Not Found Please add a valid id")
