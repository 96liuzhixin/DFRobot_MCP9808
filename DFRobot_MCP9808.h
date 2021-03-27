/*!
 * @file DFRobot_MCP9808.h
 * @brief Define the basic structure of class DFRobot_MCP9808
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author      ZhixinLiu(zhixin.liu@dfrobot.com)
 * @version  V1.0
 * @date  2021-3-24
 * @get from https://www.dfrobot.com
 * @url https://www.dfrobot.com
 */
#ifndef __DFROBOT_MCP9808_H__
#define __DFROBOT_MCP9808_H__
#include <Arduino.h>
#include <Wire.h>

//#define ENABLE_DBG
//#define NORMAL_ENABLE

#ifdef ENABLE_DBG
  #ifdef NORMAL_ENABLE
    #define DBG(...) {Serial.println(__VA_ARGS__);}
  #else
    #define DBG(...) {Serial.print("[");Serial.print(__FUNCTION__); Serial.print("(): "); Serial.print(__LINE__); Serial.print(" ] "); Serial.println(__VA_ARGS__);}
  #endif
#else
  #define DBG(...)
#endif

#define I2C_ADDRESS_REGISTER    (0x00)

#define FRU_REGISTER            (0x00 & 0x0F)
#define CONFIG_REGISTER         (0x01 & 0x0F)
#define T_UPPER_REGISTER        (0x02 & 0x0F)
#define T_LOWER_REGISTER        (0x03 & 0x0F)
#define T_CRIT_REGISTER         (0x04 & 0x0F)
#define TEMPERATURE_REGISTER    (0x05 & 0x0F)
#define MANUFACTURER_REGISTER   (0x06 & 0x0F)
#define DEVICE_REGISTER         (0x07 & 0x0F)
#define RESOLUTION_REGISTER     (0x08 & 0x0F)

#define MANUFACTURER_ID         (0x54)
#define DEVICE_ID               (0x04)

#define CRIT_0_UPPER_0_LOWER_0  (0x00 << 5)
#define CRIT_0_UPPER_0_LOWER_1  (0x01 << 5)
#define CRIT_0_UPPER_1_LOWER_0  (0x02 << 5)
#define CRIT_0_UPPER_1_LOWER_1  (0x03 << 5)
#define CRIT_1_UPPER_0_LOWER_0  (0x04 << 5)
#define CRIT_1_UPPER_0_LOWER_1  (0x05 << 5)
#define CRIT_1_UPPER_1_LOWER_0  (0x06 << 5)
#define CRIT_1_UPPER_1_LOWER_1  (0x07 << 5)

#define RESOLUTION_0_5          (0x00 & 0x03)
#define RESOLUTION_0_25         (0x01 & 0x03)
#define RESOLUTION_0_125        (0x02 & 0x03)
#define RESOLUTION_0_0625       (0x03 & 0x03)          // default resolutivn

#define COMPARATOR_OUTPUT_MODE  0x00                   // default comparator mode
#define INTERRPUT_OUTPUT_MODE   0x01

#define CRIT_LOCK               0x80
#define WIN_LOCK                0x40
#define CRIT_WIN_LOCK           0xC0
#define NO_LOCK                 0x00                   // default no lock

#define POWER_UP_MODE           0x00                   // dafault power up
#define LOW_POWER_MODE          0x01

#define HYSTERESIS_0_0          0x00                   // default hysteresis
#define HYSTERESIS_1_5          0x02
#define HYSTERESIS_3_0          0x04
#define HYSTERESIS_6_0          0x06

#define POLARITY_HIGH           0x02
#define POLARITY_LOW            0x00                   // default active low

#define ENABLE_ALERT            0x08
#define DISABLE_ALERT           0x00                   // default disable

#define ONLY_CRIT_RESPONSE          0x40
#define UPPER_LOWER_CRIT_RESPONSE   0x00               // dafault output mode


