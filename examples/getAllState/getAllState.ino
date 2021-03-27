 /*!
  * @file  getAllState.ino
  * @brief 获取所有的默认配置
  * @n 实验现象：传感器所有配置状态打印在串口
  * @n i2c 地址选择，默认i2c地址为0x1F，A2、A1、A0引脚为高电平
  * @n 1代表高电平，0代表低电平,8种组合为
  *               | A2 | A1 | A0 |
  *               | 0  | 0  | 0  |    0x18
  *               | 0  | 0  | 1  |    0x19
  *               | 0  | 1  | 0  |    0x1A
  *               | 0  | 1  | 1  |    0x1B
  *               | 1  | 0  | 0  |    0x1D
  *               | 1  | 0  | 1  |    0x1D
  *               | 1  | 1  | 0  |    0x1E
  *               | 1  | 1  | 1  |    0x1F   default i2c address
  *
  * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  * @licence     The MIT License (MIT)
  * @author      ZhixinLiu(zhixin.liu@dfrobot.com)
  * @version     V0.2
  * @date        2021-03-26
  * @get         from https://www.dfrobot.com
  * @url         https://www.dfrobot.com
  */
#include "DFRobot_MCP9808.h"
#define I2C_ADDRESS 0x1F
DFRobot_MCP9808_I2C mcp9808(&Wire ,I2C_ADDRESS);

void setup()
{
  Serial.begin(115200);
  while(mcp9808.begin() != 0){
    Serial.println("i2c device number error!");
    delay(1000);
  } Serial.println("i2c connect success!");

  while(!mcp9808.sensorInit()){
    Serial.println("初始化失败，请检查模块是否正确!");
    delay(100);
  } Serial.println("sensor init success!");

  /**
    获取温度的分辨率
      RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
      RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
      RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
      RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
  */
  switch(mcp9808.getResolution()){
    case RESOLUTION_0_5:
      Serial.println("分辨率：0.5");
      break;
    case RESOLUTION_0_25:
      Serial.println("分辨率：0.25");
      break;
    case RESOLUTION_0_125:
      Serial.println("分辨率：0.125");
      break;
    case RESOLUTION_0_0625:
      Serial.println("分辨率：0.0625");
      break;
    default:
      break;
  }

  /**
    获取锁定的状态，来判断是否可以修改上限下限和临界值的阈值
    锁定后只能通过断电复位解除锁定
      CRIT_LOCK       // 临界值锁定，临界值的阈值不允许被修改
      WIN_LOCK        // 上限下限锁定，上限下限的阈值不允许被修改
      CRIT_WIN_LOCK   // 临界值和窗口同时锁定，上限下限和临界值的数据都不允许被修改
      NO_LOCK         // 没有锁定，上限下限和临界值的阈值都可以被修改
  */
  switch(mcp9808.getLockState()){
    case CRIT_LOCK:
      Serial.println("锁定模式：临界值锁定");
      break;
    case WIN_LOCK:
      Serial.println("锁定模式：上限下限锁定");
      break;
    case CRIT_WIN_LOCK:
      Serial.println("锁定模式：临界值和窗口同时锁定");
      break;
    case NO_LOCK:
      Serial.println("锁定模式：没有锁定");
      break;
    default:
      break;
  }

  /**
   * @brief 获取电源的配置模式，上电模式和低功耗模式
       POWER_UP_MODE         // 上电模式，该模式下，可以正常访问寄存器，能够得到正常的温度
       LOW_POWER_MODE        // 低功耗模式，温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
  */
  switch(mcp9808.getPowerMode()){
    case POWER_UP_MODE:
      Serial.println("电源模式：上电模式");
      break;
    case LOW_POWER_MODE:
      Serial.println("电源模式：低功耗模式");
      break;
      break;
    default:
      break;
  }

  /**
    获取报警温度滞后的温度
    ,滞后功能仅适用于降温（从热至冷）,也就是说（上限/下限/临界值）减去滞后温度，ALE电平才恢复
      HYSTERESIS_0_0        // 温度滞后范围为 +0.0℃
      HYSTERESIS_1_5        // 温度滞后范围为 +1.5℃
      HYSTERESIS_3_0        // 温度滞后范围为 +3.0℃
      HYSTERESIS_6_0        // 温度滞后范围为 +6.0℃
  */
  switch(mcp9808.getAlertHysteresis())
  {
    case HYSTERESIS_0_0:
      Serial.println("温度滞后范围：+0.0 C");
      break;
    case HYSTERESIS_1_5:
      Serial.println("温度滞后范围：+1.5 C");
      break;
    case HYSTERESIS_3_0:
      Serial.println("温度滞后范围：+3.0 C");
      break;
    case HYSTERESIS_6_0:
      Serial.println("温度滞后范围：+6.0 C");
      break;
    default:
      break;
  }

  /**
    获取报警模式状态，得到时报警模式或者非报警模式
      ENABLE_ALERT           // 报警模式
      DISABLE_ALERT          // 非报警模式
  */
  switch(mcp9808.getAlertEnableState())
  {
    case ENABLE_ALERT:
      Serial.println("警报模式：报警模式");
      break;
    case DISABLE_ALERT:
      Serial.println("警报模式：非报警模式");
      break;
    default:
      break;
  }

  /**
    获取ALE引脚的极性
      POLARITY_HIGH         // ALE引脚高电平为活动电平
      POLARITY_LOW          // ALE引脚低极性为活动电平
  */
  switch(mcp9808.getPolarityState())
  {
    case POLARITY_HIGH:
      Serial.println("引脚极性：高极性");
      break;
    case POLARITY_LOW:
      Serial.println("引脚极性：低极性");
      break;
    default:
      break;
  }

  /**
    获取警报输出的模式
      COMPARATOR_OUTPUT_MODE           // 比较器输出模式
      INTERRPUT_OUTPUT_MODE            // 中断输出模式
   */
  switch(mcp9808.getAlertOutputMode())
  {
    case COMPARATOR_OUTPUT_MODE:
      Serial.println("输出模式：比较器输出");
      break;
    case INTERRPUT_OUTPUT_MODE:
      Serial.println("输出模式：中断输出");
      break;
    default:
      break;
  }

  /**
    获取中断响应的模式
      UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应
      ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
   */
  switch(mcp9808.getAlertResponseMode())
  {
    case UPPER_LOWER_CRIT_RESPONSE:
      Serial.println("响应模式：上限/下线和临界值响应");
      break;
    case ONLY_CRIT_RESPONSE:
      Serial.println("响应模式：临界值响应");
      break;
    default:
      break;
  }
}

void loop()
{
  delay(1000);
}