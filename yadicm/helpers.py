"""Various helper functions."""


import datetime


def get_logfile_name() -> str:
    return "yadicm_" + datetime.datetime.now().strftime("%Y_%m") + ".log"