class DFRobot_MCP9808{
public:
  DFRobot_MCP9808(){};
  ~DFRobot_MCP9808(){};

  /**
   * @brief 初始化传感器，对比传感器的芯片id 和 厂商 id
     @return state
                true  is init successfully
                flase is 芯片id或者厂商id错误
   */
  bool sensorInit(void);

  /**
   * @brief 设置温度传感器的分辨率，不同的分辨率，获取的温度的精度不同
   * @param resolution
                RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
                RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
                RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
                RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
     @return true is set successfully
             false is set parameter error
   */
  bool setResolution(uint8_t resolution);

  /**
   * @brief 获取温度传感器的分辨率 ,不同的分辨率，获取的温度的精度不同
   * @return resolution
                RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
                RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
                RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
                RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
   */
  uint8_t getResolution(void);

  /**
   * @brief 获取当前的环境温度，注意设置不同分辨率能够得到的温度精度不同
   * @return 温度值为浮点数，默认保留两位小数，单位为 ℃
   */
  float getTemperature(void);

  /**
   * @brief 获取当前比较器的状态，只有在比较器模式下有效
            比较器模式是比较当前温度和上限阈值，下限阈值，和临界值的关系
   * @return state
                TA 代表当前温度，TCRIT代表临界温度，TUPPER代表上限温度，TLOWER代表下限温度
                CRIT_0_UPPER_0_LOWER_0    // TA < TCRIT、TA ≤ TUPPER、TA ≥ TLOWER
                CRIT_0_UPPER_0_LOWER_1    // TA < TCRIT、TA ≤ TUPPER、TA < TLOWER
                CRIT_0_UPPER_1_LOWER_0    // TA < TCRIT、TA > TUPPER、TA ≥ TLOWER
                CRIT_0_UPPER_1_LOWER_1    // TA < TCRIT、TA > TUPPER、TA < TLOWER
                CRIT_1_UPPER_0_LOWER_0    // TA ≥ TCRIT、TA ≤ TUPPER、TA ≥ TLOWER
                CRIT_1_UPPER_0_LOWER_1    // TA ≥ TCRIT、TA ≤ TUPPER、TA < TLOWER
                CRIT_1_UPPER_1_LOWER_0    // TA ≥ TCRIT、TA > TUPPER、TA ≥ TLOWER
                CRIT_1_UPPER_1_LOWER_1    // TA ≥ TCRIT、TA > TUPPER、TA < TLOWER
   */
  uint8_t getComparatorState(void);

  /**
   * @brief 设置锁定模式或解锁，防止错误操作更改上限、下限、临界值的大小，锁定后只能通过断电复位解除锁定
   * @param lock
                CRIT_LOCK       // 锁定临界值，临界值的阈值不允许被修改
                WIN_LOCK        // 锁定上限下限，上限下限的阈值不允许被修改
                CRIT_WIN_LOCK   // 锁定临界值和上限下限，上限下限和临界值的数据都不允许被修改
                NO_LOCK         // 不锁定上限下限和临界值
     @return state
                true  is set successfully
                false is set parameter error
   */
  bool setLockState(uint8_t lock);

  /**
   * @brief 获取锁定的状态，来判断是否可以修改上限下限和临界值的阈值
   * @return state
                CRIT_LOCK       // 临界值锁定，临界值的阈值不允许被修改
                WIN_LOCK        // 上限下限锁定，上限下限的阈值不允许被修改
                CRIT_WIN_LOCK   // 临界值和窗口同时锁定，上限下限和临界值的数据都不允许被修改
                NO_LOCK         // 没有锁定，上限下限和临界值的阈值都可以被修改
   */
  uint8_t getLockState(void);

  /**
   * @brief 设置电源模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                          低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
   * @param mode
                POWER_UP_MODE         // 上电模式
                LOW_POWER_MODE        // 低功耗模式
   * @return 0x00 is set success
             0xFE is parameter error
             0xFF is register lock is not allowed to be modified
   */
  uint8_t setPowerMode(uint8_t mode);

