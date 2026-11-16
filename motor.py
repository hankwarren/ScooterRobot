from machine import Pin, PWM
import time #importing time for delay  

class Motor:
    def __init__(self):
        # Defining motor pins
        # the pin numbers used here are GPIO numbers
        #OUT1  and OUT2
        self.In1=Pin(1,Pin.OUT) 
        self.In2=Pin(0,Pin.OUT)  
        self.SpeedA=PWM(Pin(8))
        self.SpeedA.freq(1000)


        #OUT3  and OUT4
        self.In3=Pin(2,Pin.OUT)  
        self.In4=Pin(3,Pin.OUT)  
        self.SpeedB=PWM(Pin(9))
        self.SpeedB.freq(1000)
        
        self.speed_A = 15000
        self.speed_B = 15000

    def move_forward(self):
        print("forward")
        self.In1.high()
        self.In2.low()
        self.In3.low()
        self.In4.low()
    
    def move_backward(self):
        print("backward")
        self.In1.low()
        self.In2.high()
        self.In3.high()
        self.In4.high()
    
    def turn_right(self):
        print("right")
        self.In1.low()
        self.In2.low()
        self.In3.low()
        self.In4.high()
    
    def turn_left(self):
        print("left")
        self.In1.low()
        self.In2.high()
        self.In3.low()
        self.In4.low()
        
    def stop(self):
        print("stop")
        self.In1.low()
        self.In2.low()
        self.In3.low()
        self.In4.low()

    def set_speed_A(self, s):
        self.speed_A = s
        
    def set_speed_B(self, s):
        self.speed_b = s
        
    def get_speed_A(self):
        return self.speed_A
    
    def get_speed_B(self):
        return self.speed_B

if __name__ == '__main__':
    motor = Motor()
    while True:
        motor.speedA.duty_u16(self.get_speed_A())
        motor.speedB.duty_u16(self.get_speed_B())
        motor.move_forward()
        time.sleep(2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              )

        motor.stop()

        motor.move_backward()
        time.sleep(2)
        motor.stop()
    
        motor.turn_left()
        time.sleep(2)
        motor.stop()
    
        motor.turn_right()
        time.sleep(2)
    
        motor.stop()
        time.sleep(1)
    