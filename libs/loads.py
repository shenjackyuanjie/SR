"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import json


def config(file_name, stack=None):
    rd = {}  # rd -> return
    try:
        with open(file_name, "r") as jf:  # jf -> json file
            rd = json.load(jf)
    except FileNotFoundError:
        raise FileNotFoundError("no config file")
    if stack != None:
        rd = rd[stack]
    return rd
