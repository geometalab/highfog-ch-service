import time
from concurrent import futures

import subprocess


def run_shell(*args):
    subprocess.run(*args)


def run_in_parallel(commands, max_concurrent_tasks=9):  # default to 9 parallel tasks

    start = time.time()

    ex = futures.ThreadPoolExecutor(max_workers=max_concurrent_tasks)
    print('main: starting')

    wait_for = [
        ex.submit(run_shell, command)
        for command in commands
    ]

    for f in futures.as_completed(wait_for):
        print('main: result: {}'.format(f.result()))

    end = time.time()
    rounded_end = ('{0:.4f}'.format(round(end - start, 4)))
    print('Script ran in about', str(rounded_end), 'seconds')
