# -*- coding:utf-8 -*-
"""
  @file get_all_state.py
  @brief 获取所有配置状态的例程
  @n 实验现象：配置的状态打印在终端
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
    获取温度传感器的分辨率 ,不同的分辨率，获取的温度的精度不同
    resolution
            RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
            RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
            RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
            RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
  '''
  resolution = tmp.get_resolution()
  if resolution == RESOLUTION_0_5:
    print "resolution = 0.5 .C"
  elif resolution == RESOLUTION_0_25:
    print "resolution = 0.25 .C"
  elif resolution == RESOLUTION_0_125:
    print "resolution = 0.125 .C"
  else:
    print "resolution = 0.0625 .C"

  '''
    获取电源的配置模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                                低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
      POWER_UP_MODE         // 上电模式
      LOW_POWER_MODE        // 低功耗模式
  '''
  state = tmp.get_power_mode()
  if state == POWER_UP_MODE:
    print "Power on mode"
  else:
    print "low power mode"

  '''
    获取警报输出的模式
      COMPARATOR_OUTPUT_MODE           // 比较器输出模式
      INTERRPUT_OUTPUT_MODE            // 中断输出模式
  '''
  state = tmp.get_alert_output_mode()
  if state == COMPARATOR_OUTPUT_MODE:
    print "Comparator output mode"
  else:
    print "Interrupt output mode"

  '''
      获取ALE引脚的极性状态，引脚极性为高：ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
                             引脚极性为低：ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
      POLARITY_HIGH         // 引脚极性为高
      POLARITY_LOW          // 引脚极性为低
  '''
  state = tmp.get_polarity_state()
  if state == POLARITY_HIGH:
    print "Pin polarity is high"
  else:
    print "Pin polarity is low"

  '''
    获取响应模式，响应上限下限和临界值，或者只响应临界值，
      UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应
      ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
  '''
  state = tmp.get_alert_response_mode()
  if state == UPPER_LOWER_CRIT_RESPONSE:
    print "Both upper/lower and crti values respond"
  else:
    print "Critical response"


  '''
    设置报警温度滞后的范围，在上限下限和临界值的阈值上增加一个范围,滞后功能仅适用于降温（从热至冷）,
    也就是说上限减去滞后温度，ALE电平才恢复
    例如:温度上限为30.0度，滞后温度为+1.5度，当前是35度ALE已经产生电平翻转，
         要想ALE恢复电平，必须达到30-1.5（28.5）度，ALE引脚才能恢复电平
      HYSTERESIS_0_0        // 没有滞后，就是到达指定温度就响应
      HYSTERESIS_1_5        // 从热至冷要滞后1.5℃
      HYSTERESIS_3_0        // 从热至冷要滞后3.0℃
      HYSTERESIS_6_0        // 从热至冷要滞后6.0℃
  '''
  state = tmp.get_alert_hysteresis()
  if state == HYSTERESIS_0_0:
    print "The temperature lag range is 0 degrees"
  elif state == HYSTERESIS_1_5:
    print "The temperature lag range is 1.5 degrees"
  elif state == HYSTERESIS_3_0:
    print "The temperature lag range is 3.0 degrees"
  else:
    print "The temperature lag range is 6.0 degrees"
  
  
  '''
    获取报警模式状态，得到时报警模式或者非报警模式
      ENABLE_ALERT           // 报警模式
      DISABLE_ALERT          // 非报警模式
  '''
  state = tmp.get_alert_enable_state()
  if state == ENABLE_ALERT:
    print "Alarm mode"
  else:
    print "No alarm mode"

  '''
    获取锁定的状态，来判断是否可以修改上限下限和临界值的阈值
      CRIT_LOCK       // 锁定临界值，临界值的阈值不允许被修改
      WIN_LOCK        // 锁定上限下限，上限下限的阈值不允许被修改
      CRIT_WIN_LOCK   // 锁定临界值和上限下限，上限下限和临界值的数据都不允许被修改
      NO_LOCK         // 未锁定寄存器
  '''
  state = tmp.get_lock_state()
  if state == CRIT_LOCK:
    print "The crit is locked"
  elif state == WIN_LOCK:
    print "The upper and lower limits are locked"
  elif state == CRIT_WIN_LOCK:
    print "The upper and lower limits and crit are locked"
  else:
    print "no locked"

def loop():
  time.sleep(0.1)
  exit()

if __name__ == "__main__":
  setup()
  while True:
    loop()