from setuptools import setup

setup(name='expecter',
      version='0.2.1',
      description='Expecter Gadget, a better expectation (assertion) library',
      long_description=open('README.txt').read(),
      author='Gary Bernhardt',
      author_email='gary.bernhardt@gmail.com',
      py_modules=['expecter'],
      url='https://github.com/garybernhardt/expecter',
      license='BSD',
      classifiers=['Development Status :: 3 - Alpha',
                   'Topic :: Software Development :: Testing',
                   'Intended Audience :: Developers']
     )

