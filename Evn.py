import os
import math
from Hotspot import Hotspot
class Evn(object):
    def __init__(self):
        self.actions = []
        self.state = []
        self.getAllActions()
        self.n_actions = len(self.actions)
        self.hotspots = []
        self.getAllHotSpots()


    def getAllActions(self):
        with open('C:/E/dataSet/2018-05-29/hotspot.txt', 'r') as file:
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
        # 当前时刻的hotspot的编号 和 当前时刻所属的时间段
        current_hotspot_num = int(self.state[current_index - 1])
        current_phase = math.ceil((time*60 + move_time) / 3600)

        # 获得选择的hotspot 和 当前时刻的hotspot
        selected_hotspot = self.getHotspotFromHotspotsListByNum(selected_hotspot_num)
        current_hotspot = self.getHotspotFromHotspotsListByNum(current_hotspot_num)
        distance = self.getDistanceBetweenHotspotsDistance(selected_hotspot, current_hotspot)
        # 移动到选择的hotspot 花费的时间 单位 秒
        moving_time = distance / 5
        # 将 移动时间累加到 state 的最后一位中
        self.state[-1] += moving_time


    def reset(self):
        for i in range(501):
            self.state.append(i)
        path = 'C:/E/dataSet/2018-05-29/hotspot/8点时间段访问hotspot/'
        files = os.listdir(path)
        for file in files:
            sensor = int(file.split('.')[0])
            self.state.append(sensor + 0.1)
            with open(path + file) as f:
                for line in f:
                    data = line.split(',')
                    hotspot = int(data[2])
                    if int(data[3]) == 0:
                        isbelong = 0
                    else:
                        isbelong = 1
                    self.state.append(sensor + hotspot/100 + isbelong/1000)
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