import os
import math
from Hotspot import Hotspot
from Point import Point
from datetime import datetime
from BaseStation import BaseStation
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
        # mc 移动所花费的时间
        self.move_time = 0


    def getAllActions(self):
        # 暂时没写
        pass
        # 读取hotspot 文件中的信息，放入到self.actions 中
        # with open('hotspot.txt', 'r') as file:
        #     for line in file:
        #         array = line.strip().split(',')
        #         a = array[2]
        #         for i in range(1, 7):
        #             b = a + '_' + str(i)
        #             self.actions.append(b)

    def step(self, action):
        # action 的形状 '2_3'，代表在第二个hotspot 待 3个t的时间
        action_arr = action.split('_')
        # charger 移动花费的时间 单位(秒)
        move_time = self.move_time
        # action 中 选择的hotspot的编号和等待时间
        selected_hotspot_num = int(action_arr[0])
        selected_wait_time = int(action_arr[1])
        # current_index 用来指向CS中的最后一个 action 的后一位，将新来的action 添加到 这个位置
        current_index = 0
        # MC 在hotspot 总共等待的时间 单位(self.t)
        total_wait_time = 0
        for i in range(1, 500):
            # CS 的形状如 ‘2.4’表示在第二个hotspot 等待了4个t，得到第一个小数位的值，加一起放入 total_wait_time  (action 原因 需要修改)
            total_wait_time += self.state[i] * 10 % 10
            if self.state[i] == 0:
                current_index = i
                break
        # 将action 添加到CS中的最后一个   (action 原因 需要修改)
        self.state[current_index] = selected_hotspot_num + selected_wait_time / 10

        # 当前时刻的hotspot的编号
        current_hotspot_num = int(self.state[current_index - 1])
        # 选择了的hotspot 和 当前时刻的hotspot，两个hotspot 间的距离
        if current_hotspot_num == 0:
            # 如果当前时刻是0 ，表示还在基站没有出发
            current_hotspot = BaseStation()
        else:
            current_hotspot = self.getHotspotFromHotspotsListByNum(current_hotspot_num)
        selected_hotspot = self.getHotspotFromHotspotsListByNum(selected_hotspot_num)

        distance = self.getDistanceBetweenHotspots(selected_hotspot, current_hotspot)
        # 移动到选择的hotspot 花费的时间 单位 秒
        moving_time = distance / 5
        # 将 移动时间累加到 state 的最后一位中
        self.move_time += moving_time
        # MC 从当前 的 hotspot，移动到 被选中的hotspot 的时间
        total_time_seconds = round(total_wait_time * self.t * 60 + move_time + moving_time)

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
        # 充电完成后 属于current_phase 这个时间段
        current_phase = math.ceil(charging_end_time_seconds / 3600)
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
                        # 更新上一次被充电的时间
                        sensor[2] = str(present_time.hour) + ':' + str(present_time.minute) + ':' + str(present_time.second)
                        # 更新state中 的剩余寿命信息的状态
                        for i in range(501, len(self.state)):
                            if int(sensor_num) == int(self.state[i]):
                                self.state[i] = int(self.state[i])

                        # 更新state 中的 sensor 访问hotspot 的信息
                        path = 'C:/E/dataSet/2018-05-29/sensor/' + str(current_phase) + '点时间段访问hotspot/'
                        # 获取当前目录下的所有文件
                        files = os.listdir(path)
                        for file in files:
                            # 获得sensor的编号，即是文件的名称
                            sensor = int(file.split('.')[0])
                            with open(path + file) as f:
                                # 获取文件的每一行
                                for line in f:
                                    # 用逗号分割，得到list
                                    data = line.strip().split(',')
                                    # 得到 hotspot 的编号
                                    hotspot = int(data[2])
                                    # 如果 int(data[3]) 为0，即表示sensor没有访问hotspot，反之就访问了
                                    if int(data[3]) == 0:
                                        isbelong = 0
                                    else:
                                        isbelong = 1
                                    # sensor访问hotspot的信息用3位表示，如 179.161 表示179号sensor 访问了 16号hotspot
                                    # 所以这里需要修改的是最后一个小数位，用实数位和前两个小数位来匹配，修改信息
                                    sensor_hotspot = round(sensor + hotspot/100, 2)
                                    for i in range(501, len(self.state)):
                                        if sensor_hotspot == round(self.state[i], 2):
                                            self.state[i] = round(sensor + hotspot/100 + isbelong/1000, 3)

                        reword += math.exp(-rl)
                    else:
                        reword += -0.5
        # mc 给到达的sensor 充电后，如果能量为负或者 充电后的时间 大于 结束的时间，则回合结束，反之继续
        end_time_str = '21:59:59'
        end_time = datetime.strptime(end_time_str, '%H:%M:%S')
        if self.sensors_mobile_charger['MC'][0] <= 0 or charging_end_time > end_time:
            done = True
        else:
            done = False

        return self.state, reword, done

    def reset(self):
        # 前面的501个位置表示 CS 的相关信息
        for i in range(501):
            self.state.append(0)
        path = 'C:/E/dataSet/2018-05-29/sensor/8点时间段访问hotspot/'
        # 获取当前目录下的所有文件
        files = os.listdir(path)
        for file in files:
            # 获得sensor的编号，即是文件的名称
            sensor = file.split('.')[0]
            # 当前sensor 的剩余寿命
            sensor_reserved_rl = self.sensors_mobile_charger[sensor][0] / self.sensors_mobile_charger[sensor][1]
            # 如果剩余寿命大于两个小时，则添加形如 1.0 的数据到state，否则添加 形如1.1的数据到state，因为不会出现
            # 剩余寿命为0 的情况，所以不考虑
            if sensor_reserved_rl > 2 * 3600:
                self.state.append(float(sensor))
            else:
                self.state.append(float(sensor) + 0.1)
            with open(path + file) as f:
                for line in f:
                    # 对每一行进行分割
                    data = line.strip().split(',')
                    hotspot = int(data[2])
                    if int(data[3]) == 0:
                        isbelong = 0
                    else:
                        isbelong = 1
                    self.state.append(round(int(sensor) + hotspot/100 + isbelong/1000, 3))
        return self.state

    # 初始化获取所有的 hotspot,放入 属性self.hotspots中
    def getAllHotSpots(self):
        path = 'hotspot.txt'
        with open(path) as file:
            for line in file:
                data = line.strip().split(',')
                hotspot = Hotspot(float(data[0]), float(data[1]), int(data[2]))
                self.hotspots.append(hotspot)

    # 通过编号获得 hotspot
    def getHotspotFromHotspotsListByNum(self, num):
        for hotspot in self.hotspots:
            if hotspot.get_num() == num:
                return hotspot

    # 得到两个hotspot 间的距离
    def getDistanceBetweenHotspots(self, p1, p2):
        x = p1.get_x() - p2.get_x()
        y = p1.get_y() - p2.get_y()
        return math.sqrt((x ** 2) + (y ** 2))

    # 得到hotspot 和 轨迹点间的距离
    def getDistanceBetweenHotspotAndPoint(self, p1, p2):
        x = p1.get_x() - p2.get_x()
        y = p1.get_y() - p2.get_y()
        return math.sqrt((x ** 2) + (y ** 2))

    # 初始化所有的sensor 和 mc 的能量信息和能量消耗速率，上一次被充电的时间
    def set_sensors_mobile_charger(self):
        self.sensors_mobile_charger['000'] = [0.7 * 10.8 * 1000, 0.6, '08:00:00']
        self.sensors_mobile_charger['001'] = [0.3 * 10.8 * 1000, 0.8, '08:00:00']
        self.sensors_mobile_charger['003'] = [0.9 * 10.8 * 1000, 1, '08:00:00']
        self.sensors_mobile_charger['004'] = [0.5 * 10.8 * 1000, 0.5, '08:00:00']
        self.sensors_mobile_charger['005'] = [0.1 * 10.8 * 1000, 0.8, '08:00:00']
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
        self.sensors_mobile_charger['167'] = [0.5 * 10.8 * 1000, 0.8, '08:00:00']
        self.sensors_mobile_charger['179'] = [0.8 * 10.8 * 1000, 0.9, '08:00:00']
        self.sensors_mobile_charger['MC'] = [2000 * 1000, 50]


if __name__ == '__main__':
    evn = Evn()
    evn.reset()
    state_, reword, done = evn.step('2_3')
    print(state_)
    print(reword)
    print(done)

