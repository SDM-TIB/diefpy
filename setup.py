from distutils.core import setup

setup(name='diefpy',
      version='0.1',
      packages=['diefpy'],
      url='https://github.com/maribelacosta/diefpy',
      license='MIT',
      author='Maribel Acosta',
      author_email='maribel.acosta@kit.edu',
      description='Python package for computing diefficiency metrics dief@t and dief@k.',
      keywords='metrics benchmarking efficiency diefficiency-metrics dief python',
      install_requires=['matplotlib', 'numpy'])
