from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="WZ MULTI-AI AGENT",
    version="1.0",
    author="warzho",
    packages=find_packages(),
    install_requires = requirements,
)
