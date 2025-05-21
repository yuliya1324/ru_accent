import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "requests>=2.21.0", 
    "russtress>=0.1.4",
    "tensorflow>=2.15.0",
    "numpy>=1.25.0",
    "scipy>=1.11.0"
]

test_requirements = [
    "pytest>=6.0.0",
]

setuptools.setup(
    name="ru_accent_poet",
    version="0.1.6",
    author="Julia Korotkova",
    author_email="koylenka15@gmail.com",
    maintainer="Danslav Slavenskoj",
    description="A package for putting stress marks in Russian poetic texts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuliya1324/ru_accent",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Russian",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="russian, accent, stress, poetry, nlp, linguistics",
    project_urls={
        "Changelog (EN)": "https://github.com/yuliya1324/ru_accent/blob/master/CHANGELOG.en.md",
        "Changelog (RU)": "https://github.com/yuliya1324/ru_accent/blob/master/CHANGELOG.ru.md",
        "Workflow (EN)": "https://github.com/yuliya1324/ru_accent/blob/master/WORKFLOW.en.md",
        "Workflow (RU)": "https://github.com/yuliya1324/ru_accent/blob/master/WORKFLOW.ru.md",
    },
)
