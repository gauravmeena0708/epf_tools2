import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='epftools',
    author='gaurav meena',
    author_email='gauravmeena0708@gmail.com',
    description='epftools (Python Package Index) Package',
    keywords='example, pypi, package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gauravmeena0708/epftools',
    project_urls={
        'Documentation': 'https://github.com/gauravmeena0708/epftools',
        'Bug Reports': 'https://github.com/gauravmeena0708/epftools/issues',
        'Source Code': 'https://github.com/gauravmeena0708/epftools',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
 
)
