from __future__ import unicode_literals
import pip

requirements = ['requirements.txt', 'requirements_facial.txt', 'requirements_speech.txt']


def install(packages):
    for package in packages:
        pip.main(['install', package])

if __name__ == '__main__':

    for filepath in requirements:
        with open(filepath) as fp:
            req = fp.readlines()
        print('Installing: {}'.format(filepath))
        install(req)
    print("Done!")