#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import subprocess
import sys
import threading
import time

import matplotlib
import numpy as np
import psutil

if not os.environ.get('DISPLAY'):
    print('DISPLAY not found. Using non-interactive Agg backend')
    matplotlib.use('Agg')

import matplotlib.pyplot as plt


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
        x = np.linspace(0, int(result['elapsed']), len(result['cpu']))
        y = np.array(result['cpu'])

        plt.plot(x, y, label=k, linewidth=2)

    plt.xlabel("Time(s)")
    plt.ylabel("CPU (%)")
    plt.legend(labels=[k for k in summary], loc="best")
    plt.title("CPU load tracing")

    plt.subplot(122)
    for k in summary:
        result = summary[k]
        x = np.linspace(0, int(result['elapsed']), len(result['memory']))
        y = np.array(result['memory'])

        plt.plot(x, y, label=k, linewidth=2)
    plt.xlabel("Time(s)")
    plt.ylabel("Memory (%)")
    plt.legend(labels=[k for k in summary], loc="best")
    plt.title("Memory load tracing")

    if not output.endswith('.png'):
        output += '.png'
    plt.savefig(output)
