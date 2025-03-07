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

```etl.py``` contains the bulk of the code, returning a client object and a class, ```RedditETL```, which contains a method for each stage in the data pipeline. Data is extracted from Reddit using PRAW, Reddit's API wrapper for Python. Data stored in the ```RedditPostData``` dataclass include post ID, community name, title, score, URL, number of comments, creation datetime, and post contents.

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
In the initial stages of the project, I followed the original code fairly closely. A few modifications were made to the filters applied, and I also added sort method functionality. I chose not to include tests or metadata generation, though I recognize the importance of these components. The original project also included an ETL pipeline for Twitter, which I skipped, and an associated abstract base class. I kept the ETL factory, though this was probably unnecessary given that Reddit is the only site my pipeline supports.

The major differences began to emerge when I made the decision to implement Airflow as an orchestrator. I went back and forth about how to break my code up into DAG tasks, but ultimately ended up splitting the main module into ```main.py``` and ```cli.py```. This allows for increased flexibility, as the latter maintains command-line argument parsing and ```dag.py``` is able to use the same logic stored in ```main.py``` in the form of a task. Using decorators to define the DAG and its tasks through the TaskFlow API was new to me, but I figured it wouldn't be a bad idea to familiarize myself as this appears to be the more modern and recommended approach.

My project also uses Docker, unlike the original. I chose to do this partly due to the Airflow integration, but I mostly wanted hands-on experience with containerization.

## Challenges & Future Iterations
Funnily enough, the most difficult part of this project was learning how to package my modules and work with Docker. Prior to this, most of my projects have been limited to one or two scripts, so dealing with so many files and directories was a learning experience in itself. Creating the Dockerfile also took a lot of trial and error, but I eventually got it to function how I wanted it to. Setting up relative paths to ensure compatibility with both the CLI and DAG was also tough, because I was set on having Airflow generate CSVs in the project's output folder.

Though I'm happy with where it is currently, there's a ton of room for extension with this project. For one, more social media sites could be supported. As for the database, SQLite is sufficient for a project of this scale, but I would like to learn how to implement Airflow's PostgresOperator in the future. I contemplated using DuckDB, but didn't need the analytical efficiency it offers—again, it wouldn't have mattered given the scale, but it was still a consideration.

It would be interesting to incorporate more SQL, or somehow email the CSV generated in each DAG run. S3 integration and handling streaming data also crossed my mind for future exploration.

## Acknowledgements
Thank you to Joseph Machado for making the original project's repo publicly available, and for making data engineering feel so accessible through his [blog](https://www.startdataengineering.com/), even to a beginner like myself.
