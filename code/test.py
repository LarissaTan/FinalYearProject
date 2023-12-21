from store_data_pulse import *
from store_data import *
from datetime import datetime
from arima import perform_arma_prediction
'''
data = [11, 23, 32, 43, 54, 65, 76, 87, 98, 102]


print(perform_arma_prediction(data))


write_data_pulse("2023-12-13 23:45:51;106")
write_data_pulse("2023-12-13 23:46:27;104")
write_data_pulse("2023-12-13 23:46:49;105")
write_data_pulse("2023-12-13 23:47:02;102")
write_data_pulse("2023-12-13 23:47:26;102")
write_data_pulse("2023-12-13 23:47:38;99")

write_data_pulse("2023-12-13 23:48:02;101")
write_data_pulse("2023-12-13 23:48:14;107")
write_data_pulse("2023-12-13 23:48:39;108")
write_data_pulse("2023-12-13 23:48:51;110")

write_data("2023-12-13 23:46:27;2.056")
write_data("2023-12-13 23:46:49;1.997")
write_data("2023-12-13 23:47:02;2.076")
write_data("2023-12-13 23:47:26;2.238")
write_data("2023-12-13 23:47:38;2.012")

write_data("2023-12-13 23:48:02;2.413")
write_data("2023-12-13 23:48:14;2.264")
write_data("2023-12-13 23:48:39;2.716")
write_data("2023-12-13 23:48:51;2.801")
write_data("2023-12-13 23:49:26;2.798") ''' 
tmps = read_data()
print(tmps.__len__())
#print(tmps[-1][0]) #最后新的时间获取

for tmp in tmps:
    print(tmp)
   
'''
    print("....")
    print(tmp[1])
    print(tmp[2])
    print(tmp[0])
    print("....")
    

    date_object = datetime.strptime(tmp[0], "%Y-%m-%d %H:%M:%S")
    print("Date Object:", date_object)
    # 获取当前时间
    current_time = datetime.now()

    # 比较两个 datetime 对象
    if date_object > current_time:
        print("日期在当前时间之后")
    elif date_object < current_time:
        print("日期在当前时间之前")
    else:
        print("日期与当前时间相同")
    print("Value 1:", tmp[1])
    print("Value 2:", tmp[2])


    write_data("2023-12-13 23:46:27;2.056;104")
    write_data("2023-12-13 23:46:49;1.997;105")
    write_data("2023-12-13 23:47:02;2.076;102")
    write_data("2023-12-13 23:47:26;2.238;102")
    write_data("2023-12-13 23:47:38;2.012;99")

    write_data("2023-12-13 23:48:02;2.413;101")
    write_data("2023-12-13 23:48:14;2.264;107")
    write_data("2023-12-13 23:48:39;2.716;108")
    write_data("2023-12-13 23:48:51;2.801;110")
    write_data("2023-12-13 23:49:26;2.798;-1")

write_data("2023-12-13 23:45:51;106")
write_data("2023-12-13 23:46:27;104")
write_data("2023-12-13 23:46:49;105")
write_data("2023-12-13 23:47:02;102")
write_data("2023-12-13 23:47:26;102")
write_data("2023-12-13 23:47:38;99")

write_data("2023-12-13 23:48:02;101")
write_data("2023-12-13 23:48:14;107")
write_data("2023-12-13 23:48:39;108")
write_data("2023-12-13 23:48:51;110")
    '''
