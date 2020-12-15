import unittest


def add(arg1, arg2):
    return arg1 + arg2


def subtract(arg1, arg2):
    return arg1 - arg2


def multiply(arg1, arg2):
    return arg1 * arg2


def divide(arg1, arg2):
    if arg2 == 0:
        raise ValueError("Can't divide by 0")
    return arg1 / arg2

