from setuptools import setup, find_packages

setup(
    name="envarena",
    version="0.1.0",
    description="A collection of interactive environments with UI and LLM wrappers",
    author="ZapBot",
    packages=find_packages(exclude=("examples", "tests", "docs")),
    install_requires=[
        "ollama",
        "rich",
    ],
    python_requires=">=3.8",
)