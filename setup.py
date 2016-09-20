from setuptools import setup


def readme():
    with open('README.rst', 'r') as f:
        return f.read()


setup(
    name='quilt',
    packages=['quilt'],
    version='0.1.6',
    description='Quilt Python API https://quiltdata.com',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    author='quiltdata',
    author_email='founders@quiltdata.io',
    license='LICENSE.txt',
    url='https://github.com/quiltdata/python-api',
    download_url='https://github.com/quiltdata/python-api/tarball/0.1.6',
    keywords='quiltdata api social shareable data platform',
    install_requires=[
        'requests==2.11.1',
        'numpy==1.11.1',
        'pandas==0.18.1',
        'psycopg2==2.6.2',
        'sqlalchemy==1.0.15',
    ],
    include_package_data=True,
    zip_safe=False)
