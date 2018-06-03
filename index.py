from datetime import datetime
import math
if __name__ == '__main__':
    # total_wait_time = 30
    # move_time = 40
    # moving_time = 12
    # selected_wait_time = 2
    #
    # total_time_seconds = total_wait_time * 10 * 60 + move_time + moving_time
    # hour = int(total_time_seconds / 3600)
    # minute = int((total_time_seconds - 3600 * hour) / 60)
    # second = total_time_seconds - hour * 3600 - minute * 60
    # present_time = str(hour + 8) + ':' + str(minute) + ':' + str(second)
    # present_time = datetime.strptime(present_time, '%H:%M:%S')

    # MC 在 被选中的 hotspot 待 selected_wait_time*self.t 的时间后 的时间
    # charging_end_time_seconds = total_time_seconds + selected_wait_time * 10 * 60
    # hour = int(charging_end_time_seconds / 3600)
    # minute = int((charging_end_time_seconds - 3600 * hour) / 60)
    # second = charging_end_time_seconds - hour * 3600 - minute * 60
    # charging_end_time = str(hour + 8) + ':' + str(minute) + ':' + str(second)
    # charging_end_time = datetime.strptime(charging_end_time, '%H:%M:%S')
    # print(present_time)
    # print(charging_end_time)
    #
    # print((charging_end_time - present_time).seconds)

    # present = datetime.strptime('9:00:00', '%H:%M:%S')
    # charging_end_time = datetime.strptime('9:00:0', '%H:%M:%S')
    # if charging_end_time > present:
    #     print('a')
    sensors_mobile_charger = {}
    sensors_mobile_charger['000'] = [0.7, 0.6]
    sensors_mobile_charger['001'] = [0.3, 0.8]
    sensors_mobile_charger['003'] = [0.9, 1]
    # sensors_mobile_charger['004'] = [0.5, 0.5]
    # sensors_mobile_charger['015'] = [0.4, 0.6]
    # sensors_mobile_charger['030'] = [1, 0.9]
    # sensors_mobile_charger['042'] = [0.2, 0.8]
    # sensors_mobile_charger['065'] = [1, 1]
    # sensors_mobile_charger['081'] = [0.9, 0.7]
    # sensors_mobile_charger['082'] = [0.8, 0.5]
    #
    # sensors_mobile_charger['085'] = [0.3, 0.7]
    # sensors_mobile_charger['096'] = [0.4, 1]
    # sensors_mobile_charger['125'] = [0.6, 0.6]
    # sensors_mobile_charger['126'] = [0.3, 0.5]
    # sensors_mobile_charger['165'] = [0.5, 0.8]
    # sensors_mobile_charger['179'] = [0.8, 0.9]
    # sensors_mobile_charger['MC'] = [2000, 50]
    #
    # for key in sensors_mobile_charger:
    #     if key == '003':
    #         sensor = sensors_mobile_charger[key]
    #         sensor[0] = 100
    #
    # for key, value in sensors_mobile_charger.items():
    #     print(key, value)
    a = [0,1]
    print(a[-1])
