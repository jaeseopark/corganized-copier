from setuptools import setup, find_packages

setup(
    name="copier",
    packages=find_packages(exclude=("test",)),
    python_requires=">=3.6",
    install_requires=["PyYAML", "gdrivewrapper", "httplib2", "commmons", "corganizeclient"]
)
