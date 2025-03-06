from setuptools import setup, find_packages

setup(
    name="reddit-etl",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["numpy==1.26.4", "praw==7.7.1", "python-dotenv==1.0.0"],
)
