from __future__ import unicode_literals, print_function

from facial.face import Initialise, Camera, Display, Runner

if __name__ == '__main__':
    folder = "./data/known/"
    init = Initialise()
    tl, p = init.get_targets(folder)

    camera = Camera()
    camera.start()
    display = Display(camera, tl, p)
    Runner(display).run()

