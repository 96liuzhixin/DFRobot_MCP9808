# -*- coding:utf-8 -*-
"""
  @file get_temperature.py
  @brief 普通获取温度的例子
  @n 实验现象：温度在串口显示，测量温度随环境温度改变而改变
  @n i2c 地址选择，默认i2c地址为0x1F，A2、A1、A0引脚为高电平，
  @n 其8中组合为,1代表高电平，0代表低电平
                | A2 | A1 | A0 |
                | 0  | 0  | 0  |    0x18
                | 0  | 0  | 1  |    0x19
                | 0  | 1  | 0  |    0x1A
                | 0  | 1  | 1  |    0x1B
                | 1  | 0  | 0  |    0x1D
                | 1  | 0  | 1  |    0x1D
                | 1  | 1  | 0  |    0x1E
                | 1  | 1  | 1  |    0x1F   default i2c address
                
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  @version  V0.2
  @date  2021-03-27
  @get from https://www.dfrobot.com
  @url https://www.dfrobot.com
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from DFRobot_MCP9808 import *

I2C_1       = 0x01               # I2C_1 使用i2c1接口驱动传感器， 可以调整为i2c0但是需要配置树莓派的文件
I2C_ADDRESS = 0x1F               # I2C 设备的地址，可以更改A2、A1、A0来更换地址，默认地址为0x1F
tmp = DFRobot_MCP9808_I2C(I2C_1 ,I2C_ADDRESS)

def setup():
  while ERROR == tmp.sensor_init():
    print "sensor init error ,please check connect or device id or manufacturer id error"
  print "sensor init success"
  '''
    设置温度传感器的分辨率，不同的分辨率，获取的温度的精度不同
    resolution
            RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
            RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
            RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
            RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
  '''
  if 0 == tmp.set_resolution(RESOLUTION_0_25):
    print "Resolution set successfully"
  else:
    print "parameter error"

  '''
    设置电源模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                  低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
      POWER_UP_MODE         // 上电模式
      LOW_POWER_MODE        // 低功耗模式
  '''
  if 0 == tmp.set_power_mode(POWER_UP_MODE):
    print "Power mode was set successfully"
  else:
    print "Register lock"

def loop():
  temperature = tmp.get_temperature()
  print "temperature = %.2f .C"%temperature
  print ""
  time.sleep(1)

if __name__ == "__main__":
  setup()
  while True:
    loop()