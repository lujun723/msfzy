# -*- coding: utf-8 -*-

import serial
import time
import json
import ast
from filectrl import text_save, text_read

process_flag = 0
s = None
config = None
CARD_NO = None
alpha_db = []
r_db = []
MAN_NO = None
STATION_NO = None
KEY_PRESSED = None
ALARM_ON = None
POWER_LEVEL = None

def load_config():
    with open('config.json') as json_file:
        data = json.load(json_file)  # 变成python对象了：str，list，dict等
        return data


def setup():
    global s
    global config
    global alpha_db,r_db
    # open serial COM port to /dev/ttyS0, which maps to UART0(D0/D1)
    #  the baudrate is set to 57600 and should be the same as the one
    #  specified in the Arduino sketch uploaded to ATmega32U4.
    s = serial.Serial("/dev/ttyS0", 57600)
    alpha_db = text_read('man_alpha_db.txt')
    r_db = text_read('man_r_db.txt')
    # 拿配置
    # config = load_config()


def backup(alpha_date_temp,r_date_temp):
    man_alpha_read = text_read('man_alpha_db.txt')
    man_r_read = text_read('man_r_db.txt')
    man_alpha_read = map(int, man_alpha_read)
    man_r_read = map(int, man_r_read)

    alpha_date_temp = map(int, alpha_date_temp)
    r_date_temp = map(int, r_date_temp)
    # 找不同的元素
    # s1 = set(man_alpha_read)
    # s2 = set(alpha_date_temp)
    # print s1.symmetric_difference(s2)
    # print list(s1.symmetric_difference(s2))

    if alpha_date_temp != man_alpha_read:
        print "alpha different"
        # 写入数据库
        text_save(alpha_db, 'man_alpha_db.txt', 'w')
    if r_date_temp != man_r_read:
        print "r different"
        text_save(r_db, 'man_r_db.txt', 'w')


def loop():
    data = ''
    read_buf = ['']
    # while s.inWaiting() > 0:
    while read_buf[-1] != '}':
        read_buf.append(s.read(1))
    data = ''.join(read_buf)
    data_process(data)
    alarm_set(ALARM_ON, POWER_LEVEL)


def alarm_set(g_alarm_flag, g_power_level):
    led_cmd = {'pkg_name':'led_cmd', 'warning':g_alarm_flag}
    led_cmd_json = json.dumps(led_cmd)

    if g_alarm_flag == 1:
        g_alarm_flag = 2 # 为了只发一次
        print led_cmd_json
    elif g_alarm_flag == 0:
        g_alarm_flag = 2
        print led_cmd_json


def data_process(data_buf):
    global CARD_NO, MAN_NO, STATION_NO, KEY_PRESSED, ALARM_ON, POWER_LEVEL
    print (data_buf)
    # print (data_buf)
    data_buf = ast.literal_eval(json.dumps(data_buf))
    # print "Now length is ", len(data_buf)

    try:
        dict_object = json.loads(data_buf)

        if dict_object["pkg_name"] == "man_card":  # 上位机下发的配置
            CARD_NO = int(dict_object["card_no"])
            alpha_db[CARD_NO] = int(dict_object["a_val"])
            r_db[CARD_NO] = int(dict_object["r_val"])
            print "CARD_NO is" ,CARD_NO
            print "alpha_db[CARD_NO] is", alpha_db[CARD_NO]
            print "r_db[CARD_NO]", r_db[CARD_NO]
            backup(alpha_db, r_db) # 这句放这里很慢
        elif dict_object["pkg_name"] == "uhf_card": # UHF读卡信息, 下位机重复读取卡号，只能发一次
            STATION_NO = int(dict_object["uhf_no"])
            MAN_NO = int(dict_object["card_no"])
            # for test start
            print "Now Alpha val is ", alpha_db[MAN_NO]
            print "Now R val is ", r_db[MAN_NO]
            # for test end
            # print type(alpha_db[MAN_NO])
            # print alpha_db[MAN_NO]
            if int(alpha_db[MAN_NO]) > 0 or int(r_db[MAN_NO]) > 0:
                ALARM_ON = 1
                print json.dumps({"pkg_name":"buzz_cmd","cmd":1})
            else:
                ALARM_ON = 0
                print json.dumps({"pkg_name":"buzz_cmd","cmd":0})
        elif dict_object["pkg_name"] == "key_scan": # 按键读取，暂时不考虑具体逻辑
            KEY_PRESSED = dict_object["key_down"]
            # for test start
            print "Now pressed key is ", KEY_PRESSED
            # for test end
        elif dict_object["pkg_name"] == "battery": # 电池电量
            POWER_LEVEL = int(dict_object["power_level"])
            #for test start
            print "Power level is ", POWER_LEVEL
            #for test end



    except Exception, e:
        print Exception, ":", e
        print "ERROR data_buf is ", data_buf

    """
    print dict_object["SubBoard_ID"]
    print dict_object["data_len"]
    print dict_object["data"]
    """


if __name__ == '__main__':
    setup()
    while True:
        loop()