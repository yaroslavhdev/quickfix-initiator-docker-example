#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
def setup_logger(logger_name, level=logging.INFO):
    lz = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    lz.setLevel(level)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    lz.addHandler(streamHandler)
