#!/usr/bin/env python3
"""Async and await example using subprocesses

Notes:
    Requires Python 3.6.
    SOURCE: https://fredrikaverpil.github.io/2017/06/20/async-and-await-with-subprocesses/
    removed windows specific code
"""

import asyncio

import time


async def run_command(*args):
    """Run command in subprocess

    Example from:
        http://asyncio.readthedocs.io/en/latest/subprocess.html
    """
    # Create subprocess
    process = await asyncio.create_subprocess_exec(
        *args,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE)

    # Status
    print('Started:', args, '(pid = ' + str(process.pid) + ')')

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Progress
    if process.returncode == 0:
        print('Done:', args, '(pid = ' + str(process.pid) + ')')
    else:
        print('Failed:', args, '(pid = ' + str(process.pid) + ')')

    # Result
    result = stdout.decode().strip()

    # Return stdout
    return result


async def run_command_shell(command):
    """Run command in subprocess (shell)
    """
    # Create subprocess
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE)

    # Status
    print('Started:', command, '(pid = ' + str(process.pid) + ')')

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Progress
    if process.returncode == 0:
        print('Done:', command, '(pid = ' + str(process.pid) + ')')
    else:
        print('Failed:', command, '(pid = ' + str(process.pid) + ')')

    # Result
    result = stdout.decode().strip()

    # Return stdout
    return result


def make_chunks(l, n):
    """Yield successive n-sized chunks from l.

    Note:
        Taken from https://stackoverflow.com/a/312464
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def run_asyncio_commands(tasks, max_concurrent_tasks=0):
    """Run tasks asynchronously using asyncio and return results

    If max_concurrent_tasks are set to 0, no limit is applied.
    """

    all_results = []

    if max_concurrent_tasks == 0:
        chunks = [tasks]
    else:
        chunks = make_chunks(l=tasks, n=max_concurrent_tasks)

    for tasks_in_chunk in chunks:
        loop = asyncio.get_event_loop()

        commands = asyncio.gather(*tasks_in_chunk)  # Unpack list using *
        results = loop.run_until_complete(commands)
        all_results += results
        loop.close()
    return all_results


def run_in_parallel(commands, max_concurrent_tasks=5):  # default to 5 parallel tasks

    start = time.time()

    tasks = [run_command(*command) for command in commands]

    results = run_asyncio_commands(tasks, max_concurrent_tasks)
    print('Results:', results)

    end = time.time()
    rounded_end = ('{0:.4f}'.format(round(end - start, 4)))
    print('Script ran in about', str(rounded_end), 'seconds')
