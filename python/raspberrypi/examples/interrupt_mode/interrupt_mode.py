# -*- coding:utf-8 -*-
"""
  @file get_temperature.py
  @brief �жϻ�ȡ�¶ȵ����ӣ���ALE�������ӵ� BCM 25
  @n ʵ�������¶��ڴ�����ʾ�������¶��滷���¶ȸı���ı�
  @n ʵ�������ж�io����״̬ת��ʱ�����������¶������޺������м������һֱ�������޻���һֱ�������ޣ���ʱ���ᷢ���ж�
  @n ʵ�����󣺵��¶�״̬�ڵ������޵�״̬ʱ�ı䣬���������޴�ʱ�������ж���Ҫ����жϣ�
  @n ʵ����������жϺ�ALE���ŵ�ƽ�ָ��������ٽ�ֵʱ����ж�ʧЧ��ALE���ŵ�ƽ���ָ���
  @n i2c ��ַѡ��Ĭ��i2c��ַΪ0x1F��A2��A1��A0����Ϊ�ߵ�ƽ��
  @n ��8�����Ϊ,1�����ߵ�ƽ��0�����͵�ƽ
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

I2C_1       = 0x01               # I2C_1 ʹ��i2c1�ӿ������������� ���Ե���Ϊi2c0������Ҫ������ݮ�ɵ��ļ�
I2C_ADDRESS = 0x1F               # I2C �豸�ĵ�ַ�����Ը���A2��A1��A0��������ַ��Ĭ�ϵ�ַΪ0x1F
tmp = DFRobot_MCP9808_I2C(I2C_1 ,I2C_ADDRESS)
global interrupt_state
interrupt_state = 0

'''
  io���жϺ�������25�����Ŵ����жϽ��뺯��
  ����¶�����������ж�
'''
def my_interrupt(channel):
  global interrupt_state
  interrupt_state = 1

def setup():
  GPIO.setmode(GPIO.BCM)
  '''
    �������ŵ�ģʽ������Ϊ����ģʽ��
      pull_up_down=GPIO.PUD_DOWN   ��ALE��������Ϊ�߼���ʱ��BCM 25����������Ϊ��������
      pull_up_down=GPIO.PUD_UP     ��ALE��������Ϊ�ͼ���ʱ��BCM 25����������Ϊ��������
    
  '''
  GPIO.setup(25 ,GPIO.IN ,pull_up_down=GPIO.PUD_UP)
  
  '''
    �������ŵ��ж�ģʽ��ALE���ż���Ϊ��ѡ���������ж�
                        ALE���ż���Ϊ��ѡ���½����ж�
      GPIO.RISING     // �������ж�
      GPIO.FALLING    // �½����ж�
  '''
  GPIO.add_event_detect(25, GPIO.FALLING, callback=my_interrupt, bouncetime=500)

  while ERROR == tmp.sensor_init():
    print "sensor init error ,please check connect or device id or manufacturer id error"
  print "sensor init success"
  '''
    �����¶ȴ������ķֱ��ʣ���ͬ�ķֱ��ʣ���ȡ���¶ȵľ��Ȳ�ͬ
    resolution
            RESOLUTION_0_5     // ��ȡ�¶ȵ�С������Ϊ0.5�ı���     ��0.5�� ��1.0�桢1.5��
            RESOLUTION_0_25    // ��ȡ�¶ȵ�С������Ϊ0.25�ı���    ��0.25�桢0.50�桢0.75��
            RESOLUTION_0_125   // ��ȡ�¶ȵ�С������Ϊ0.125�ı���   ��0.125�桢0.250�桢0.375��
            RESOLUTION_0_0625  // ��ȡ�¶ȵ�С������Ϊ0.0625�ı���  ��0.0625�桢0.1250�桢0.1875��
  '''
  if 0 == tmp.set_resolution(RESOLUTION_0_25):
    print "Resolution set successfully"
  else:
    print "parameter error"

  '''
    ���õ�Դģʽ���ϵ�ģʽ����ģʽ�£������������ʼĴ������ܹ��õ��������¶ȣ�
                  �͹���ģʽ���¶Ȳ���ֹͣ�����Զ�ȡ��д��Ĵ������������߻��ʹ�ĵ�����
      POWER_UP_MODE         // �ϵ�ģʽ
      LOW_POWER_MODE        // �͹���ģʽ
  '''
  if 0 == tmp.set_power_mode(POWER_UP_MODE):
    print "Power mode was set successfully"
  else:
    print "Register lock" 
  
  '''
    ���þ��������ģʽ���Ƚ������ģʽ����Ҫ����жϣ��ж�ģʽ��Ҫ����ж�
      COMPARATOR_OUTPUT_MODE           // �Ƚ������ģʽ����Ҫ����жϣ��Ƚ�ģʽ�Ĵ����ǣ����¶ȸ������޻��¶ȵ������޻����¶ȳ����ٽ�ֵ
        ���磺ʹ���˱���ģʽ������ALE����Ϊ�͵�ƽ������������޾������¶�ʱ��
              ALE���ŴӸߵ�ƽ���͵�ƽ�����¶ȵ������޵���������ʱ��ALE���Żָ��ߵ�ƽ
      INTERRPUT_OUTPUT_MODE            // �ж����ģʽ��Ҫ����жϣ�����������ʱ���������ж��ж�һֱ���ڣ��ж�ģʽ�Ĵ������Ǵ�һ��״̬��Ϊ��һ��״̬
        ���磺������������ֵ20�ȣ�������ֵ25�ȣ��ٽ���ֵ30�ȣ����¶�һֱ����20��ʱ�������жϣ�
              ���¶ȳ���25��ʱ�Ų����жϣ�ALE�������䣬��ʱӦ������жϣ�ALE���Żָ������������
              ��ALE���Ŵ����ٽ��¶�30��ʱ���ж�ģʽʧЧ������ж�ҲʧЧ��������¶Ƚ���30�����£��Żָ��ж�ģʽ��
  '''
  if 0 == tmp.set_alert_output_mode(INTERRPUT_OUTPUT_MODE):
    print "The comparator mode was set successfully"
  else:
    print "Register lock or parameter error"

  '''
    ����ALE���ŵļ���
      POLARITY_HIGH         // ����ALE���Ÿߵ�ƽΪ���ƽ��Ĭ��Ϊ�͵�ƽ������������ALEΪ�ߵ�ƽ
      POLARITY_LOW          // ����ALE���ŵͼ���Ϊ���ƽ��Ĭ��Ϊ�ߵ�ƽ������������ALEΪ�͵�ƽ
  '''
  if 0 == tmp.set_polarity(POLARITY_LOW):
    print "Pin polarity set successfully"
  else:
    print "Register lock or parameter error"

  '''
    ������Ӧģʽ����Ӧ�������޺��ٽ�ֵ������ֻ��Ӧ�ٽ�ֵ��ֻ��Ӧ�ٽ�ֵ���������ж�ģʽ
      UPPER_LOWER_CRIT_RESPONSE         // ����/���ߺ��ٽ�ֵ ����Ӧ
      ONLY_CRIT_RESPONSE                // ��ֹ����������Ӧ��ֻ���ٽ�ֵ��Ӧ
  '''
  if 0 == tmp.set_alert_response_mode(UPPER_LOWER_CRIT_RESPONSE):
    print "Set response mode successfully"
  else:
    print "Register lock or parameter error"

  '''
    �������޺�������ֵ,�������õ��ж�ģʽ��Ӧ����������¶Ⱥ͵�������¶ȵ���Ӧ�������λС��
      upper
        // ���õ��¶����ޣ��Զ�������0.25�ı�������ΧΪ-40 �� +125��
      lower
        // ���õ��¶����ޣ��Զ�������0.25�ı�������ΧΪ-40 �� +125��
  '''
  if 0 == tmp.set_upper_lower_tereshold(32.5 ,20.5):
    print "Set upper limit threshold successfully"
  else:
    print "Failed to set upper limit because the upper limit of temperature is less than lower limit, or the upper limit and lower limit are less than two degrees or Register lock"
  
  '''
    �����¶��ٽ�ֵ,�������õ��ж�ģʽ��Ӧ��������ٽ�ֵ�¶ȱ�����������¶�
      value
        // �¶ȵ��ٽ�ֵ�������λС�����Զ�������0.25�ı�������ΧΪ-40 �� +125��
  '''
  state = tmp.set_crit_threshold(35.5)
  if 0 == state:
    print "Set the threshold value for success"
  else:
    print "Register lock"
  
  '''
    ���ñ����¶��ͺ�ķ�Χ�����������޺��ٽ�ֵ����ֵ������һ����Χ,�ͺ��ܽ������ڽ��£��������䣩,
    Ҳ����˵���޼�ȥ�ͺ��¶ȣ�ALE��ƽ�Żָ�
    ����:�¶�����Ϊ30.0�ȣ��ͺ��¶�Ϊ+1.5�ȣ���ǰ��35��ALE�Ѿ�������ƽ��ת��
         Ҫ��ALE�ָ���ƽ������ﵽ30-1.5��28.5���ȣ�ALE���Ų��ָܻ���ƽ
      HYSTERESIS_0_0        // û���ͺ󣬾��ǵ���ָ���¶Ⱦ���Ӧ
      HYSTERESIS_1_5        // ��������Ҫ�ͺ�1.5��
      HYSTERESIS_3_0        // ��������Ҫ�ͺ�3.0��
      HYSTERESIS_6_0        // ��������Ҫ�ͺ�6.0��
  '''
  if 0 == tmp.set_alert_hysteresis(HYSTERESIS_1_5):
    print "Set hysteresis temperature successfully"
  else:
    print "Register lock or parameter error"
  
  '''
    ʹ�ܻ��߽�ֹ����ģʽ��ʹ�ܱ���ģʽ��ALE���ŵ��ﱨ���������������䣬��ֹ����ģʽALE����û����Ӧ
      ENABLE_ALERT           // ʹ�ܱ���ģʽ��ALE���ŵ��ﱨ����������������
      DISABLE_ALERT          // ��ֹ����ģʽ����ֹ����ģʽALE����û����Ӧ
  '''
  if 0 == tmp.set_alert_enable(ENABLE_ALERT):
    print "To enable or inhibit success"
  else:
    print "Register lock or parameter error"
  
  '''
    ��������ģʽ�ͽ�������ֹ��������������ޡ����ޡ��ٽ�ֵ����ֵ�Ĵ�С
      CRIT_LOCK       // �����ٽ�ֵ���ٽ�ֵ����ֵ���������޸�
      WIN_LOCK        // �����������ޣ��������޵���ֵ���������޸�
      CRIT_WIN_LOCK   // �����ٽ�ֵ���������ޣ��������޺��ٽ�ֵ�����ݶ����������޸�
      NO_LOCK         // �������Ĵ���
  '''
  if 0 == tmp.set_lock_state(NO_LOCK):
    print "Unlocked or locked successfully"
  else:
    print "parameter error"
  
  tmp.clear_interrupt()     # ʹ�ܱ���ģʽ��������һ���ж�
  
def loop():
  global interrupt_state
  temperature = tmp.get_temperature()
  print "temperature = %.2f .C"%temperature
  print ""
  time.sleep(1)
  
  if interrupt_state == 1:
    interrupt_state = 0
    tmp.clear_interrupt()
    print "The temperature state has changed"

if __name__ == "__main__":
  setup()
  while True:
    loop()