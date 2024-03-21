import enum

VERSION = "v0.0.1"
DEBUG = False

SETTINGS_INI_FILENAME = "settings.ini"


class IniEnum(enum.StrEnum):
    GENERAL_SECTION = 'General'
    KEY_SECTION = 'Key'
    DURATION_SECTION = 'Duration'

class DurationEnum(enum.StrEnum):
    DURATION_PRESSED = 'duration_pressed'
    DURATION_TAP = 'duration_tap'
    DURATION_KEY_INTERVAL = 'duration_key_interval'
    DURATION_SUPER_SKILL = 'duration_super_skill'
    DURATION_KEY_THE_SAME = 'duration_key_the_same'

class KeyEnum(enum.StrEnum):
    L1_x = 'l1_x'
    L1_y = 'l1_y'
    L2_x = 'l2_x'
    L2_y = 'l2_y'
    L3_x = 'l3_x'
    L3_y = 'l3_y'
    R1_x = 'r1_x'
    R1_y = 'r1_y'
    R2_x = 'r2_x'
    R2_y = 'r2_y'
    R3_x = 'r3_x'
    R3_y = 'r3_y'
    Circle_x = 'circle_x'
    Circle_y = 'circle_y'
    Cross_x = 'cross_x'
    Cross_y = 'cross_y'
    Triangle_x = 'triangle_x'
    Triangle_y = 'triangle_y'
    Square_x = 'square_x'
    Square_y = 'square_y'
