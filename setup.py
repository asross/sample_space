import setuptools
import sample_space
from subprocess import check_output

readme = check_output("pandoc --from=markdown --to=rst README.md",
                      shell=True).decode('utf-8')

setuptools.setup(name='sample_space',
      version='0.1.0',
      test_suite='nose.collector',
      tests_require=['nose'],
      description='A simple API for defining sample spaces (to run simple statistical simulations)',
      long_description=readme,
      install_requires=['numpy', 'matplotlib'],
      url='http://github.com/asross/sample_space',
      author='Andrew Ross',
      author_email='andrewslavinross@gmail.com',
      license='MIT',
      packages=['sample_space'],
      zip_safe=False)
