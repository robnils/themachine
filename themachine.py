from __future__ import unicode_literals, print_function

import datetime
import cv2
from facial.face import Initialise, Camera, Display, Data


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
        self.main_loop()


if __name__ == '__main__':
    folder = "./data/known/"
    init = Initialise()
    tl, p = init.get_targets(folder)

    camera = Camera()
    camera.start()
    display = Display(camera, tl, p)
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

