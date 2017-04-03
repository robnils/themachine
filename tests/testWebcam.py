from __future__ import unicode_literals
from unittest import TestCase

from facial.face import Identification, Colours


class TestWebcam(TestCase):

    def test_get_colours_works(self):

        colour = Identification.get_color()
        self.assertEquals(colour, {
            'colour': Colours.red,
            'text_color': Colours.white
        })




