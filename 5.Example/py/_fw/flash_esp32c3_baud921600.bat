@echo off
reg query "HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\SERIALCOMM"
echo "[please enter COM No]"
set /p comno=
echo "[erase flash]"
python -m esptool --chip esp32-C3 --port COM%comno% erase_flash
echo "[write fireware]"
python -m esptool --chip esp32-C3 --port COM%comno% --baud 921600 write_flash -z 0x0 esp32c3-20220618-v1.19.1.bin
echo "[fireware info]"
python -m esptool --chip esp32-c3 --port COM%comno% flash_id
echo "[press any key to exit]"
pause
