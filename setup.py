from setuptools import setup

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: Microsoft :: Windows',
    'Topic :: Utilities',
]
py_versions = ['2', '2.6', '2.7']
classifiers += [
    'Programming Language :: Python :: %s' % x
    for x in py_versions
]

setup(
    name='bender-skype',
    description='bender-skype: Skype as Bender backbone',
    version='0.1.0',
    url='https://github.com/bender-bot/bender-skype',
    license='LGPLv3',
    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
    author='Fabio Menegazzo',
    author_email='menegazzo@gmail.com',
    classifiers=classifiers,
    install_requires=['Skype4Py'],
    py_modules=['bender_skype'],
    entry_points={
        'bender_backbone': [
            'skype = bender_skype:BenderSkype',
        ],
    }
)
