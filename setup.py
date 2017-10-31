from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='diefpy',
      version='0.1',
      packages=['diefpy'],
      url='https://github.com/maribelacosta/diefpy',
      license='MIT',
      author='Maribel Acosta',
      author_email='maribel.acosta@kit.edu',
      description='Python package for computing diefficiency metrics dief@t and dief@k.',
      keywords='metrics benchmarking efficiency diefficiency-metrics dief python',
      install_requires=['matplotlib>=1.3.1', 'numpy>=1.8.0'],
      include_package_data=True,
      package_data={'dief': ['data/*']},
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python',
            'License :: OSI Approved :: MIT License',
            'Topic :: System :: Benchmark'
      ])
