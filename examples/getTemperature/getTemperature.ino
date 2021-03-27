 /*!
  * @file  getTemperature.ino
  * @brief 普通获取温度的例子
  * @n 实验现象：温度在串口显示，测量温度随环境温度改变而改变
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
  uint8_t state = 0;
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
    设置温度的分辨率
      RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
      RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
      RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
      RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
  */
  if(mcp9808.setResolution(RESOLUTION_0_25)){
    Serial.println("设置温度的分辨率成功!");
  }else{
    Serial.println("parameter error!");
  }

  /**
    设置电源模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                  低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
      POWER_UP_MODE         // 上电模式
      LOW_POWER_MODE        // 低功耗模式
  */
  if(mcp9808.setPowerMode(POWER_UP_MODE) == 0){
    Serial.println("设置电源模式成功！");
  }else{
    Serial.println("Register locked or parameter error!");
  }
}

void loop()
{
  Serial.print("Temperature is ="); 
  Serial.print(mcp9808.getTemperature());
  Serial.println(" C");
  delay(1000);
}