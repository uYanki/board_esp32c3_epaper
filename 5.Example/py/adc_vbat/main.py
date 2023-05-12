from machine import Pin, ADC

PIN_ADC_VBAT = const(0)

adc_vbat = ADC(Pin(PIN_ADC_VBAT))

# 不同输入衰减量的对应不同的电压测量范围

db_v = [  # 输入衰减 & 测量范围
    ADC.ATTN_0DB, 1.00,
    ADC.ATTN_2_5DB, 1.34,
    ADC.ATTN_6DB, 2.00,
    ADC.ATTN_11DB, 3.60
]

adc_vbat.width(ADC.WIDTH_12BIT)  # 精度

for idx in range(0, 8, 2):
    print("db:", db_v[idx], ", vol:", db_v[idx+1])
    adc_vbat.atten(db_v[idx])
    print(adc_vbat.read() / 4095 * db_v[idx+1])
    print(adc_vbat.read_u16() / 65535 * db_v[idx+1])
    print(adc_vbat.read_uv() / 1e6)
