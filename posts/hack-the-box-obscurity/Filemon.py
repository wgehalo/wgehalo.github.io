import os
import shutil
import winsound

highlights_temp_folder = 'C:\\highlights_temp\\Escape From Tarkov'
beep_frequency_hz = 750
beep_duration_ms = 80

def alert():
    winsound.Beep(beep_frequency_hz, beep_duration_ms)
    winsound.Beep(beep_frequency_hz + 200, beep_duration_ms)

#Get initial count
files = os.listdir(highlights_temp_folder)
old_count = len(files)

while True:
    files = os.listdir(highlights_temp_folder)
    new_count = len(files)

    if new_count > old_count:
        alert()

    old_count = new_count