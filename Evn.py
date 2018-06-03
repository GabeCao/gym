import os
import math
from Hotspot import Hotspot
from datetime import datetime
class Evn(object):
    def __init__(self):
        # 所有的action
        self.actions = []
        self.state = []
        # 给self.actions 赋值
        self.getAllActions()
        # actions 的大小
        self.n_actions = len(self.actions)
        # 所有的hotspot 放在这个list里
        self.hotspots = []
        # 给 self.hotspots 赋值
        self.getAllHotSpots()
        # 所有的sensor 和 mobile charger = 的初始能量信息 {sensor : [初始能量, 消耗速率]}
        self.sensors_mobile_charger = {}
        self.set_sensors_mobile_charger()


    def getAllActions(self):
        # 读取hotspot 文件中的信息，放入到self.actions 中
        with open('hotspot.txt', 'r') as file:
            for line in file:
                array = line.strip().split(',')
                a = array[2]
                for i in range(1, 7):
                    b = a + '_' + str(i)
                    self.actions.append(b)

    def step(self, action):
        action_arr = action.split('_')
        # charger 移动花费的时间
        move_time = self.state[-1]
        # action 中 选择的hotspot的编号和等待时间
        selected_hotspot_num = int(action_arr[0])
        selected_wait_time = int(action_arr[1])

        current_index = 0
        time = 0
        for i in range(1, 500):
            time += self.state[i] * 10 % 10
            if self.state[i] == 0:
                current_index = i
                break
        # 将action 添加到最后一个
        self.state[current_index] = selected_hotspot_num + selected_wait_time / 10
        # 当前时刻的hotspot的编号 和 当前时刻所属的时间段
        current_hotspot_num = int(self.state[current_index - 1])
        # 从08：00 到现在的总时间 total_time
        total_time = (time*60 + move_time)
        current_phase = math.ceil(total_time / 3600)

        # 获得选择的hotspot 和 当前时刻的hotspot
        selected_hotspot = self.getHotspotFromHotspotsListByNum(selected_hotspot_num)
        current_hotspot = self.getHotspotFromHotspotsListByNum(current_hotspot_num)
        distance = self.getDistanceBetweenHotspotsDistance(selected_hotspot, current_hotspot)
        # 移动到选择的hotspot 花费的时间 单位 秒
        moving_time = distance / 5
        # 将 移动时间累加到 state 的最后一位中
        self.state[-1] += moving_time

        # 选择的hotspot 在MC停留的时间里 到达的 sensor
        stay_time_seconds = selected_wait_time * 60
        arravied_sensor = []
        path = 'C:/E/dataSet/2018-05-29/sensor数据/'
        files = os.listdir(path)
        for file in files:
            sensor_num = file.split('.')[0]
            with open(path + file) as f:
                for line in f:
                    data = line.strip().split(',')



        selected_hotspot_sensor_times = {}
        path = 'hotspot/' + str(current_phase) + '时间段/' + str(selected_hotspot_num) + '.txt'
        with open(path) as file:
            for line in file:
                data = line.strip().split(',')
                if int(data[1]) != 0:
                    selected_hotspot_sensor_times[data[0]] = int(data[1])

        for key, value in selected_hotspot_sensor_times.items():
            for i in range(501, len(self.state)):
                if int(key) == int(self.state[i]):


    def reset(self):
        for i in range(501):
            self.state.append(0)
        path = 'C:/E/dataSet/2018-05-29/hotspot/8点时间段访问hotspot/'
        files = os.listdir(path)
        for file in files:
            sensor = int(file.split('.')[0])
            self.state.append(sensor + 0.1)
            with open(path + file) as f:
                for line in f:
                    data = line.strip().split(',')
                    hotspot = int(data[2])
                    if int(data[3]) == 0:
                        isbelong = 0
                    else:
                        isbelong = 1
                    self.state.append(round(sensor + hotspot/100 + isbelong/1000, 3))
        self.state.append(0)
        return self.state

    def getAllHotSpots(self):
        path = 'hotspot.txt'
        with open(path) as file:
            for line in file:
                data = line.strip().split(',')
                hotspot = Hotspot(float(data[0]), float(data[1]), int(data[2]))
                self.hotspots.append(hotspot)

    def getHotspotFromHotspotsListByNum(self, num):
        for hotspot in self.hotspots:
            if hotspot.get_num() == num:
                return hotspot

    def getDistanceBetweenHotspotsDistance(self, p1, p2):
        x = p1.get_x() - p2.get_x()
        y = p1.get_y() - p2.get_y()
        return math.sqrt((x ** 2) + (y ** 2))

    def set_sensors_mobile_charger(self):
        self.sensors_mobile_charger['000'] = [0.7, 0.6]
        self.sensors_mobile_charger['001'] = [0.3, 0.8]
        self.sensors_mobile_charger['003'] = [0.9, 1]
        self.sensors_mobile_charger['004'] = [0.5, 0.5]
        self.sensors_mobile_charger['015'] = [0.4, 0.6]
        self.sensors_mobile_charger['030'] = [1, 0.9]
        self.sensors_mobile_charger['042'] = [0.2, 0.8]
        self.sensors_mobile_charger['065'] = [1, 1]
        self.sensors_mobile_charger['081'] = [0.9, 0.7]
        self.sensors_mobile_charger['082'] = [0.8, 0.5]
        self.sensors_mobile_charger['085'] = [0.3, 0.7]
        self.sensors_mobile_charger['096'] = [0.4, 1]
        self.sensors_mobile_charger['125'] = [0.6, 0.6]
        self.sensors_mobile_charger['126'] = [0.3, 0.5]
        self.sensors_mobile_charger['165'] = [0.5, 0.8]
        self.sensors_mobile_charger['179'] = [0.8, 0.9]
        self.sensors_mobile_charger['MC'] = [2000, 50]



