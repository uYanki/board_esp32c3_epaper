from epdconfig import *

from machine import Pin, SPI
import framebuf
import utime

# Display resolution
EPD_WIDTH = 400
EPD_HEIGHT = 300

# for imageblack
COLOR1_FULL_WHITE = const(0xFF)
COLOR1_FULL_BLACK = const(0x00)

# for imagered
COLOR2_FULL_WHITE = const(0x00)
COLOR2_FULL_RED = const(0xFF)


class EPD_4in2_B:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)

        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

        self.spi = SPI(SPI_NUM, baudrate=4_000_000, phase=0, polarity=0, mosi=Pin(MOSI_PIN), sck=Pin(SCLK_PIN))
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)

        self.EPD_4IN2B_Init()
        self.EPD_4IN2B_Clear()
        utime.sleep_ms(500)

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(200)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(200)

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)

    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        print("e-Paper busy")
        while (self.digital_read(self.busy_pin) == 0):  # LOW: idle, HIGH: busy
            self.send_command(0x71)
        self.delay_ms(100)
        print("e-Paper busy release")

    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.delay_ms(100)
        self.ReadBusy()

    def EPD_4IN2B_Init(self):
        self.reset()

        self.send_command(0x04)  # POWER_ON
        self.ReadBusy()

        self.send_command(0x00)  # panel setting
        self.send_data(0x0f)

    def EPD_4IN2B_Clear(self):
        high = self.height
        if (self.width % 8 == 0):
            wide = self.width // 8
        else:
            wide = self.width // 8 + 1

        self.send_command(0x10)
        self.send_data1([COLOR1_FULL_WHITE] * high * wide)

        self.send_command(0x13)
        self.send_data1([COLOR2_FULL_WHITE] * high * wide)

        self.send_command(0x12)
        self.delay_ms(10)
        self.TurnOnDisplay()

    def EPD_4IN2B_Display(self, blackImage, redImage):
        high = self.height
        if (self.width % 8 == 0):
            wide = self.width // 8
        else:
            wide = self.width // 8 + 1

        self.send_command(0x10)
        self.send_data1(blackImage)

        self.send_command(0x13)
        self.send_data1(redImage)

        self.TurnOnDisplay()

    def Sleep(self):
        self.send_command(0X50)
        self.send_data(0xf7)     # border floating

        self.send_command(0X02)  # power off
        self.ReadBusy()          # waiting for the electronic paper IC to release the idle signal
        self.send_command(0X07)  # deep sleep
        self.send_data(0xA5)


def epd_test():

    # 红色部分有点

    epd = EPD_4in2_B()

    epd.imageblack.fill(COLOR1_FULL_WHITE)  # white
    epd.imagered.fill(COLOR2_FULL_WHITE)  # white

    epd.imageblack.text("1234", 5, 10, COLOR1_FULL_BLACK)  # black
    epd.imagered.text("1234", 5, 30, COLOR2_FULL_RED)  # red

    epd.imageblack.fill_rect(10, 45, 40, 20, COLOR1_FULL_BLACK)
    epd.imageblack.text("1234", 15, 50, COLOR1_FULL_WHITE)  # white
    epd.imagered.fill_rect(10, 75, 40, 20, COLOR2_FULL_RED)
    epd.imagered.text("1234", 15, 80, COLOR2_FULL_WHITE)  # white

    epd.EPD_4IN2B_Display(epd.buffer_black, epd.buffer_red)
    epd.delay_ms(2000)

    epd.Sleep()
