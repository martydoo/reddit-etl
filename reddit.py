import logging
import os
from dataclasses import dataclass

import praw
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


@dataclass
class RedditPostData:
    """
    Dataclass to contain Reddit post data.

    Args:
        id (str): Post unique ID.
        community (str): SubReddit containing post.
        title (str): Post title.
        score (int): Post score.
        url (str): Post URL.
        comments (int): Number of comments.
        created (str): Creation datetime.
        text (str): Post contents.
    """

    id: str
    community: str
    title: str
    score: int
    url: str
    comments: int
    created: str
    text: str


class RedditETL:
    """
    Pull data from a particular community, filter based on specifications,
    and load into a local SQLite database.
    """

    def extract(self, sub, num_posts, client):
        """
        Extract posts from community.

        Args:
            sub (str): SubReddit to pull from.
            num_posts (int): Number of posts to retrieve.
            client (praw.Reddit): Client used to interact with Reddit.

        Returns:
            List[RedditPostData]: List of Reddit submission data.
        """
        logger.info("Extracting posts.")
        if client is None:
            raise ValueError("Must pass client object.")

        subreddit = client.subreddit(sub)
        popular_posts = subreddit.hot(limit=num_posts)
        reddit_data = []

        for submission in popular_posts:
            reddit_data.append(
                RedditPostData(
                    id=submission.id,
                    community=submission.subreddit.name,
                    title=submission.title,
                    score=submission.score,
                    url=submission.url,
                    comments=submission.num_comments,
                    created=str(submission.created_utc),
                    text=submission.selftext,
                )
            )

        return reddit_data

    def transform(self, data, transform_function):
        """
        Filter post data based on function.

        Args:
            data (List[RedditPostData]): List of Reddit submission data.
            transform_function (Callable): Filter to apply to posts.

        Returns:
            List[RedditPostData]: Filtered list of Reddit submission data.
        """
        logger.info("Transforming posts.")
        return transform_function(data)

    def load(self, data, cursor):
        """
        Load transformed post data into database.

        Args:
            data (List[RedditPostData]): Filtered list of Reddit submission data.
            cursor (DatabaseConnection): Managed cursor to access database.
        """
        logger.info("Loading posts.")
        if cursor is None:
            raise ValueError("Must pass cursor object.")

        with cursor as cur:
            for submission in data:
                cur.execute(
                    """
                    INSERT OR REPLACE INTO
                        posts (
                        id, community, title, score, url, comments, created, text
                        )
                    VALUES (
                        :id, :community, :title, :score, :url, :comments, :created, :text
                        )
                    ;
                    """,
                    {
                        "id": submission.id,
                        "community": submission.community,
                        "title": submission.title,
                        "score": submission.score,
                        "url": submission.url,
                        "comments": submission.comments,
                        "created": submission.created,
                        "text": submission.text,
                    },
                )

    def run(self, cursor, client, transform_function, sub="all", num_posts=50):
        """
        Run ETL pipeline.

        Args:
            cursor (DatabaseConnection): Managed cursor to access database.
            client (praw.Reddit): Client used to interact with Reddit.
            transform_function (Callable): Filter to apply to posts.
            sub (str): SubReddit to pull from.
            num_posts (int): Number of posts to retrieve.
        """
        logger.info("Running Reddit ETL pipeline.")

        # Extract `num_posts` from `sub` community using `client`
        raw_data = self.extract(sub, num_posts, client)

        # Filter `raw_data` based on `transform_function` filter
        transformed_data = self.transform(raw_data, transform_function)

        # Load `transformed_data` into database using managed `cursor` object
        self.load(transformed_data, cursor)


def etl_factory(site):
    """
    Factory to specify post data source. Currently only supports Reddit,
    but can be extended in the future to pull data from other platforms.

    Args:
        site (str): Site to extract data from. Defaults to Reddit.

    Returns:
        Tuple[praw.Reddit, RedditETL]: Tuple containing client and pipeline.
    """
    factory = {
        "reddit": (
            praw.Reddit(
                client_id=os.environ["REDDIT_CLIENT_ID"],
                client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                user_agent=os.environ["REDDIT_USER_AGENT"],
            ),
            RedditETL(),
        )
    }

    if site in factory:
        return factory[site]
    else:
        raise ValueError(f"{site} is not supported.")
