from setuptools import setup, find_packages

setup(name='flasktdd',
      version='1.0.0',
      description='flask tdd project',
      author='Isamu Hirahata',
      author_email='isamuhirahata@gmail.com',
      url='https://github.com/isamuhiro/flasktdd.git',
      packages=find_packages(exclude=('tests*', 'testing*')))
