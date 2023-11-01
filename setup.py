from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="deutsche-bahn-api",
    version="1.0.6",
    author="Tutorialwork",
    author_email="mail@manuelschuler.dev",
    description="A small package to work with the Deutsche Bahn timetables api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tutorialwork/deutsche_bahn_api",
    packages=find_packages(),
    install_requires=["mpu", "requests"],
    package_data={"deutsche_bahn_api": ["static/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)