from setuptools import setup, find_packages

setup(
    name='SpectraPro',
    version='0.1',
    packages=find_packages(where='origin'),  # source directory
    package_dir={'': 'origin'},  # source directory
    install_requires=[
        'spe2py',
        'spe_loader',
        'numpy',
        'matplotlib',
        'math',
        'os',
        'sys',
        're',
        'scipy',
        'PyQt5',
    ],  # 这里可以添加依赖包
    author='Junjie Xie',
    author_email='a1033899938@gmail.com',
    description='A program for processing spectra data',
    long_description=open('tests/origin/README.md').read(),
    long_description_content_type='text/markdown',
    url="Haven't personal pages now",  # 项目主页
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
