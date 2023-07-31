from threading import Thread

from device_manager import Device
from utils import FileHandler, logger
from queue import Queue
from datetime import datetime
from time import sleep

THREADS = 3


class DeviceMonitor:
    def __init__(self, devices: list[Device], output_filepath: str) -> None:
        self.output_fileHandler = FileHandler(output_filepath, file_type='csv',
                                              default_data='DeviceId, DeviceName, Timestamp, Status\n')
        self.devices = devices
        self.job_queue: Queue = Queue()
        self.output_queue: Queue = Queue()

    def ping_ips(self) -> None:
        """Selected an ip from jobq queue and save its status to the output"""
        while True:
            try:
                # Getting Task from job queue
                task = self.job_queue.get()
                status = task.ping()  # Status Retrival
                logger.info(f"Ping id: {task.id}, Status: {('1' if status else '0')} ")
                if status:
                    self.output_queue.put([task.id, task.name, datetime.now(), status])
                else:
                    self.output_queue.put([task.ip, task.name, datetime.now(), 0])

            finally:
                self.job_queue.task_done()

    def write_output(self, delay: int = 300, once: bool = False) -> None:
        """
        Write Output to the CSV file 5 at a time
        Args:
           delay: int - Delay between the write in ms
           once: bool - To execute the function once
        Returns:
        """
        while True:
            logger.info('--- Writing Output to file --- ')
            task = [list(self.output_queue.get()) for _ in range(self.output_queue.qsize())]
            self.output_fileHandler.rewrite_file(task)
            if self.output_queue.qsize() > 0:
                self.output_queue.task_done()
            if once:
                break
            sleep(delay)

    def log_status(self):
        df = self.output_fileHandler.read_file()
        print(df)

    def start(self, delay: int = 300) -> None:
        try:
            # Creating Thread for ping and output
            for _ in range(THREADS):
                th = Thread(target=self.ping_ips, daemon=True)
                th.start()
            out = Thread(target=self.write_output, args=[delay / 3], daemon=True)

            out.start()
            cycle: int = 1
            # loop to set up ping every 5 minutes
            while True:
                logger.info(f"Cycle {cycle}")
                self.write_output(once=True)
                if len(self.devices) < 1:
                    raise ValueError(
                        f"No Device Data was found add some using \n python ping-monitor add-device")
                # adding elements to job queue
                for device in self.devices:
                    self.job_queue.put(device)
                print(self.job_queue.qsize())
                cycle += 1
                sleep(delay)
        except ValueError as err:
            print(err)
        except KeyboardInterrupt:
            print('The Process was terminated Forcefully')
            exit(0)
