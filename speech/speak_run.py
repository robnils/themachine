from time import sleep

from speech.speak import Speak

s = Speak()
s.start()

index = 0
while True:
    if index % 10 == 0:
        print "Still listening..."
    sleep(0.1)
    index += 1