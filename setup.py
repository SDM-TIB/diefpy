from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='diefpy',
      version='0.2',
      packages=['diefpy'],
      url='https://github.com/maribelacosta/diefpy',
      license='MIT',
      author='Maribel Acosta',
      author_email='maribel.acosta@kit.edu',
      description='Python package for computing diefficiency metrics dief@t and dief@k.',
      keywords='metrics benchmarking efficiency diefficiency-metrics dief python',
      install_requires=['matplotlib==3.2.2', 'numpy>=1.8.0'],
      include_package_data=True,
      package_data={'dief': ['data/*']},
      python_requires='>3.6',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Framework :: Matplotlib',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'License :: OSI Approved :: MIT License',
            'Topic :: System :: Benchmark',
            'Typing :: Typed'
      ])
