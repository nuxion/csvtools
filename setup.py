import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csvtoolz",
    version="0.0.5",
    author="Xavier Petit",
    author_email="nuxion@gmail.com",
    description="Manage CSV related tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=['chardet>=3.0.4',
                      'toolz>=0.9.0',
                      'Jinja2>=2.10',
                      'nose>=1.3.7',
                     'SQLAlchemy>=1.2.11'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
