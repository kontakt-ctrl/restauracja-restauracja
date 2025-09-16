#!/bin/bash
# Skrypt monitorujący Raspberry Pi: temperatura, CPU, RAM, dysk, zasilanie, uptime, IP, błędy
# Log: /home/pi/translator/log/raspberry-info.log

LOGFILE="/home/pi/translator/log/raspberry-info.log"
DATE="$(date '+%Y-%m-%d %H:%M:%S')"

# Temperatury CPU
TEMP_CPU="$(vcgencmd measure_temp 2>/dev/null | cut -d'=' -f2 || echo 'brak')"
RAW_TEMP="$(cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null)"
if [[ "$RAW_TEMP" =~ ^[0-9]+$ ]]; then
    TEMP_SYS="$(awk "BEGIN {print $RAW_TEMP/1000}")"
else
    TEMP_SYS="brak"
fi

# Obciążenie CPU, RAM, dysk
CPU_LOAD="$(top -bn1 | grep 'Cpu(s)' | awk '{print $2}')"
MEM_INFO="$(free -h | grep Mem | awk '{print $3 "/" $2}')"
DISK_INFO="$(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')"

# Uptime
UPTIME="$(uptime -p)"

# IP
IP_ADDR="$(hostname -I | awk '{print $1}')"

# Zasilanie/throttling
THROTTLED="$(vcgencmd get_throttled 2>/dev/null | tr -d '\n')"
if [[ "$THROTTLED" == "throttled=0x0" ]]; then
    THROTTLE_STATUS="OK"
else
    THROTTLE_STATUS="!!PROBLEM: $THROTTLED"
fi

# Ostatnie błędy systemowe
SYSLOG="$(sudo tail -n 10 /var/log/syslog 2>/dev/null | grep -i -E "error|fail|warn" | tail -n 3)"

# Zapis do logu
{
    echo "==== $DATE ===="
    echo "Temperatura CPU: $TEMP_CPU (sys: $TEMP_SYS°C)"
    echo "Obciążenie CPU: $CPU_LOAD%"
    echo "RAM: $MEM_INFO"
    echo "Dysk: $DISK_INFO"
    echo "Uptime: $UPTIME"
    echo "IP: $IP_ADDR"
    echo "Zasilanie/throttling: $THROTTLE_STATUS"
    echo "Błędy systemowe:"
    echo "$SYSLOG"
    echo ""
} >> "$LOGFILE"
