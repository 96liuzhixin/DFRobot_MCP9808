# -*- coding:utf-8 -*-
"""
  @file get_temperature.py
  @brief 比较器获取温度的例子
  @n 实验现象：温度在串口显示，测量温度随环境温度改变而改变
  @n 实验现象：打印当前温度和上限下限温度和临界值温度的状态，比如说当前温度大于临界值温度，小于下限温度，大于上限温度
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
  
  '''
    设置警报输出的模式，比较器输出模式不需要清除中断，中断模式需要清除中断
      COMPARATOR_OUTPUT_MODE           // 比较器输出模式不需要清除中断，比较模式的触发是，当温度高于上限或温度低于下限或者温度超过临界值
        例如：使能了报警模式，设置ALE引脚为低电平活动，当超过上限警报的温度时，
              ALE引脚从高电平到低电平，当温度低于上限但高于下限时，ALE引脚恢复高电平
      INTERRPUT_OUTPUT_MODE            // 中断输出模式需要清除中断，当产生警报时如果不清除中断中断一直存在，中断模式的触发，是从一种状态变为另一种状态
        例如：设置了下限阈值20度，上限阈值25度，临界阈值30度，当温度一直低于20度时不产生中断，
              当温度超过25度时才产生中断，ALE引脚跳变，此时应该清空中断，ALE引脚恢复，特殊情况，
              当ALE引脚大于临界温度30度时，中断模式失效，清空中断也失效，必须等温度降到30度以下，才恢复中断模式。
  '''
  if 0 == tmp.set_alert_output_mode(COMPARATOR_OUTPUT_MODE):
    print "The comparator mode was set successfully"
  else:
    print "Register lock or parameter error"

  '''
    设置ALE引脚的极性
      POLARITY_HIGH         // 设置ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
      POLARITY_LOW          // 设置ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
  '''
  if 0 == tmp.set_polarity(POLARITY_LOW):
    print "Pin polarity set successfully"
  else:
    print "Register lock or parameter error"

  '''
    设置响应模式，响应上限下限和临界值，或者只响应临界值，只响应临界值不适用于中断模式
      UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应
      ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
  '''
  if 0 == tmp.set_alert_response_mode(UPPER_LOWER_CRIT_RESPONSE):
    print "Set response mode successfully"
  else:
    print "Register lock or parameter error"

  '''
    设置上限和下限阈值,根据配置的中断模式响应，高于这个温度和低于这个温度的响应，最多两位小数
      upper
        // 设置的温度上限，自动处理成0.25的倍数，范围为-40 到 +125度
      lower
        // 设置的温度下限，自动处理成0.25的倍数，范围为-40 到 +125度
  '''
  if 0 == tmp.set_upper_lower_tereshold(32.5 ,20.5):
    print "Set upper limit threshold successfully"
  else:
    print "Failed to set upper limit because the upper limit of temperature is less than lower limit, or the upper limit and lower limit are less than two degrees or Register lock"
  
  '''
    设置温度临界值,根据配置的中断模式响应，这里的临界值温度必须大于上限温度
      value
        // 温度的临界值，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
  '''
  state = tmp.set_crit_threshold(35.5)
  if 0 == state:
    print "Set the threshold value for success"
  else:
    print "Register lock"
  
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
  if 0 == tmp.set_alert_hysteresis(HYSTERESIS_1_5):
    print "Set hysteresis temperature successfully"
  else:
    print "Register lock or parameter error"
  
  '''
    使能或者禁止报警模式，使能报警模式后，ALE引脚到达报警条件后会产生跳变，禁止报警模式ALE引脚没有响应
      ENABLE_ALERT           // 使能报警模式，ALE引脚到达报警条件后会产生跳变
      DISABLE_ALERT          // 禁止报警模式，禁止报警模式ALE引脚没有响应
  '''
  if 0 == tmp.set_alert_enable(ENABLE_ALERT):
    print "To enable or inhibit success"
  else:
    print "Register lock or parameter error"
  
  '''
    设置锁定模式和解锁，防止错误操作更改上限、下限、临界值、阈值的大小
      CRIT_LOCK       // 锁定临界值，临界值的阈值不允许被修改
      WIN_LOCK        // 锁定上限下限，上限下限的阈值不允许被修改
      CRIT_WIN_LOCK   // 锁定临界值和上限下限，上限下限和临界值的数据都不允许被修改
      NO_LOCK         // 不锁定寄存器
  '''
  if 0 == tmp.set_lock_state(NO_LOCK):
    print "locked successfully"
  else:
    print "parameter error"

def loop():
  temperature = tmp.get_temperature()
  '''
    获取当前比较器的状态，只有在比较器模式下有效
    比较器模式是比较当前温度和上限阈值，下限阈值，和临界值的关系
    TA 代表当前温度，TCRIT代表临界温度，TUPPER代表上限温度，TLOWER代表下限温度
      CRIT_0_UPPER_0_LOWER_0    // TA < TCRIT、TA ≤ TUPPER、TA ≥ TLOWER
      CRIT_0_UPPER_0_LOWER_1    // TA < TCRIT、TA ≤ TUPPER、TA < TLOWER
      CRIT_0_UPPER_1_LOWER_0    // TA < TCRIT、TA > TUPPER、TA ≥ TLOWER
      CRIT_0_UPPER_1_LOWER_1    // TA < TCRIT、TA > TUPPER、TA < TLOWER
      CRIT_1_UPPER_0_LOWER_0    // TA ≥ TCRIT、TA ≤ TUPPER、TA ≥ TLOWER
      CRIT_1_UPPER_0_LOWER_1    // TA ≥ TCRIT、TA ≤ TUPPER、TA < TLOWER
      CRIT_1_UPPER_1_LOWER_0    // TA ≥ TCRIT、TA > TUPPER、TA ≥ TLOWER
      CRIT_1_UPPER_1_LOWER_1    // TA ≥ TCRIT、TA > TUPPER、TA < TLOWER
  '''
  state = tmp.get_comparator_state()
  if state == CRIT_0_UPPER_0_LOWER_0:
    print "temperature = %.2f .C  CRIT_0_UPPER_0_LOWER_0 "%temperature
  elif state == CRIT_0_UPPER_0_LOWER_1:
    print "temperature = %.2f .C  CRIT_0_UPPER_0_LOWER_1 "%temperature
  elif state == CRIT_0_UPPER_1_LOWER_0:
    print "temperature = %.2f .C  CRIT_0_UPPER_1_LOWER_0 "%temperature
  elif state == CRIT_0_UPPER_1_LOWER_1:
    print "temperature = %.2f .C  CRIT_0_UPPER_1_LOWER_1 "%temperature
  elif state == CRIT_1_UPPER_0_LOWER_0:
    print "temperature = %.2f .C  CRIT_1_UPPER_0_LOWER_0 "%temperature
  elif state == CRIT_1_UPPER_0_LOWER_1:
    print "temperature = %.2f .C  CRIT_1_UPPER_0_LOWER_1 "%temperature
  elif state == CRIT_1_UPPER_1_LOWER_0:
    print "temperature = %.2f .C  CRIT_1_UPPER_1_LOWER_0 "%temperature
  elif state == CRIT_1_UPPER_1_LOWER_1:
    print "temperature = %.2f .C  CRIT_1_UPPER_1_LOWER_1 "%temperature
  else:
    print "The state does not exist"
  time.sleep(1)

if __name__ == "__main__":
  setup()
  while True:
    loop()