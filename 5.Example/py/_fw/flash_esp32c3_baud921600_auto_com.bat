@echo off
echo "[erase flash]"
python -m esptool --chip esp32-C3 erase_flash
echo "[write fireware]"
python -m esptool --chip esp32-C3 --baud 921600 write_flash -z 0x0 esp32c3-20220618-v1.19.1.bin
echo "[fireware info]"
python -m esptool --chip esp32-c3 flash_id
echo "[press any key to exit]"
pause
