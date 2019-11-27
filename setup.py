from setuptools import setup

setup(name='victoria',
      version='0.2',
      description='Vitens water quality tool for distribution networks',
      url='https://github.com/michaeltan91/Victoria',
      author='Michael Tan',
      author_email='michael.tan@vitens.nl',
      license='Apache Licence 2.0',
      packages=['victoria'],
      package_data={'victoria': ['lib/*']},
      install_requires = [
          'pandas'
      ],
      zip_safe=False)