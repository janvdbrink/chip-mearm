Synopsis

This is a small python script that was written for the CHIP to have it used for the MeArm robotic arm (http://www.instructables.com/id/MeArm-Robot-Arm-Your-Robot-V10). It uses a PCA9685 i2c-controlled PWM driver to control the 4 servos, and takes any command through a standard web browser interface. 


Installation

First setup WIFI, as described here: https://docs.getchip.com/chip.html#wifi-connection. Install the Adafruit Python PCA9685 library from source:<br />
    sudo apt-get install git build-essential python-dev python<br />
    cd ~<br />
    git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git <br />
    cd Adafruit_Python_PCA9685 <br />
    sudo python setup.py install <br />

The default I2C bus is now i2c-2 as i2c-1 was removed in OS 1.1 (4.4 Kernel), please ensure your using this, and that the PCA9685 was detected at address 40h using "i2cdetect -y 2". That's it! Just Put all files in a folder (and include the subfolder "Servo") and run it as a standard python script:
    python httpd.py

    
Contributors

- Jan van den Brink (@janvdbrink)

License

MIT License. (c) Jan van den Brink
