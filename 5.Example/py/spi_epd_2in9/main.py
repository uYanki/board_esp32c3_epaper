from epd2in9d import EPD_2IN9_D

if __name__ == '__main__':
    epd = EPD_2IN9_D()
    epd.Clear(0x00)

    epd.fill(0xff)
    epd.text("Waveshare", 5, 10, 0x00)
    epd.text("ePaper-2.9-D", 5, 40, 0x00)
    epd.text("Raspberry Pico", 5, 70, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(3000)

    epd.vline(10, 90, 60, 0x00)
    epd.vline(120, 90, 60, 0x00)
    epd.hline(10, 90, 110, 0x00)
    epd.hline(10, 150, 110, 0x00)
    epd.line(10, 90, 120, 150, 0x00)
    epd.line(120, 90, 10, 150, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(3000)

    epd.rect(10, 180, 50, 80, 0x00)
    epd.fill_rect(70, 180, 50, 80, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(3000)

    for i in range(0, 10):
        epd.fill_rect(40, 270, 40, 10, 0xff)
        epd.text(str(i), 60, 270, 0x00)
        epd.display_Partial(epd.buffer)
        epd.delay_ms(500)

    epd.Clear(0x00)
    epd.delay_ms(2000)
    epd.sleep()
