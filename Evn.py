import os
import math
from Hotspot import Hotspot
from Point import Point
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
        # 时间片，一个小时分为6个t
        self.t = 10


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
        # charger 移动花费的时间 单位(秒)
        move_time = self.state[-1]
        # action 中 选择的hotspot的编号和等待时间
        selected_hotspot_num = int(action_arr[0])
        selected_wait_time = int(action_arr[1])

        current_index = 0
        # MC 在hotspot 总共等待的时间 单位(self.t)
        total_wait_time = 0
        for i in range(1, 500):
            total_wait_time += self.state[i] * 10 % 10
            if self.state[i] == 0:
                current_index = i
                break
        # 将action 添加到CS中的最后一个
        self.state[current_index] = selected_hotspot_num + selected_wait_time / 10

        # 当前时刻的hotspot的编号
        current_hotspot_num = int(self.state[current_index - 1])
        # 选择了的hotspot 和 当前时刻的hotspot，两个hotspot 间的距离
        selected_hotspot = self.getHotspotFromHotspotsListByNum(selected_hotspot_num)
        current_hotspot = self.getHotspotFromHotspotsListByNum(current_hotspot_num)
        distance = self.getDistanceBetweenHotspots(selected_hotspot, current_hotspot)
        # 移动到选择的hotspot 花费的时间 单位 秒
        moving_time = distance / 5
        # 将 移动时间累加到 state 的最后一位中
        self.state[-1] += moving_time
        # MC 从当前 的 hotspot，移动到 被选中的hotspot 的时间
        total_time_seconds = total_wait_time * self.t * 60 + move_time + moving_time
        hour = int(total_time_seconds / 3600)
        minute = int((total_time_seconds - 3600 * hour) / 60)
        second = total_time_seconds - hour * 3600 - minute * 60
        present_time = str(hour + 8) + ':' + str(minute) + ':' + str(second)
        present_time = datetime.strptime(present_time, '%H:%M:%S')

        # MC 在 被选中的 hotspot 待 selected_wait_time*self.t 的时间后 的时间
        charging_end_time_seconds = total_time_seconds + selected_wait_time * self.t * 60
        hour = int(charging_end_time_seconds / 3600)
        minute = int((charging_end_time_seconds - 3600 * hour) / 60)
        second = charging_end_time_seconds - hour * 3600 - minute * 60
        charging_end_time = str(hour + 8) + ':' + str(minute) + ':' + str(second)
        charging_end_time = datetime.strptime(charging_end_time, '%H:%M:%S')

        # 选择的hotspot 在MC停留的时间里 到达的 sensor
        arrived_sensor = []
        path = 'C:/E/dataSet/2018-05-29/sensor数据/'
        files = os.listdir(path)
        for file in files:
            # 当前 sensor 的 编号
            sensor_num = file.split('.')[0]
            with open(path + file) as f:
                for line in f:
                    data = line.strip().split(',')
                    x = float(data[0])
                    y = float(data[1])
                    sensor_time = datetime.strptime(data[2], '%H:%M:%S')
                    point = Point(x, y, sensor_time)
                    distance_point_hotspot = self.getDistanceBetweenHotspotAndPoint(selected_hotspot, point)
                    if distance_point_hotspot < 60 and present_time <= point.get_time() <= charging_end_time:
                        arrived_sensor.append(sensor_num)
        # 设置返回的奖励值 初始为0
        reword = 0
        for sensor_num in arrived_sensor:
            for key in self.sensors_mobile_charger:
                if key == sensor_num:
                    # 取出sensor
                    sensor = self.sensors_mobile_charger[sensor_num]
                    # 得到上一次的充电时间
                    previous_charging_time = datetime.strptime(sensor[2], '%H:%M:%S')
                    # 当前sensor 电量消耗的速率
                    sensor_consumption_ratio = sensor[1]
                    # 当前sensor 的剩余电量
                    sensor_reserved_energy = sensor[0] - (present_time - previous_charging_time).seconds * sensor[1]
                    # 当前sensor 的剩余寿命
                    rl = sensor_reserved_energy / sensor_consumption_ratio
                    # 如果剩余寿命大于两个小时
                    if rl >= 2 * 3600:
                        reword += 0
                    # 如果剩余寿命在0 到 两个小时
                    elif 0 < rl < 2 * 3600:
                        # mc 充电后的剩余能量
                        self.sensors_mobile_charger['MC'][0] = self.sensors_mobile_charger['MC'][0] \
                                                               - (10.8 * 1000 - sensor_reserved_energy)
                        # 设置sensor 充电后的剩余能量 是满能量
                        sensor[1] = 10.8 * 1000
                        # 改变state 的状态
                        for i in range(501, len(self.state)):
                            if int(sensor_num) == int(self.state[i]):
                                self.state[i] = int(self.state[i])
                        reword += math.exp(-rl)
                    else:
                        reword += -0.5
        # mc 给到达的sensor 充电后，如果能量为负，则回合结束，反之没有结束
        if self.sensors_mobile_charger['MC'][0] <= 0:
            done = True
        else:
            done = False

        return self.state, reword, done

    def reset(self):
        for i in range(501):
            self.state.append(0)
        path = 'C:/E/dataSet/2018-05-29/hotspot/8时间段访问hotspot/'
        files = os.listdir(path)
        for file in files:
            sensor = int(file.split('.')[0])
            self.state.append(float(sensor))
            with open(path + file) as f:
                for line in f:
                    data = line.strip().split(',')
                    hotspot = int(data[2])
                    if int(data[3]) == 0:
                        isbelong = 0
                    else:
                        isbelong = 1
                    self.state.append(round(sensor + hotspot/100 + isbelong/1000, 3))
        # 添加 mc 移动时间到最后一位
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

    def getDistanceBetweenHotspots(self, p1, p2):
        x = p1.get_x() - p2.get_x()
        y = p1.get_y() - p2.get_y()
        return math.sqrt((x ** 2) + (y ** 2))

    def getDistanceBetweenHotspotAndPoint(self, p1, p2):
        x = p1.get_x() - p2.get_x()
        y = p1.get_y() - p2.get_y()
        return math.sqrt((x ** 2) + (y ** 2))

    def set_sensors_mobile_charger(self):
        self.sensors_mobile_charger['000'] = [0.7 * 10.8 * 1000, 0.6, '08:00:00']
        self.sensors_mobile_charger['001'] = [0.3 * 10.8 * 1000, 0.8, '08:00:00']
        self.sensors_mobile_charger['003'] = [0.9 * 10.8 * 1000, 1, '08:00:00']
        self.sensors_mobile_charger['004'] = [0.5 * 10.8 * 1000, 0.5, '08:00:00']
        self.sensors_mobile_charger['015'] = [0.4 * 10.8 * 1000, 0.6, '08:00:00']
        self.sensors_mobile_charger['030'] = [1 * 10.8 * 1000, 0.9, '08:00:00']
        self.sensors_mobile_charger['042'] = [0.2 * 10.8 * 1000, 0.8, '08:00:00']
        self.sensors_mobile_charger['065'] = [1 * 10.8 * 1000, 1, '08:00:00']
        self.sensors_mobile_charger['081'] = [0.9 * 10.8 * 1000, 0.7, '08:00:00']
        self.sensors_mobile_charger['082'] = [0.8 * 10.8 * 1000, 0.5, '08:00:00']
        self.sensors_mobile_charger['085'] = [0.3 * 10.8 * 1000, 0.7, '08:00:00']
        self.sensors_mobile_charger['096'] = [0.4 * 10.8 * 1000, 1, '08:00:00']
        self.sensors_mobile_charger['125'] = [0.6 * 10.8 * 1000, 0.6, '08:00:00']
        self.sensors_mobile_charger['126'] = [0.3 * 10.8 * 1000, 0.5, '08:00:00']
        self.sensors_mobile_charger['165'] = [0.5 * 10.8 * 1000, 0.8, '08:00:00']
        self.sensors_mobile_charger['179'] = [0.8 * 10.8 * 1000, 0.9, '08:00:00']
        self.sensors_mobile_charger['MC'] = [2000 * 1000, 50]

    def test(self):
        return 1,3

if __name__ == '__main__':
    evn = Evn()
    evn.reset()
    state_, reword, done = evn.step('2_3')
    print(state_)
    print(reword)
    print(done)

