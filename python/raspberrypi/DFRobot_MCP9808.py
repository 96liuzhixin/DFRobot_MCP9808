# -*- coding: utf-8 -*
""" 
  @file DFRobot_MCP9808.py
  @note DFRobot_MCP9808 Class infrastructure, implementation of underlying methods
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  version  V0.2
  date  2021-03-27
  @get from https://www.dfrobot.com
  @url https://www.dfrobot.com
"""
import serial
import time
import smbus
import spidev
import os
import RPi.GPIO as GPIO

#GPIO.setwarnings(False)
ERROR                          = -1
NONE                           = (0x00)

FRU_REGISTER                   = (0x00 & 0x0F)
CONFIG_REGISTER                = (0x01 & 0x0F)
T_UPPER_REGISTER               = (0x02 & 0x0F)
T_LOWER_REGISTER               = (0x03 & 0x0F)
T_CRIT_REGISTER                = (0x04 & 0x0F)
TEMPERATURE_REGISTER           = (0x05 & 0x0F)
MANUFACTURER_REGISTER          = (0x06 & 0x0F)
DEVICE_REGISTER                = (0x07 & 0x0F)
RESOLUTION_REGISTER            = (0x08 & 0x0F)

MANUFACTURER_ID                = (0x54)
DEVICE_ID                      = (0x04)

CRIT_0_UPPER_0_LOWER_0         = (0x00 << 5)
CRIT_0_UPPER_0_LOWER_1         = (0x01 << 5)
CRIT_0_UPPER_1_LOWER_0         = (0x02 << 5)
CRIT_0_UPPER_1_LOWER_1         = (0x03 << 5)
CRIT_1_UPPER_0_LOWER_0         = (0x04 << 5)
CRIT_1_UPPER_0_LOWER_1         = (0x05 << 5)
CRIT_1_UPPER_1_LOWER_0         = (0x06 << 5)
CRIT_1_UPPER_1_LOWER_1         = (0x07 << 5)

RESOLUTION_0_5                 = (0x00 & 0x03)
RESOLUTION_0_25                = (0x01 & 0x03)
RESOLUTION_0_125               = (0x02 & 0x03)
RESOLUTION_0_0625              = (0x03 & 0x03)      # default resolutivn

COMPARATOR_OUTPUT_MODE         = 0x00               # default comparator mode
INTERRPUT_OUTPUT_MODE          = 0x01

CRIT_LOCK                      = 0x80
WIN_LOCK                       = 0x40
CRIT_WIN_LOCK                  = 0xC0
NO_LOCK                        = 0x00               # default no lock
POWER_UP_MODE                  = 0x00               # dafault power up
LOW_POWER_MODE                 = 0x01

HYSTERESIS_0_0                 = 0x00               # default hysteresis
HYSTERESIS_1_5                 = 0x02
HYSTERESIS_3_0                 = 0x04
HYSTERESIS_6_0                 = 0x06

POLARITY_HIGH                  = 0x02
POLARITY_LOW                   = 0x00               # default active low

ENABLE_ALERT                   = 0x08
DISABLE_ALERT                  = 0x00               # default disable

ONLY_CRIT_RESPONSE             = 0x40
UPPER_LOWER_CRIT_RESPONSE      = 0x00               # dafault output mode

