#!/usr/bin/env python
# _*_ coding:utf-8 _*_


class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')
