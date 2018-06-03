from datetime import datetime
if __name__ == '__main__':
    time_str = '21:59:58'
    time_1 = datetime.strptime(time_str, '%H:%M:%S')
    time_2 = datetime.strptime('21:59:56', '%H:%M:%S')
    print(time_1)
    print(time_2)
    sec = (time_1 - time_2).seconds
    if sec < 10:
        print("a")

