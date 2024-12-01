from setuptools import setup, find_packages

setup(
    name="code_prompter",
    version="1.0.0",
    description="A tool to summarize project directories for LLM inputs",
    author_email="zhaojy2005@outlook.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "code-prompter=code_prompter.main:main",
        ],
    },
    install_requires=[
        'setuptools>=65.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="Apache 2.0",
)

