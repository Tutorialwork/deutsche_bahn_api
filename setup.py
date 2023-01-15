from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="deutsche-bahn-api",
    version="1.0.0",
    author="Tutorialwork",
    author_email="mail@manuelschuler.dev",
    description="A small package to work with the Deutsche Bahn timetables api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tutorialwork/deutsche_bahn_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)