from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='web_ip_calc',

      version='0.1.0',
      description='WEB IP calculator written in python',
      url='https://ipcalc.pielatowski.pl',
      author='Adam Pielatowski',
      author_email='pielatowski@outlook.com',
      packages=['web_ip_calc'],
      install_requires=required,
      )
