from setuptools import setup, find_packages

setup(
    name='Simple CRUD Flask and MongoDB',
    version='1.0.0',
    description='',
    author='Patar Martua Doli Siahaan',
    author_email='patarmds@gmail.com',
    url='https://github.com/patarshn/simple-crud-flask-mongodb',
    packages=find_packages(),
    install_requires=[
        'Flask==2.1.2',
        'pymongo==4.1.1',
        'pymongo[srv]==4.1.1',
    ]
)