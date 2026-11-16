import network
import socket
from time import sleep
import machine
from motor import Motor
from servo import Servos
from machine import I2C, Pin, Timer
from ssd1306 import SSD1306_I2C

class Server:
    def __init__(self):
        self.ssid = 'belkin.490'
        self.password = '2aa4d2aa'

#led = Pin("LED", Pin.OUT)
#timer = Timer()

    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(pm=0xA11140) # magic?
        wlan.connect(self.ssid, self.password)
        count = 0
        while wlan.isconnected() == False:
            print(f'{count}: Waiting for connection...')
            sleep(1)
            count = count + 1
        
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        return ip

    def open_socket(self, ip):
        address = (ip, 80)
        connection = socket.socket()
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        connection.bind(address)
        connection.listen(1)
        return connection
        
    def webpage(self):
        html = f"""
<!DOCTYPE html>
<html>
<body>
<head>
<title>Robot Control</title>
</head>
<center><b>
    <form action="./forward">
    <input type="submit" value="Forward" style="height:120px; width: 120px" />
    </form>
    
    <table><tr>
    <td>
    <form action="./left">
    <input type="submit" value="Left" style="height:120px; width: 120px" />
    </form>
    </td>
    <td>
    <form action="./stop">
    <input type="submit" value="Stop" style="height:120px; width: 120px" />
    </form>
    </td>
    <td>
    <form action="./right">
    <input type="submit" value="Right" style="height:120px; width: 120px" />
    </form>
    </td>
    </tr></table>
    
    <form action="./backward">
    <input type="submit" value="Backward" style="height:120px; width: 120px" />
    </form>
    <table><tr>
    <td>
    <form action="/speed1">
    <input type="submit" value="speed1" style="height:120px; width: 120px" />
    </form>
    </td>
        <td>
    <form action="/speed2">
    <input type="submit" value="speed1" style="height:120px; width: 120px" />
    </form>
    </td>
    <td>
    <form action="/speed3">
    <input type="submit" value="speed2" style="height:120px; width: 120px" />
    </form>
    </td>
    <td>
    <form action="/speed4">
    <input type="submit" value="speed3" style="height:120px; width: 120px" />
    </form>
    </td>
    <td>
    <form action="/speed5">
    <input type="submit" value="speed4" style="height:120px; width: 120px" />
    </form>
    </td>
    </tr></table>
</center>
</body>
</html>
"""
        return str(html)

    def serve(self, connection, motor):
        motor.SpeedA.duty_u16(motor.get_speed_A())
        motor.SpeedB.duty_u16(motor.get_speed_B())
        while True:
            client = connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            # print('------------------------')
            # print(request)
        
            try:
                request = request.split()[1]
                # print(f'{request} received')
            except IndexError:
                pass
            
            print(request)
            if request == '/left?':
                motor.turn_left()
            elif request == '/forward?':
                motor.move_forward()
            elif request == '/right?':
                motor.turn_right()
            elif request == '/backward?':
                motor.move_backward()
            elif request == '/stop?':
                motor.stop()
            elif request == '/speed1?':
                motor.set_speed_A(15000)
                motor.set_speed_B(15000)
                motor.SpeedA.duty_u16(motor.get_speed_A())
                motor.SpeedB.duty_u16(motor.get_speed_B())
            elif request == '/speed2?':
                motor.set_speed_A(20000)
                motor.set_speed_B(20000)
                motor.SpeedA.duty_u16(motor.get_speed_A())
                motor.SpeedB.duty_u16(motor.get_speed_B())
            elif request == '/speed3?':
                motor.set_speed_A(25000)
                motor.set_speed_B(25000)
                motor.SpeedA.duty_u16(motor.get_speed_A())
                motor.SpeedB.duty_u16(motor.get_speed_B())
            elif request == '/speed4?':
                motor.set_speed_A(30000)
                motor.set_speed_B(30000)
                motor.SpeedA.duty_u16(motor.get_speed_A())
                motor.SpeedB.duty_u16(motor.get_speed_B())          

        #led.toggle()
        
            html = self.webpage()
            client.send(html)
            client.close()


#def blink(timer):
#    led.toggle()

def main():
    try:
        id = 0
        scl = Pin(17)
        sda = Pin(16)
        WIDTH = 128
        HEIGHT = 32
        i2c = I2C(id=id, scl=scl, sda=sda, freq=200000)
        oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

        # timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
    	server = Server()
        motor = Motor()

        
        ip = server.connect()
        print( f'connected on {ip}')

        oled.fill(0)
        oled.hline(0,0, 127, 1)
        oled.text(ip, 0, 2)
        oled.hline(0, 31, 127, 1)
        oled.show()
        

        connection = server.open_socket(ip)
        server.serve(connection, motor)
    
    except KeyboardInterrupt:
        machine.reset()
    
if __name__ == '__main__':
    main()