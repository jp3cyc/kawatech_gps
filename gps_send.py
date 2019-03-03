from gps3 import gps3
import urllib.request


# GPSの設定
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

# csvファイルへの書き出しをする．データは追加する
path = '/home/pi/GPS/data/gpslog.csv'

f = open(path,mode='a')

data = "time, lat, lon, alt, speed \n"
f.write(data)

gps_count = 0


for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)

        gps_time = str(data_stream.TPV['time'])
        gps_lat =  str(data_stream.TPV['lat'])
        gps_lon = str(data_stream.TPV['lon'])
        gps_alt = str( data_stream.TPV['alt'] ) 
        gps_speed = str(data_stream.TPV['speed'])

        data =  gps_time + "," + gps_lat + "," + gps_lon + "," + gps_alt + "," + gps_speed + "\n" 

        print(data)
        f.write(data)

        if( (gps_lat != "n/a") and (gps_lon != "n/a")): # GPS受信時のみデータをサーバに送る
                gps_count += 1
                if(gps_count == 1):     # 10回に1回送信する設定
                        p = "latitude=" + gps_lat + "&longitude=" + gps_lon

                        url = "https://jp3cyc.jp/?"+p # GPSデータを送信するサーバを指定する．
                        
                        print (url)

                        with urllib.request.urlopen(url) as res:
                                html = res.read()
                                print(html) # サーバからの応答が表示される
                elif(gps_count >= 9):
                        gps_count = 0
               

