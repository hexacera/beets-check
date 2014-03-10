from setuptools import setup

with open('README.md') as desc:
    long_description = desc.read()
setup(name='beets-check',
      version='0.9.0-beta',
      description='beets plugin verifying file integrity with checksums',
      long_description=long_description,
      author='Thomas Scholtes',
      author_email='thomas-scholtes@gmx.de',
      url='http://www.github.com/geigerzaehler/beets-check',
      license='MIT',
      platforms='ALL',

      test_suite='test',

      packages=['beetsplug'],
      namespace_packages=['beetsplug'],

      install_requires=[
          'beets>=1.3.0',
      ],

      classifiers=[
          'Topic :: Multimedia :: Sound/Audio',
          'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
          'License :: OSI Approved :: MIT License',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
)
