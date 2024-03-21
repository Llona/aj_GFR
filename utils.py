import settings
from os import path
import sys
import configparser
from collections import OrderedDict


def dict_value_to_int_float(dicts):
    temp_dict = dict()
    for k, v in dicts.items():
        try:
            temp_dict[k] = int(v)
        except Exception as e:
            # print(e)
            str(e)
            temp_dict[k] = float(v)

    return temp_dict


class IniControl(configparser.ConfigParser):
    def __init__(self, ini_full_path):
        super(IniControl, self).__init__()
        self.ini_full_path = ini_full_path
        self.ini_format = 'utf8'
        self.format_list = ['utf8', 'utf-8-sig', 'utf16', None, 'big5', 'gbk', 'gb2312']
        self.try_ini_format()

    def try_ini_format(self):
        for file_format in self.format_list:
            try:
                config_lh = configparser.ConfigParser()
                with open(self.ini_full_path, 'r', encoding=file_format) as file:
                    config_lh.read_file(file)
                self.ini_format = file_format
                return
            except Exception as e:
                print('checking {} format: {}'.format(self.ini_full_path, file_format))
                str(e)

    def read_config(self, section, key):
        try:
            config_lh = configparser.ConfigParser()
            file_ini_lh = open(self.ini_full_path, 'r', encoding=self.ini_format)
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()
            return config_lh.get(section, key)
        except Exception as e:
            print("Error! 讀取ini設定檔發生錯誤! " + self.ini_full_path)
            str(e)
            raise

    def read_section_config(self, section):
        try:
            config_lh = configparser.ConfigParser()
            file_ini_lh = open(self.ini_full_path, 'r', encoding=self.ini_format)
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()
            single_section = config_lh.items(section)

            section_dict = OrderedDict()
            for item in single_section:
                section_dict[item[0]] = item[1]
            return section_dict
        except Exception as e:
            print("Error! 讀取ini設定檔發生錯誤! " + self.ini_full_path)
            str(e)
            raise

    def write_config(self, sections, ini_dict):
        try:
            config_lh = configparser.ConfigParser()
            config_lh.optionxform = str
            file_ini_lh = open(self.ini_full_path, 'r', encoding=self.ini_format)
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()

            for key, value in ini_dict.items():
                config_lh.set(sections, key, value)
            file_ini_lh = open(self.ini_full_path, 'w', encoding=self.ini_format)
            config_lh.write(file_ini_lh)
            file_ini_lh.close()
        except Exception as e:
            print("Error! 寫入ini設定檔發生錯誤! " + self.ini_full_path)
            str(e)
            raise


def singleton(cls):
    instance = None

    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


@singleton
class InitPath(object):
    def __init__(self):
        self.pwd = None
        self.settings_ini_path = None
        self.find_root_path()
        # print("init path")

    def find_root_path(self):
        # print("find root path")
        settings_ini_path = ''
        root_path = sys.path[0]
        root_path_find = False

        for retry_count in range(1, 3):
            settings_ini_path = path.join(root_path, settings.SETTINGS_INI_FILENAME)
            if path.exists(settings_ini_path):
                root_path_find = True
                break
            else:
                root_path = path.join(root_path, '..')

        if not root_path_find:
            print("Error! can't find settings.ini")
            raise

        root_path = path.realpath(root_path)
        self.pwd = root_path
        self.settings_ini_path = settings_ini_path
        return root_path
