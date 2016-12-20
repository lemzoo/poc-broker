#!/usr/bin/env python
import time


def display_digit(number):
    for i in range(0, number):
        display = '.'
        print(display, sep='', end='', flush=True)
        time.sleep(1)
