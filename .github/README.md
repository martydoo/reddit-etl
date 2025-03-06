# reddit-etl: An end-to-end data pipeline for Reddit posts 📝🛠️
This project serves to extract submissions, filter them in a variety of ways, and load them into a SQLite database. Airflow is used to run the pipeline and automatically generate CSV database backups within the project folder on a scheduled basis. A CLI script is also included to initiate the ETL process on an ad hoc basis for testing purposes. The entire application is containerized using Docker to maintain a predictable and replicable environment.

## Purpose & Inspiration
I recently came across Joseph Machado's excellent [blog post](https://www.startdataengineering.com/post/code-patterns/) on data pipeline design and felt building [his project](https://github.com/josephmachado/socialetl) from scratch and expanding upon it would be a great learning opportunity. Having used social media for so many years, working with real data from Reddit was inherently interesting and rewarding.

This project has allowed me to reinforce my skills in Python, SQL, and shell scripting, as well as put classroom knowledge into practical use—incorporating Airflow and Docker with no concrete blueprint sent me down numerous rabbit holes, but taught me an incredible amount in such a short time.

Though my primary goal was to build an ETL pipeline, I learned a lot along the way about design principles and how different components of a codebase interact (even if this one's relatively small and isolated).

## Technologies
* **Python**: Core pipeline logic, DAG configuration, CLI, packaging
    * **External Libraries**: apache-airflow, dotenv, numpy, praw, setuptools
    * **Standard Libraries**: argparse, contextlib, dataclasses, datetime, logging, os, pathlib, random, sqlite3
* **Bash**: Shell script for CSV generation
* **SQL**: Schema creation, database loading, queries
* **Apache Airflow**: DAG management, monitoring, scheduling
* **Docker**: Containerization of application

## How It Works
Accessible through both ```cli.py``` and ```dag.py```, the ```main.py``` module handles interactions between the three core modules: ```db.py```, ```etl.py```, and ```transform.py```. The ```defaults.py``` module includes default arguments in a dictionary format to ensure consistency and a single source of truth across all components.

```db.py``` manages the connection to the SQLite database, executing changes and automatically closing the associated cursor. A function, ```db_factory()```, handles database file name specification and returns a ```DatabaseConnection``` object for the user to interact with.

```transform.py``` contains four filters and another factory for easy return of the selected transformation function. ```zero_transformation()``` applies no filter to the posts passed to the function. ```random_transformation()``` selects five random submissions. ```discussion_transformation()``` filters for posts with at least one comment. ```popular_transformation()``` filters for posts with scores (upvotes) greater than two standard deviations above the mean.

```etl.py``` contains the bulk of the code, returning a client object and a class, ```RedditETL```, which contains a method for each stage in the data pipeline. Data is extracted from Reddit using PRAW, Reddit's API wrapper for Python. Data stored in the ```RedditPostData``` dataclass include post ID, community name, title, score, URL, number of comments, creation datetime and post contents.

After the ETL pipeline is run, the shell script, ```generate_csv.sh```, serves to automate the database backup process. If run using the DAG, this script will be executed following the data loading process.

A script, ```schema.py```, is also included to make schema creation and deletion easier.

## Setup
Before running the pipeline for the first time, the database should be reset using:

```python3 schema.py --reset-db```

This can, of course, be run at any time a clean slate is desired.

Instructions for setting up the ```.env``` file can be found in Machado's repo. 

As stated before, ```cli.py``` can be used when scheduled runs are not required. Command-line arguments allow for customization of post sorting method (hot [default], new, top) and filter (zero [default], random, discussion, popular), as well as SubReddit selection (default is 'all'). For example:

```python3 cli.py --sub pinball --sort top --filter random```

If one wishes to start the DAG, it's fairly easy to do so as Docker eliminates the need to install Airflow separately. Installation of all dependencies and Airflow UI setup is handled through:

```docker-compose up --build```

Airflow can subsequently be accessed at:

```http://localhost:8080/```

Ctrl+C will shut down the Airflow service, and the Docker container can be stopped with:

```docker-compose down```

## Project Differences
* Where does my project differ from original

## Challenges & Future Iterations
* Components I wish to extend

## Acknowledgements
Thank you to Joseph Machado for making the original project's repo publicly available, and for making data engineering feel so accessible through his [blog](https://www.startdataengineering.com/), even to a beginner like myself.
