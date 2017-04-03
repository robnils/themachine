from __future__ import unicode_literals, print_function

import datetime
from threading import Thread
from time import sleep

import cv2
from facial.face import Initialise, Camera, Display, Data
from speech.speak import Speak


class Runner:

    def __init__(self, display):
        self.display = display

    def main_loop(self):
        process_this_frame = True
        while True:
            t1 = datetime.datetime.now()

            self.display.handle_frame()

            # process every second frame for performance improvements
            if process_this_frame:
                Data.result = self.display.calculate()
            process_this_frame = not process_this_frame

            if Data.result:
                for r in Data.result:
                    self.display.draw_identify(r)

            t2 = datetime.datetime.now()
            self.display.draw_fps(t1, t2)

            self.display.update()
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting...")
                # Release handle to the webcam
                self.display.camera.video_capture.release()
                cv2.destroyAllWindows()
                break

    def run(self):
        t = Communicate()
        t.start()
        self.main_loop()


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Communicate(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.talk_queue = Queue()
        self.talk_queue.enqueue("Hi")
        self.talk_queue.enqueue("I am the Machine.")

    def run(self):
        speak = Speak()
        sleep(2.0)
        while True:
            if not self.talk_queue.isEmpty():
                string = self.talk_queue.dequeue()
                speak.speak(string)
                sleep(0.5)


if __name__ == '__main__':
    known = "./data/known/"
    init = Initialise()

    camera = Camera()
    camera.start()
    display = Display(camera)
    Runner(display).run()

# todo calculate location and identification every other frame, first location, then encoding
# todo delay identification a few frames

# todo yml file per person which can be encrypted and retrieved easily

# TODO
# start with no data. introduce self.
# detect a face
# scan known faces
# if we have faces, check if there is a comparison. if there is, say "hi <person>".
# else take a screenshot of the person.
# ask their name.
# save their face in a yaml with their name as the filename.
# say "nice to meet you <person>".

