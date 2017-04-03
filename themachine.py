from __future__ import unicode_literals, print_function

import datetime
import uuid
from threading import Thread
from time import sleep

import cv2
from facial.face import Initialise, Camera, Display, Data
from speech.speak import Speak


class Runner:

    def __init__(self, display, communicate):
        self.display = display
        self.communicate = communicate

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
                self.communicate.process_cqueue = False
                break

    def run(self):
        self.communicate.start()
        self.main_loop()


class Queue:
    timeout = {}

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def timeout_reached(self, item):
        return datetime.datetime.now() >= Queue.timeout[item]

    def enqueue(self, item, timeout=0.0):
        if item not in Queue.timeout or self.timeout_reached(item):
            self.items.insert(0, item)
            Queue.timeout[item] = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    def dequeue(self):
        elem = self.items.pop()
        # todo need?
        #if self.timeout_reached(elem):
        #    Queue.timeout.pop(elem, None)
        return elem

    def size(self):
        return len(self.items)


class Communicate(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.process_cqueue = True

    def run(self):
        speak = Speak()
        sleep(1.0)
        while self.process_cqueue:

            if not self.queue.isEmpty():
                string = self.queue.dequeue()
                speak.speak(string)
        print('Communication stopped')

if __name__ == '__main__':
    known = "./data/known/"
    init = Initialise()

    talk_queue = Queue()
    talk_queue.enqueue("Hi")
    talk_queue.enqueue("I am the Machine.")
    communicate = Communicate(talk_queue)

    camera = Camera()
    camera.start()
    display = Display(camera, talk_queue)
    Runner(display, communicate).run()

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

