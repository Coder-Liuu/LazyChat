from setuptools import setup, find_packages

setup(
    name='LazyChat',
    version='0.25',
    author='Coder-liuu',
    author_email='lysc@bupt.edu.cn',
    description='A terminal chat software',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lazychat=LazyChat.main:main',
        ],
    },
)