class DFRobot_MCP9808(object):
  def __init__(self ,bus):
    if bus != 0:
      self.i2cbus = smbus.SMBus(bus)

  '''
    @brief 初始化传感器，对比传感器的芯片id 和 厂商 id
    @return 0  is init success
            -1 芯片id 或者厂商id错误，请检查
  '''
  def sensor_init(self):
    device_id = self.get_device_id()
    manufaturer_id = self.get_manufacturer_id()
    if device_id == DEVICE_ID and manufaturer_id == MANUFACTURER_ID:
      return 0
    else:
      return -1

  '''
    @brief get device id
    @return device id
                DEVICE_ID          // device id is 0x04
  '''
  def get_device_id(self):
    rslt = self.read_reg(DEVICE_REGISTER ,2)
    return rslt[0]

  '''
    @brief get manufacturer id
    @return manufacturer id
                MANUFACTURER_ID    // manufacturer id is 0x54
  '''
  def get_manufacturer_id(self):
    rslt = self.read_reg(MANUFACTURER_REGISTER ,2)
    return rslt[1]

  '''
    @brief 设置温度传感器的分辨率，不同的分辨率，获取的温度的精度不同
    @param resolution
                RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
                RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
                RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
                RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
    @return state
                0    is set successfully
                -1   设置的分辨率错误，请检查分辨率参数
  '''
  def set_resolution(self ,resolution):
    txbuf = [0]
    if resolution == RESOLUTION_0_5 or resolution == RESOLUTION_0_25 or resolution == RESOLUTION_0_125 or resolution == RESOLUTION_0_0625:
      txbuf[0] = resolution
      self.write_reg(RESOLUTION_REGISTER ,txbuf)
      return 0
    else:
      return -1

  '''
    @brief 获取温度传感器的分辨率 ,不同的分辨率，获取的温度的精度不同
    @return resolution
                RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
                RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
                RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
                RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
  '''
  def get_resolution(self):
    rslt = self.read_reg(RESOLUTION_REGISTER ,1)
    return rslt[0]&0x03

  '''
    @brief 获取当前的环境温度，注意设置不同分辨率能够得到的温度精度不同
    @return 温度值为浮点数，
  '''
  def get_temperature(self):
    rslt = self.read_reg(TEMPERATURE_REGISTER ,2)
    rslt[0] &= 0x1F
    if rslt[0]&0x10 == 0x10:
      rslt[0] &= 0x0F
      return 256.0-(float(rslt[0]*16.0) + float(rslt[1]/16.0))
    else:
      return float(rslt[0]*16.0) + float(rslt[1]/16.0)

  '''
    @brief 获取当前比较器的状态，只有在比较器模式下有效
           比较器模式是比较当前温度于上限阈值，下限阈值，和临界值的关系的模式
    @return state
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
  def get_comparator_state(self):
    rslt = self.read_reg(TEMPERATURE_REGISTER ,2) 
    return (rslt[0]&0xE0)

  '''
    @brief 设置电源模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                         低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
    @param mode
                POWER_UP_MODE         // 上电模式
                LOW_POWER_MODE        // 低功耗模式
    @return 0x00 is set success
            -1   设置失败，寄存器已经锁定，请先解锁寄存器
  '''
  def set_power_mode(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    rslt[0] &= 0x06
    rslt[0] |= (mode&0x01);
    self.write_reg(CONFIG_REGISTER ,rslt)
    return 0

  '''
    @brief 获取电源的配置模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                                低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
    @return mode
                POWER_UP_MODE         // 上电模式
                LOW_POWER_MODE        // 低功耗模式
  '''
  def get_power_mode(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[0]&0x01)

  '''
    @brief 设置锁定模式或解锁，防止错误操作更改上限、下限、临界值的大小
    @param lock
                CRIT_LOCK       // 锁定临界值，临界值的阈值不允许被修改
                WIN_LOCK        // 锁定上限下限，上限下限的阈值不允许被修改
                CRIT_WIN_LOCK   // 锁定临界值和上限下限，上限下限和临界值的数据都不允许被修改
                NO_LOCK         // 不锁定寄存器
     @return state
                0x00 is set successfully
                0xFE 设置的模式错误
  '''
  def set_lock_state(self ,lock):
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if lock == CRIT_LOCK or lock == WIN_LOCK or lock == CRIT_WIN_LOCK or lock == NO_LOCK:
      rslt[1] &= 0x3F
      rslt[1] |= lock
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xfe

  '''
    @brief 获取锁定的状态，来判断是否可以修改上限下限和临界值的阈值
    @return state
                CRIT_LOCK       // 临界值锁定，临界值的阈值不允许被修改
                WIN_LOCK        // 上限下限锁定，上限下限的阈值不允许被修改
                CRIT_WIN_LOCK   // 临界值和窗口同时锁定，上限下限和临界值的数据都不允许被修改
                NO_LOCK         // 没有锁定，上限下限和临界值的阈值都可以被修改
  '''
  def get_lock_state(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0xC0)

  '''
    @brief 设置报警温度滞后的范围，在上限下限和临界值的阈值上增加一个范围,滞后功能仅适用于降温（从热至冷）
            ,也就是说（上限/下限/临界值）减去滞后温度，ALE电平才恢复
            例如:温度上限为30.0度，滞后温度为+1.5度，当前是35度ALE已经产生电平翻转，
            要想ALE恢复电平，必须达到30-1.5（28.5）度，ALE引脚才能恢复电平
    @param mode
                HYSTERESIS_0_0        // 没有滞后，就是到达指定温度就响应
                HYSTERESIS_1_5        // 从热至冷要滞后1.5℃
                HYSTERESIS_3_0        // 从热至冷要滞后3.0℃
                HYSTERESIS_6_0        // 从热至冷要滞后6.0℃
    @return state
                0x00 is set successfully
                -1 当前寄存器为锁定状态不允许修改
                0xFE 设置的范围错误，请检查范围
  '''
  def set_alert_hysteresis(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == HYSTERESIS_0_0 or mode == HYSTERESIS_1_5  or mode == HYSTERESIS_3_0 or mode == HYSTERESIS_6_0:
      rslt[0] &= 0x01
      rslt[0] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief 获取滞后的温度
    @return hysteresis
                HYSTERESIS_0_0        // 没有滞后，就是到达指定温度就响应
                HYSTERESIS_1_5        // 从热至冷要滞后1.5℃
                HYSTERESIS_3_0        // 从热至冷要滞后3.0℃
                HYSTERESIS_6_0        // 从热至冷要滞后6.0℃
  '''
  def get_alert_hysteresis(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[0]&0x06)

  '''
    @brief 使能或者禁止报警模式，使能报警模式后，ALE引脚到达报警条件后会产生跳变，禁止报警模式ALE引脚没有响应
    @param mode
                ENABLE_ALERT           // 使能报警模式，ALE引脚到达报警条件后会产生跳变
                DISABLE_ALERT          // 禁止报警模式，禁止报警模式ALE引脚没有响应
    @return state
                0x00 is set successfully
                -1   当前寄存器为锁定状态不允许修改
                0xFE 设置的模式错误，请检查模式
  '''
  def set_alert_enable(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == ENABLE_ALERT or mode == DISABLE_ALERT:
      rslt[1] &= 0xF7
      rslt[1] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief 获取报警模式状态，得到时报警模式或者非报警模式
    @return mode
                ENABLE_ALERT           // 报警模式
                DISABLE_ALERT          // 非报警模式
  '''
  def get_alert_enable_state(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x08)
  
  '''
    @brief 设置ALE引脚的极性，引脚极性为高：ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
                              引脚极性为低：ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
    @param polarity
                POLARITY_HIGH         // ALE引脚高电平为活动电平
                POLARITY_LOW          // ALE引脚低极性为活动电平
    @return state
                0x00 is set successfully
                -1   当前寄存器为锁定状态不允许修改
                0xFE 设置的极性错误，请检查极性
  '''
  def set_polarity(self ,polarity):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if polarity == POLARITY_HIGH or polarity == POLARITY_LOW:
      rslt[1] &= 0xFD
      rslt[1] |= polarity
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief 获取ALE引脚的极性状态，引脚极性为高：ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
                                  引脚极性为低：ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
    @return polarity
                POLARITY_HIGH         // ALE引脚高电平为活动电平
                POLARITY_LOW          // ALE引脚低极性为活动电平
  '''
  def get_polarity_state(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x02)

  '''
    @brief 设置警报输出的模式，比较器输出模式不需要清除中断，中断模式需要清除中断
    @param mode
                COMPARATOR_OUTPUT_MODE           // 比较器输出模式不需要清除中断，
                例如：使能了报警模式，设置ALE引脚为低电平活动
                      当超过上限警报的温度时，ALE引脚从高电平到低电平，当温度低于上限但高于下限时，ALE引脚恢复高电平
                INTERRPUT_OUTPUT_MODE            // 中断输出模式需要清除中断，当产生警报时，如果不清除中断中断一直存在，中断模式的触发，是从一种状态变为另一种状态，
                例如：设置了下限阈值20度，上限阈值25度，临界阈值30度，当温度一直低于20度时不产生中断，当温度超过25度时才产生中断，ALE引脚跳变，此时应该清空中断，ALE引脚                       恢复，特殊情况，当ALE引脚大于临界温度30度时，中断模式失效，清空中断也失效，必须等温度降到30度以下，才恢复中断模式
     @return state
                0x00 is set successfully
                -1 当前寄存器为锁定状态不允许修改
                0xFE 设置的警报输出模式错误，请检查模式
  '''
  def set_alert_output_mode(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == COMPARATOR_OUTPUT_MODE or mode == INTERRPUT_OUTPUT_MODE:
      rslt[1] &= 0xFE
      rslt[1] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief 获取警报输出的模式
    @return mode
                COMPARATOR_OUTPUT_MODE           // 比较器输出模式
                INTERRPUT_OUTPUT_MODE            // 中断输出模式
  '''
  def get_alert_output_mode(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x01)

  '''
    @brief 设置响应模式，响应上限下限和临界值，或者只响应临界值，只响应临界值不适用于中断模式
    @param mode
                UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应，
                ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
    @return state
                0x00 is set successfully
                -1   当前寄存器为锁定状态不允许修改
                0xFE 设置的响应模式错误，请检查模式
  '''
  def set_alert_response_mode(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == UPPER_LOWER_CRIT_RESPONSE or mode == ONLY_CRIT_RESPONSE:
      rslt[1] &= 0xFB
      rslt[1] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief 获取响应的模式
    @return mode
                UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应
                ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
  '''
  def get_alert_response_mode(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x04)

  '''
    @brief 设置上限和下限阈值,根据配置的中断模式响应，高于上限温度和低于下限温度响应
    @param upper
              // 温度上限，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
    @param lower
              // 温度下限，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
    @return state
                0x00                              // 设置上限下限成功
                -2                                // 设置上限下限失败，原因是温度上限小于下限，或者上限温度和下限温度小于两度
                -1                                // 设置上限下限失败，寄存器锁定不允许操作
  '''
  def set_upper_lower_tereshold(self ,upper ,lower):
    rslt = [0]*2
    if (upper-lower) < 2.0:
      return -2
    if self.get_lock_state() != 0:
      return -1  
    self.data_threshold_analysis(upper ,rslt)
    self.write_reg(T_UPPER_REGISTER ,rslt)
    rslt[0] = 0
    rslt[1] = 0
    self.data_threshold_analysis(lower ,rslt)
    self.write_reg(T_LOWER_REGISTER ,rslt)
    return 0

  '''
    @brief 设置温度临界值,根据配置的中断模式响应，这里的临界值温度必须大于上限温度
    @param value
              // 温度的临界值，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
    @return state
                0x00                              // 设置临界值成功
                -1                                // 设置临界值失败，寄存器锁定不允许操作
  '''
  def set_crit_threshold(self ,value):
    rslt = [0]*2
    if self.get_lock_state() != 0:
      return -1
    self.data_threshold_analysis(value ,rslt)
    self.write_reg(T_CRIT_REGISTER ,rslt)
    return 0

  '''
    @brief 清空中断，只使用于中断模式下，其余模式没有效果
  '''
  def clear_interrupt(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    rslt[1] &= 0xDF
    rslt[1] |= 0x20
    self.write_reg(CONFIG_REGISTER ,rslt)

  '''
    @brief 阈值解析
  '''
  def data_threshold_analysis(self ,value ,data):
    symbol = 0
    decimals = 0
    integet = 0
    if value < 0.00001:
      symbol = 1
      value *= -1
    decimals = self.parsing_decimal(value)
    integer = int(value)
    data[0] |= symbol<<4
    data[0] |= integer>>4
    data[1] |= ((integer&0x0F)<<4)
    data[1] |= decimals

  '''
    @brief 小数位解析
  '''  
  def parsing_decimal(self ,value):
    decimals = int(value*100) - (int(value))*100
    if decimals == 0:
      return 0x00
    elif decimals > 0 and decimals <= 25:
      return 0x04
    elif decimals > 25 and decimals <= 50:
      return 0x08
    else:
      return 0x0C

'''
  @brief An example of an i2c interface module
'''
class DFRobot_MCP9808_I2C(DFRobot_MCP9808):
  def __init__(self ,bus ,addr):
    self.__addr = addr
    super(DFRobot_MCP9808_I2C, self).__init__(bus)

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
    while 1:
      try:
        self.i2cbus.write_i2c_block_data(self.__addr ,reg ,data)
        return
      except:
        print("please check connect!")
        #os.system('i2cdetect -y 1')
        time.sleep(1)
        return
  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg ,len):
    try:
      rslt = self.i2cbus.read_i2c_block_data(self.__addr ,reg ,len)
      #print rslt
    except:
      rslt = -1
    return rslt