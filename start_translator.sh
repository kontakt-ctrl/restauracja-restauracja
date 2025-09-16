#!/bin/bash
# Skrypt uruchamiający oba ekrany restauracji z Kivy/Multi-monitor Raspberry Pi
# Wersja: 2024-09-01
# Autor: Copilot Space

# 1. Aktywacja wirtualnego środowiska
source /home/restauracja/restauracja/venv/bin/activate

# 2. Wykrycie monitorów HDMI
MONITORS=$(xrandr | grep " connected" | awk '{print $1}' | grep HDMI)
MON1=$(echo $MONITORS | awk '{print $1}')
MON2=$(echo $MONITORS | awk '{print $2}')

if [ -z "$MON1" ] || [ -z "$MON2" ]; then
    echo "$(date) - Nie wykryto dwóch monitorów HDMI. Sprawdź połączenia." > /home/restauracja/start.log 2>&1
    exit 1
fi
echo "$(date) - Monitor 1: $MON1 przypisany do EPOS IMPACT 60" >> /home/restauracja/start.log 2>&1
echo "$(date) - Monitor 2: $MON2 przypisany do ThinkVision T24v " >> /home/restauracja/start.log 2>&1

# 3. Obrót drugiego ekranu pionowo (jeśli wymagane)

xrandr --output $MON2 --rotate left

# 4. Ustawienie zmiennej środowiskowej dla Kivy/SDL i unikalnych tytułów okien
export KIVY_NO_ARGS=1

# 5. Uruchomienie aplikacji na obu monitorach
INSTANCE=A SDL_VIDEO_FULLSCREEN_HEAD=0 python /home/restauracja/restauracja/pi_voice_translator_tablet.py >> /home/restauracja/translatorA.log 2>&1 &
PID_A=$!
sleep 2
INSTANCE=B SDL_VIDEO_FULLSCREEN_HEAD=1 python /home/restauracja/restauracja/pi_voice_translator_tablet.py >> /home/restauracja/translatorB.log 2>&1 &
PID_B=$!
sleep 4

# 6. Ustawianie okien na wierzchu za pomocą wmctrl (jeśli dostępne)
which wmctrl >/dev/null 2>&1
if [ $? -eq 0 ]; then
    wmctrl -r "Translator Restauracja A" -b add,above
    wmctrl -r "Translator Restauracja B" -b add,above
    wmctrl -a "Translator Restauracja A"
    wmctrl -a "Translator Restauracja B"
fi

# 7. Monitoring logów
echo "$(date) - Uruchomiono TranslatorA (PID $PID_A) oraz TranslatorB (PID $PID_B)" >> /home/restauracja/start.log 2>&1

# 8. (Opcjonalnie) monitoring Raspberry Pi
nohup /home/restauracja/restauracja/raspberry-info.sh &

exit 0