  /**
   * @brief 获取电源的配置模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                                低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
   * @return mode
                POWER_UP_MODE         // 上电模式
                LOW_POWER_MODE        // 低功耗模式
   */
  uint8_t getPowerMode(void);

  /**
   * @brief 设置报警温度滞后的范围，在上限下限和临界值的阈值上增加一个范围,滞后功能仅适用于降温（从热至冷）
            ,也就是说（上限/下限/临界值）减去滞后温度，ALE电平才恢复
            例如:温度上限为30.0度，滞后温度为+1.5度，当前是35度ALE已经产生电平翻转，
            要想ALE恢复电平，必须达到30-1.5（28.5）度，ALE引脚才能恢复电平
   * @param mode
                HYSTERESIS_0_0        // 没有滞后，就是到达指定温度就响应
                HYSTERESIS_1_5        // 从热至冷要滞后1.5℃
                HYSTERESIS_3_0        // 从热至冷要滞后3.0℃
                HYSTERESIS_6_0        // 从热至冷要滞后6.0℃
     @return state
                0x00 is set successfully
                0xFE is set parameter error
                0xFF is register lock is not allowed to be modified
   */
  uint8_t setAlertHysteresis(uint8_t mode);

  /**
   * @brief 获取滞后的温度
   * @return hysteresis
                HYSTERESIS_0_0        // 温度滞后范围为 +0.0℃
                HYSTERESIS_1_5        // 温度滞后范围为 +1.5℃
                HYSTERESIS_3_0        // 温度滞后范围为 +3.0℃
                HYSTERESIS_6_0        // 温度滞后范围为 +6.0℃
   */
  uint8_t getAlertHysteresis(void);

  /**
   * @brief 使能或者禁止报警模式，使能报警模式后，ALE引脚到达报警条件后会产生跳变，禁止报警模式ALE引脚没有响应
   * @param mode
                ENABLE_ALERT           // 使能报警模式，ALE引脚到达报警条件后会产生跳变
                DISABLE_ALERT          // 禁止报警模式，禁止报警模式ALE引脚没有响应
     @return state
                0x00 is set successfully
                0xFE is set parameter error
                0xFF is register lock is not allowed to be modified
   */
  uint8_t setAlertEnable(uint8_t mode);

  /**
   * @brief 获取报警模式状态，得到时报警模式或者非报警模式
   * @return mode
                ENABLE_ALERT           // 报警模式
                DISABLE_ALERT          // 非报警模式
   */
  uint8_t getAlertEnableState(void);

  /**
   * @brief 设置ALE引脚的极性，引脚极性为高：ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
                               引脚极性为低：ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
   * @param polarity
                POLARITY_HIGH         // ALE引脚高电平为活动电平
                POLARITY_LOW          // ALE引脚低极性为活动电平
     @return state
                0x00 is set successfully
                0xFE is set parameter error
                0xFF is register lock is not allowed to be modified
   */
  uint8_t setPolarity(uint8_t polarity);
  
  /**
   * @brief 获取ALE引脚的极性状态，引脚极性为高：ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
                                   引脚极性为低：ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
   * @return polarity
                POLARITY_HIGH         // ALE引脚高电平为活动电平
                POLARITY_LOW          // ALE引脚低极性为活动电平
   */
  uint8_t getPolarityState(void);

