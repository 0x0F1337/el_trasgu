import subprocess, threading
import msvcrt as ms
from datetime import datetime

FILENAME = 'trasgu.log'

stored_processes = {}


def new_process_log(process_name: str):
    """
    Writes a log stating that a process has started
    :param process_name: Name of the process
    """
    process_time = stored_processes[process_name]
    msg = 'New process started "{0}" at {1}\n'.format(process_name, process_time.strftime('%d/%m/%Y %H:%M'))
    
    with open(FILENAME, 'a') as log:
        log.write(msg)


def close_process_log(process_name: str):
    """
    Writes a log stating that a process has ended
    :param process_name: Name of the process
    """
    process_time = stored_processes[process_name]
    now = datetime.now()
    exec_time = now - process_time
    exec_time_mins = round(exec_time.total_seconds() / 60, 2)

    msg = 'Process "{0}" was stopped at {1}. Total execution time: {2} mins\n'.format(process_name, now.strftime('%d/%m/%Y %H:%M'), exec_time_mins)

    with open(FILENAME, 'a') as log:
        log.write(msg)


def get_processes():
    """
    Gets all running processes
    """
    global stored_processes

    while True:
        # We use wmic to get all running processes
        cmd_result = subprocess.run(['wmic', 'process', 'get', 'description'], stdout=subprocess.PIPE)
        splitted_out = str(cmd_result.stdout).split('\\r\\r\\n')

        running_processes = [proc.replace(' ', '') for proc in splitted_out] 
        
        # Loops over every gotten process
        for process in running_processes:

            # If a new process was found, log it
            if process not in stored_processes:
                stored_processes[process] = datetime.now()
                new_process_log(process)

        # Loops over every stored process
        # If there is any process that is not running anymore, log it
        for process in stored_processes.copy().keys():
            if process not in running_processes:
                close_process_log(process)
                stored_processes.pop(process)


# Main entry point
if __name__ == '__main__':
    # Starts getting processes on a new thread
    new_thread = threading.Thread(target=get_processes)
    new_thread.daemon = True
    new_thread.start()

    ms.getch()
