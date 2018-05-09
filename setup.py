from setuptools import setup

setup(
    name='ctf_keyword_extractor',
    maintainer='Jim Sam',
    version=0.0.0,
    description='A package for extracting key word metadata out of the IPTC chunk in a jpg and uploading that data to a linked content entry in Contentful',
    long_description='A package for extracting key word metadata out of the IPTC chunk in a jpg and uploading that data to a linked content entry in Contentful',
    keywords=['IPTC','metadata','Contentful','API','content management','content infrastructure']
    license='MIT',
    platforms='any',
    python_requires='>=3.6',
    **setuptools_kwargs)
)
