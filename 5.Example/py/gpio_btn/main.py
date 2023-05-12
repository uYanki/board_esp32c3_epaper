PIN_KEY1 = const(1)
PIN_KEY2 = const(2)
PIN_KEY3 = const(9)  # boot

if 0:

    from machine import Pin

    key1 = Pin(PIN_KEY1, Pin.IN, Pin.PULL_UP)
    key1.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: print(pin))

    key2 = Pin(PIN_KEY2, Pin.IN, Pin.PULL_UP)
    key2.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: print(pin))

    key3 = Pin(PIN_KEY3, Pin.IN, Pin.PULL_UP)
    key3.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: print(pin))

else:

    from button import button  # 推荐

    button(PIN_KEY1, callback=lambda pin: print("a", pin))
    button(PIN_KEY2, callback=lambda pin: print("b", pin))
    button(PIN_KEY3, callback=lambda pin: print("c", pin))
