
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

buzzer = TonalBuzzer(pin=17, mid_tone="C5", octaves=1)

# letters = "deggbagaaggabbdcbccdbbcdedcabcdcbgfgbafg" # f should be f#
# letters = [l.upper()+"5" for l in letters]

# noteDuration = "hhqqqhhqqqhhqqqhhqhhqhhqhhqhhqhhqhhqqqqq"
# new = []
# for n in note_type:
#     if n == "h":
#         new.append(0.5)
#     if n == "q":
#         new.append(1)
# print(new)

notes = ['D5', 'E5', 'G5', 'G5', 'B5', 'A5', 'G5', 'A5', 'A5', 'G5', 'G5', 'A5', 'B5', 'B5', 'D6', 'C6', 'B5', 'C6', 'C6', 'D6', 'B5', 'B5', 'C6', 'D6', 'E6', 'D6', 'C6', 'A5', 'B5', 'C6', 'D6', 'C6', 'B5', 'G5', 'F#5', 'G5', 'B5', 'A5', 'F#5', 'G5']
duration = [0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 1, 1, 1, 2]

for n, d in zip(notes, duration):
    d = d/3
    tone = Tone(n)
    buzzer.play(tone.down(8)) # D6 24 up
    sleep(d)
    buzzer.stop()
    sleep(d * 0.1)