  /**
   * @brief 设置警报输出的模式，比较器输出模式不需要清除中断，中断模式需要清除中断
   * @param mode
                COMPARATOR_OUTPUT_MODE           // 比较器输出模式不需要清除中断，
                例如：使能了报警模式，设置ALE引脚为低电平活动
                当超过上限警报的温度时，ALE引脚从高电平到低电平，当温度低于上限但高于下限时，ALE引脚恢复高电平
                INTERRPUT_OUTPUT_MODE            // 中断输出模式需要清除中断，当产生警报时，如果不清除中断中断一直存在，中断模式的触发，是从一种状态变为另一种状态，
                例如：设置了下限阈值20度，上限阈值25度，临界阈值30度，当温度一直低于20度时不产生中断，当温度超过25度时才产生中断，ALE引脚跳变，此时应该清空中断，ALE引脚恢复，特殊情况，当ALE引脚大于临界温度30度时，中断模式失效，清空中断也失效，必须等温度降到30度以下，才恢复中断模式
     @return state
                0x00 is set successfully
                0xFE is set parameter error
                0xFF is register lock is not allowed to be modified
   */
  uint8_t setAlertOutputMode(uint8_t mode);

  /**
   * @brief 获取警报输出的模式
   * @return mode
                COMPARATOR_OUTPUT_MODE           // 比较器输出模式
                INTERRPUT_OUTPUT_MODE            // 中断输出模式
   */
  uint8_t getAlertOutputMode(void);

  /**
   * @brief 设置响应模式，响应上限下限和临界值，或者只响应临界值，只响应临界值不适用于中断模式
   * @param mode
                UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应，
                ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
     @return state
                0x00 is set successfully
                0xFE is set parameter error
                0xFF is register lock is not allowed to be modified
   */
  uint8_t setAlertResponseMode(uint8_t mode);

  /**
   * @brief 获取中断响应的模式
   * @return mode
                UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应
                ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
   */
  uint8_t getAlertResponseMode(void);

  /**
   * @brief 设置上限和下限阈值,根据配置的中断模式响应，高于上限温度和低于下限温度响应
   * @param upper
              // 温度上限，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
   * @param lower
              // 温度下限，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
   * @return state
                0x00 is set successfully
                0xFE  // 温度上限小于下限，或者（上限温度-下限温度 < 2 ）
                0xFF is register lock is not allowed to be modified
   */
  uint8_t setUpperLowerThreshold(float upper ,float lower);

  /**
   * @brief 设置温度临界值,根据配置的中断模式响应，这里的临界值温度必须大于上限温度
   * @param value
              // 温度的临界值，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
   * @return state
                true  is set successfully
                false is register lock is not allowed to be modified
   */
  bool setCritThreshold(float value);

  /**
   * @brief 清空中断，只使用于中断模式下，其余模式没有效果
   */
  void clearInterrupt(void);

protected:
  /**
   * @brief 解析浮点数，用于设置上限下限临界值的浮点数部分
   * @return 二进制的浮点数
   */
  uint8_t parsingDecimal(float value);

  /**
   * @brief get manufacturer id
   * @return manufacturer id
                true               // manufacturer id is true
                false              // manufacturer id is false
   */
  bool getManufacturerID(void);

  /**
   * @brief get device id
   * @return device id
                true               // device id is true
                false              // device id is false
   */
  bool getDeviceID(void);

  /**
   * @brief 解析阈值的整数部分，放到指定位置
   * @param value 要放的阈值数据
   * @param data  要放到的地址
   */
  void dataThreshold(float value ,uint8_t *data);
  
  virtual uint8_t readData (uint8_t Reg ,uint8_t *Data ,uint8_t len)=0;
  virtual void    writeData(uint8_t Reg ,uint8_t *Data ,uint8_t len)=0;
};

class DFRobot_MCP9808_I2C:public DFRobot_MCP9808{
public:
  DFRobot_MCP9808_I2C(TwoWire *pWire=&Wire ,uint8_t addr=0x30);
  ~DFRobot_MCP9808_I2C(){};
  void writeData(uint8_t Reg,uint8_t *Data,uint8_t len);
  uint8_t readData(uint8_t Reg,uint8_t *Data,uint8_t len);
  uint8_t begin();
private:
  TwoWire *_pWire;
  uint8_t _I2C_addr;
};
#endif