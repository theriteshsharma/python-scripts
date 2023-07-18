import pandas as pd
from pythonping import ping
from datetime import datetime
from queue import Queue
from time import sleep
from threading import Thread
from pythonping.executor import SuccessOn

THREAD_WAIT_TIME = 20
THREADS = 3
OUTPUT_LIMIT = 1
SCRIPT_TIME = 5 * 60

job_queue = Queue()
output_queue = Queue()


def ping_ips(jobq: Queue, output: Queue):
    """
    Selected an ip from jobq queue and save its status to the output
    Args:
        jobq: Task Queue
        output: Output queue
    """
    while True:
        task = {}
        try:
            # Getting Task from job you
            task = jobq.get()
            response = ping(task['ip'], count=1)  # ping to ip
            status: int = int(response.success(SuccessOn.All))  # Status Retrival
            print(f"Ping id: {task['id']}, Status: {status} ")
            output.put([task['id'], task['name'], datetime.now(), status])
        except OSError:
            print(f"Invalid Ip {task['ip']}")
            output.put([task['id'], task['name'], datetime.now(), 0])
        finally:
            jobq.task_done()


def write_output(output: Queue, output_filename, once=False):
    """
    Write Output to the CSV file 5 at a time
    Args:
        once: bool
        output: Output Queue
    Returns:

    """
    while True:
        if output.qsize() > OUTPUT_LIMIT or (once and OUTPUT_LIMIT != 0):
            print('writing output')
            task = [list(output.get()) for _ in range((output.qsize() if once else OUTPUT_LIMIT))]
            pd.DataFrame(task).to_csv(output_filename, mode='a', header=False, index=False, )
            if output.qsize() > 0:
                output.task_done()
        if once:
            break


def monitor_device(input_filename, output_filename):
    try:

        # Creating Thread for ping and output
        for _ in range(THREADS):
            th = Thread(target=ping_ips, args=[job_queue, output_queue], daemon=True)
            th.start()
        out = Thread(target=write_output, args=[output_queue, output_filename], daemon=True)

        out.start()

        # loop to set up ping every 5 minutes
        while True:
            device_data = pd.read_json(input_filename)
            if device_data.empty:
                raise ValueError(
                    f"No Device Data was found in {input_filename} add some using \n python ping-monitor add-device")
            # adding elements to job queue
            for idx, row in device_data.iterrows():
                job_queue.put(row)
            print(job_queue.qsize())
            sleep(SCRIPT_TIME)
    except FileNotFoundError:
        print(f"Input file {input_filename} not found")
        exit(0)
    except ValueError as err:
        print(err)
    except KeyboardInterrupt:
        print('The Process was terminated Forcefully')
        write_output(output_queue, output_filename, once=True)
        exit(0)
