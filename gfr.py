# -*- coding: utf-8 -*-

from time import sleep
from os import system
import subprocess
import re
import os
import sys
from settings import IniEnum
from settings import KeyEnum
from settings import DurationEnum
from threading import Timer
import platform
import utils


class RunGFR(object):
    def __init__(self):
        super(RunGFR, self).__init__()

        self.dd_path = ''
        self.xxd_path = ''
        self.adb_path = ''

        self.device_id = ''

        self.key_dict = None
        self.duration_dict = None

        init_path = utils.InitPath()
        self.root_path = init_path.pwd
        self.settings_ini_path = init_path.settings_ini_path

    def setup(self):
        if platform.system() == "Windows":
            self.dd_path = os.path.join(sys.path[0], 'dd.exe')
            self.xxd_path = os.path.join(sys.path[0], 'xxd.exe')
            self.adb_path = os.path.join(sys.path[0], 'adb.exe')
        else:
            self.dd_path = 'dd'
            self.xxd_path = 'xxd'
            self.adb_path = 'adb'

        self.get_device_id()
        self.get_setting_from_ini()
        # self.key_dict = utils.dict_value_to_int(self.get_ini_key_settings())
        # self.duration_dict = utils.dict_value_to_int(self.get_ini_duration_settings())

    def get_device_id(self):

        res = self.run_wait(self.adb_path + ' devices')
        res = res.replace('List of devices attached\n', '')
        res = res.replace('device', '')
        res = res.strip()
        self.device_id = res

        print("Device ID: " + self.device_id)

    def get_setting_from_ini(self):
        ini_handle = utils.IniControl(self.settings_ini_path)
        self.key_dict = utils.dict_value_to_int_float(ini_handle.read_section_config(IniEnum.KEY_SECTION))
        self.duration_dict = utils.dict_value_to_int_float(ini_handle.read_section_config(IniEnum.DURATION_SECTION))

    def start(self):
        print("start")
        self.setup()
        # print(self.key_dict)
        # print(self.duration_dict)
        self.run_fighting()

    def run_fighting(self):
        self.touch_pos_pressed(self.key_dict[KeyEnum.L1_x], self.key_dict[KeyEnum.L1_y])
        self.start_super_skill_timer()
        while True:
            # Triangle key
            self.touch_pos_long(self.key_dict[KeyEnum.Triangle_x],
                                self.key_dict[KeyEnum.Triangle_y],
                                self.duration_dict[DurationEnum.DURATION_TAP])

            sleep(self.duration_dict[DurationEnum.DURATION_KEY_INTERVAL])

            # Circle key
            self.touch_pos_long(self.key_dict[KeyEnum.Circle_x],
                                self.key_dict[KeyEnum.Circle_y],
                                self.duration_dict[DurationEnum.DURATION_TAP])

            sleep(self.duration_dict[DurationEnum.DURATION_KEY_INTERVAL])

            # L2 key
            self.touch_pos_long(self.key_dict[KeyEnum.L2_x],
                                self.key_dict[KeyEnum.L2_y],
                                self.duration_dict[DurationEnum.DURATION_TAP])

            sleep(self.duration_dict[DurationEnum.DURATION_KEY_INTERVAL])

    def start_super_skill_timer(self):
        timer_h = Timer(self.duration_dict[DurationEnum.DURATION_SUPER_SKILL], self.super_skill)
        timer_h.start()

    def super_skill(self):
        # L3 key
        self.touch_pos_long(self.key_dict[KeyEnum.L3_x],
                            self.key_dict[KeyEnum.L3_y],
                            self.duration_dict[DurationEnum.DURATION_KEY_THE_SAME],
                            wait=False)

        #R3 key
        self.touch_pos_long(self.key_dict[KeyEnum.R3_x],
                            self.key_dict[KeyEnum.R3_y],
                            self.duration_dict[DurationEnum.DURATION_KEY_THE_SAME],
                            wait=False)

        self.start_super_skill_timer()

    def touch_pos_pressed(self, x, y):
        print("Check L1 pressed")
        duration = int(self.duration_dict[DurationEnum.DURATION_PRESSED])
        duration = duration * 1000

        if not self.check_touch_pressed(duration):
            print("L1 is release, re-start long touch")
            self.touch_pos_long(x, y, duration, wait=False)

        timer_h = Timer(1, self.touch_pos_pressed, (x, y,))
        timer_h.start()

    def check_touch_pressed(self, set_duration):
        process_str = self.run_wait("adb -s "+self.device_id+" shell ps -u shell -f")
        pressed_running_str = re.search('.*cmd input swipe .* '+str(set_duration), process_str)
        if pressed_running_str:
            return True
            # print(m.group(0))
        else:
            return False

    def touch_pos_long(self, x, y, duration_ms, wait=True):
        cmd_str = "adb -s "+self.device_id+" shell \"input swipe "+str(x)+" "+str(y)+" "+str(x+1)+" "+str(y+1)+" "+str(duration_ms)+"\""
        if wait is True:
            system(cmd_str)
        else:
            subprocess.Popen(cmd_str, shell=True)

    @staticmethod
    def run_wait(command):
        r = os.popen(command)
        text = r.read()
        r.close()
        return text


if __name__ == '__main__':
    gfr_robot = RunGFR()
    gfr_robot.start()