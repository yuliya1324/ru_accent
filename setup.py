import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["requests>=2.21.0", "russtress"]

setuptools.setup(
    name="ru_accent_poet",
    version="0.1.2",
    author="Julia Korotkova",
    author_email="koylenka15@gmail.com",
    description="A package for putting stress marks in russian poetic texts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuliya1324/ru_accent",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
