from setuptools import setup, find_packages

setup(
    name='Bluetin_Echo',
    version='0.2.0',
    packages = find_packages(),
    description='Raspberry Pi Python Library for Ultrasonic Module HC-SR04 Distance Measuring Transducer.',
    long_description=open('README.rst').read(),
    url='https://github.com/MarkAHeywood/Bluetin_Python_Echo',
    author='Mark A Heywood',
    author_email='mark@shinex.com',
    license='MIT',
    classifiers=[
		'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: System :: Hardware',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords=['RPI', 'GPIO', 'Raspberry Pi', 'Ultrasonic', 'HC-SR04', 'Transducer', 'Distance Measuring', 'Sensor'],
    install_requires=['RPi.GPIO'],
)
