#####################################################
#  Module Name: Automate ping status check
#  Developer: Ritesh Sharma @ rsharma3499@gmail.com
#####################################################
import argparse
import pandas as pd
from pythonping import ping
from datetime import datetime
from queue import Queue
from time import sleep
from threading import Thread

THREAD_WAIT_TIME = 20
THREADS = 3
OUTPUT_LIMIT = 5

output_filename = 'output.csv'
input_filename = 'device_data.json'
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
            status: int = int(response.success())  # Status Retrival
            print(f"Ping id: {task['id']}, Status: {status} ")
            output.put([task['id'], task['name'], datetime.now(), status])
        except OSError:
            print(f"Invalid Ip {task['ip']}")
            output.put([task['id'], task['name'], datetime.now(), 0])
        finally:
            jobq.task_done()


def write_output(output: Queue):
    """
    Write Output to the CSV file 5 at a time
    Args:
        output: Output Queue
    Returns:

    """
    while True:
        if output.qsize() > OUTPUT_LIMIT:
            print('writing output')
            task = [list(output.get()) for _ in range(OUTPUT_LIMIT)]
            pd.DataFrame(task).to_csv(output_filename, mode='a', header=False, index=False, )
            output.task_done()


def main():
    # Setting up the Parser for Arguments
    parser = argparse.ArgumentParser(prog="Bulk Network Device ip Status Checker", description="Script to get Status of Ip on a network")
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    global input_filename, output_filename
    input_filename, output_filename = args.input, args.output

    try:
        # Creating Thread for ping and output
        for _ in range(THREADS):
            th = Thread(target=ping_ips, args=[job_queue, output_queue], daemon=True)
            th.start()
        out = Thread(target=write_output, args=[output_queue], daemon=True)

        out.start()

        # loop to set up ping every 5 minutes
        while True:
            device_data = pd.read_json(input_filename)
            # adding elements to job queue
            for idx, row in device_data.iterrows():
                job_queue.put(row)
            print(job_queue.qsize())
            sleep(5*60)
    except FileNotFoundError:
        print(f"Input file {input_filename} not found")
        exit(0)
    except KeyboardInterrupt:
        print('The Process was terminated Forcefully')
        exit(0)


if __name__ == "__main__":
    main()
