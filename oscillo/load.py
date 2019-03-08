#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import os
import subprocess
import sys
import threading
import time

import psutil
import yaml
import argparse

import numpy as np
import matplotlib

if not os.environ.get('DISPLAY'):
    print('DISPLAY not found. Using non-interactive Agg backend')
    matplotlib.use('Agg')

import matplotlib.pyplot as plt



"""
# demo

commands:
  -
    name: gzip
    cmd: gzip /path/to/big/file
  
  -
    name: tar
    cmd: tar -zcf tmp.tar.gz /path/to/file

output: gzip-and-tar-gz
"""


class Stopwatch(object):

    def __init__(self, pid):
        self.__is_run = False
        self.__start_time = 0
        self.__elapsed_times = 0
        self.memory_percent = []
        self.cpu_percent = []
        self.pid = pid

    def start(self):
        if self.__is_run:
            return False
        self.__is_run = True
        self.__start_time = time.time()

        if self.pid > 0:
            p = psutil.Process(self.pid)
        else:
            p = psutil
            p.memory_percent = lambda: p.virtual_memory().percent
        while self.__is_run:
            try:
                self.cpu_percent.append(p.cpu_percent(1))
                self.memory_percent.append(p.memory_percent())
            except psutil.NoSuchProcess:
                break

    @property
    def elapsed(self):

        if self.__is_run:
            return self.__elapsed_times + time.time() - self.__start_time
        return self.__elapsed_times

    def stop(self):
        self.__elapsed_times = self.elapsed
        self.__is_run = False

    @property
    def cpu(self):
        return self.cpu_percent

    @property
    def memory(self):
        return self.memory_percent


def run_commands(config, global_resource):

    commands = config['commands']

    summary = {}

    for command in commands:
        name = command.get("name")
        cmd = command.get("cmd")

        p = subprocess.Popen(cmd, stderr=sys.stderr,
                             stdin=sys.stdin, stdout=sys.stdout, shell=True)
        if global_resource:
            stopwatch = Stopwatch(-1)
        else:
            stopwatch = Stopwatch(p.pid)

        thread = threading.Thread(target=stopwatch.start)
        thread.setDaemon(True)
        thread.start()
        p.communicate()
        stopwatch.stop()

        result = {"cpu": stopwatch.cpu, "memory": stopwatch.memory,
                  "elapsed": stopwatch.elapsed}
        summary[name] = result
    return summary


def print_image(summary, output="metrix.png"):

    plt.figure(figsize=(16, 4))

    plt.subplot(121)
    for k in summary:
        result = summary[k]
        x = np.linspace(0, 1, len(result['cpu']))
        y = np.array(result['cpu'])

        plt.plot(x, y, label=k, linewidth=2)

    plt.xlabel("Time(30s)")
    plt.ylabel("CPU percent")
    plt.legend(labels=[k for k in summary], loc="best")
    plt.title("CPU")

    plt.subplot(122)
    for k in summary:
        result = summary[k]
        x = np.linspace(0, 1, len(result['memory']))
        y = np.array(result['memory'])

        plt.plot(x, y, label=k, linewidth=2)
    plt.xlabel("Time(30s)")
    plt.ylabel("Memory percent")
    plt.legend(labels=[k for k in summary], loc="best")
    plt.title("Memory")

    if not output.endswith('.png'):
        output += '.png'
    plt.savefig(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-g', '--globals',
        action='store_true',
        default=False,
        help='Watch global load (cpu, memory). Default is `False`'
    )
    parser.add_argument(
        '-c', '--config',
        help='config file: which specified the command list and the name of metrix text file'
    )

    parser.add_argument(
        '-l', '--load',
        help='reload metrics file and print to image'
    )

    args = parser.parse_args()

    desc = ('Record the system load at the execution of the command line and display it graphically')

    _conf_file = args.config
    _load_log_file = args.load

    if not _conf_file and not _load_log_file:
        print(desc)
        parser.print_help()
        sys.exit(1)

    if _load_log_file:
        with open(_load_log_file, "r") as f:
            _summary = json.load(f)
        _output = _load_log_file

    else:
        with open(_conf_file, "r") as f:
            _config = yaml.load(f)

        _output = _config.get("output", 'metrix')
        _summary = run_commands(_config, args.globals)
        with open(_output + ".log", "w") as f:
            json.dump(_summary, f)
    print_image(_summary, _output)


if __name__ == '__main__':
    main()
