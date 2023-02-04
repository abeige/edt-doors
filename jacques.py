from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

buzzer = TonalBuzzer(pin=17, mid_tone="C7", octaves=1)
notes=[262,294,330,262,262,294,330,262,330,349,392,330,349,392,392,440,392,349,330,262,392,440,392,349,330,262,262,196,262,262,196,262]
duration=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.5,0.5,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,1,0.5,0.5,1]

print("buzzer min max:", buzzer.min_tone, buzzer.max_tone)
print("song min max:", Tone(min(notes)), Tone(max(notes)))

for n, d in zip(notes, duration):
    d = d/2
    tone = Tone(n)
    buzzer.play(tone.up(35)) # D6 24 up
    sleep(d)
    buzzer.stop()
    sleep(d * 0.1)
