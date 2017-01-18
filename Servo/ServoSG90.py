import Adafruit_PCA9685
import time
import curses

class ServoSG90:
    servo_min = 150  # Min pulse length out of 4096
    servo_max = 600  # Max pulse length out of 4096
    pwm = Adafruit_PCA9685.PCA9685()
    max_degree = 180 # degrees your servo can rotate
    deg_increase = 6 # number of degrees to increase by each time

    def __init__(self, servo_min=150, servo_max=600):
        self.servo_min = servo_min
        self.servo_max = servo_max

    def set_pwm_freq(self, freq):
        self.pwm.set_pwm_freq(60)

    def set_degree(self, channel, d):
        if d > self.max_degree:
            d = self.max_degree

        if d < 0:
            d = 0

        degree_pulse = self.servo_min
        degree_pulse += int((self.servo_max - self.servo_min) / self.max_degree) * d
        self.pwm.set_pwm(channel, 0, degree_pulse)
