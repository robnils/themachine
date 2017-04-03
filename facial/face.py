from __future__ import unicode_literals, print_function
from enum import Enum
import datetime

import face_recognition
import cv2
import math
import os

import yaml

from speech import speak
from speech.speak import Speak


class Person:
    def __init__(self, name, image=None):
        self.name = name
        self.image = image


class YamlWrapper:

    def __init__(self, filename):
        self.filename = filename

    def read_data(self):
        try:
            with open(self.filename) as f:
                print('Reading: {}...'.format(self.filename), end='')
                print("Done!")
                data = yaml.load(f)
                if data:
                    return data
        except:
            pass
        return {}

    def write(self, data):
        with open(self.filename, 'w') as outfile:
            print('Saving: {}...'.format(self.filename), end='')
            yaml.dump(data, outfile, default_flow_style=False)
        print("Done!")


class Initialise:

    def __init__(self):
        pass

    def get_targets(self, folderpath):
        target_face_encoding_list = []
        persons = []
        data = YamlWrapper('data/targets.yml').read_data()

        if data:
            for target in data:
                target_face_encoding = data[target]['target_face_encoding']
                name = data[target]['name']
                target_face_encoding_list.append(target_face_encoding)

                persons.append(Person(name))
            print("Returning data")
            return target_face_encoding_list, persons

        print("Generating targets...")
        for file in os.listdir(folderpath):
            # todo partials are broken
            print("Encoding: {}".format(file))
            filepath = os.path.join(folderpath, file)

            # Initialise target - load image, HOG encode, append to list of targets
            target_image = face_recognition.load_image_file(filepath)
            target_face_encodings = face_recognition.face_encodings(target_image)
            assert len(target_face_encodings) == 1, "Error: multiple target faces detected, cannot decide which is target"
            target_face_encoding = target_face_encodings[0]
            target_face_encoding_list.append(target_face_encoding)

            name = os.path.splitext(file)[0]
            persons.append(Person(name))

            data[file] = {
                'target_face_encoding': target_face_encoding,
                'name': name,
            }

        YamlWrapper('targets.yml').write(data)
        return target_face_encoding_list, persons



class Colours(Enum):
    green = (0, 200, 0)
    red = (0, 0, 200)
    yellow = (0, 200, 200)
    black = (0, 0, 0)
    white = (255, 255, 255)


class Identification:

    @staticmethod
    def get_color(state='UNKNOWN', name=''):
        # todo move these defintions to a config somewhere
        # todo add non-name based identification
        persons = {
            'Rob':  {
                'colour': Colours.green,
                'text_color': Colours.white
            }
        }

        # Return person-specific colours if we recognise them
        if name:
            colours = persons.get(name, None)
            if colours:
                return colours

        default = {
            'UNKNOWN': {
                'colour': Colours.red,
                'text_color': Colours.white
            },
            'KNOWN': {
                'colour': Colours.yellow,
                'text_color': Colours.black
            }
        }
        assert state in ['UNKNOWN', 'KNOWN'], 'Invalid state given'
        return default[state]


class Display:

    def __init__(self, camera, talk_queue, target_face_encoding_list=None, persons=None):
        self.camera = camera
        self.frame = None

        self.talk_queue = talk_queue

        self.target_face_encoding_list = target_face_encoding_list or []
        self.persons = persons or []

        self.TOLERANCE = 0.6

    def identify(self, matches):
        name = "Unknown"
        color = (0, 0, 200)
        text_color = (255, 255, 255)
        if any(matches):
            name = "Unknown"
            color = (0, 200, 200)
            text_color = (0, 0, 0)

            for idx, m in enumerate(matches):
                if m:
                    person = self.persons[idx]
                    name = person.name

                    # todo encode and encrypt image file which is imported on program startup
                    if name == "Rob":
                        name = "Admin"
                        color = (0, 200, 0)
                    break
        return name, color, text_color

    def draw_identify(self, result):
        """
        Takes in the result of the camera identification and draws a rectangle around their face
        :param result:
        :return:
        """
        # defaults
        box_width = 100
        box_height = 22

        camera_width = self.camera.properties['width']
        camera_height = self.camera.properties['height']
        left = int(camera_width * 0.5 - box_width * 0.5)
        right = int(camera_width * 0.5 + box_width * 0.5)
        top = int(camera_height * 0.5 - box_height * 0.5)
        bottom = int(camera_height * 0.5 + box_height * 0.5)

        text = "Searching..."
        color = (0, 0, 200)
        text_color = (255, 255, 255)

        if result:
            left, top, right, bottom, text, color, text_color = result

        # Draw frame
        cv2.rectangle(Data.frame, (left, top), (right, bottom), color, 1)

        # Draw a label with a name below the face
        cv2.rectangle(Data.frame, (left, bottom - 20), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_PLAIN
        center = int((left + right) * 0.5 * 0.95)
        cv2.putText(Data.frame, text, (center, bottom - 6), font, 1.0, text_color, 1)

    def draw_fps(self, t1, t2):
        """
        Draws an FPS counter in the top left corner of the screen
        :param t1:
        :param t2:
        :return:
        """
        if Data.frame is None:
            return
        fps = math.floor((1000.0 - (t2 - t1).microseconds / 1000.0) * (60.0 / 1000.0))
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        fps_color = (255, 0, 0)
        cv2.putText(Data.frame, "FPS: {}".format(fps), (10, 15), font, 1.0, fps_color, 1)

    def write_text(self, text):
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        color = (0, 255, 0)
        camera_width = self.camera.properties['width']
        camera_height = self.camera.properties['height']
        x = int(camera_width * 0.4)
        y = int(camera_height * 0.2)
        cv2.putText(Data.frame, text, (x, y), font, 1.0, color, 1)

    def handle_frame(self):
        """ Grab a single frame of video """
        ret, frame = self.camera.video_capture.read()
        # Resize frame of video to half size for faster face recognition processing
        Data.frame = cv2.resize(frame, (0, 0), fx=1.0, fy=1.0)

    def update(self):
        """ Display the resulting image """
        cv2.imshow('Video', Data.frame)

    def calculate(self):
        """ Find all the faces and face encodings in the frame of video """
        if Data.frame is None:
            print("No camera input")
            return

        # print(Data.frame.shape)
        face_locations = face_recognition.face_locations(Data.frame)
        face_encodings = face_recognition.face_encodings(Data.frame, face_locations)
        results = []

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)

            matches = []
            if self.target_face_encoding_list:
                matches = face_recognition.compare_faces(self.target_face_encoding_list, face_encoding, self.TOLERANCE)
            else:
                speak = Speak()
                if not speak.listening:
                    self.talk_queue.enqueue("I don't recognise you.", 5)
                    self.talk_queue.enqueue("What's your name?", 5)
                else:
                    speak.start()

            name, color, text_color = self.identify(matches)

            elem = [left, top, right, bottom, name, color, text_color]
            results.append(elem)
        return results


class Data:

    frame = None
    result = None

    def __call__(self, *args, **kwargs):
        print(Data.frame, Data.result)


class Camera:

    def __init__(self, camera_width=640, camera_height=480):
        self.video_capture = None
        self.properties = {
            'width': camera_width,
            'height': camera_height
        }

    def start(self):
        print("Starting camera with properties: {}".format(self.properties))
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, self.properties['width'])
        self.video_capture.set(4, self.properties['height'])
        self.video_capture.set(12, 0.9)
        return self

