import Adafruit_PCA9685.PCA9685 as PCA9685
import Adafruit_GPIO.I2C as I2C

#i2c = I2C
#device = i2c.get_i2c_device(0x40)
#device.writeRaw8(0x06)
driver = PCA9685()
driver.set_pwm_freq(60)

channel = raw_input('Enter channel #: ')
degree = raw_input('Enter degrees: ')
tick = 150 + int((600-150)/180) * int(degree)
# for channel 0, go high from start (0), and transition back to low after tick X
driver.set_pwm(int(channel), 0, int(tick))

