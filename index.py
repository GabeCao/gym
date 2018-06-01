from Hotspot import Hotspot
import math
import os

class Evn:
    def __init__(self):
        self.hotspots = []
        self.getAllHotSpots()

    def getHotspotFromHotspotsListByNum(self, num):
        for hotspot in self.hotspots:
            if hotspot.get_num() == num:
                return hotspot

    def getDistanceBetweenDistance(self, p1, p2):
        x = p1.get_x() - p2.get_x()
        y = p1.get_y() - p2.get_y()
        return math.sqrt((x ** 2) + (y ** 2))

    def test(self):
        p1 = self.getHotspotFromHotspotsListByNum(2)
        p2 = self.getHotspotFromHotspotsListByNum(3)
        return self.getDistanceBetweenDistance(p1, p2)

    def getAllHotSpots(self):
        path = 'hotspot.txt'
        with open(path) as file:
            for line in file:
                data = line.strip().split(',')
                hotspot = Hotspot(float(data[0]), float(data[1]), int(data[2]))
                self.hotspots.append(hotspot)

if __name__ == '__main__':
    for i in range(3, 11):
        print(i)