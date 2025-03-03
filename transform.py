import logging
import random
import numpy as np

def zero_transformation(data):
    """
    Does not apply any filters to the data.
    
    Args:
        data (List[RedditPostData]): List of Reddit submission data.
    
    Returns:
        List[RedditPostData]: Filtered list of Reddit submission data.
    """
    logging.info('No transformation applied.')
    return data

def random_transformation(data):
    """
    Randomly selects 5 submissions from the list of data.
    
    Args:
        data (List[RedditPostData]): List of Reddit submission data.
    
    Returns:
        List[RedditPostData]: Filtered list of Reddit submission data.
    """
    logging.info('Randomly selecting five posts.')
    posts = random.choices(data, k=5)
    return posts
    
def discussion_transformation(data):
    """
    Filters data for posts with greater than 0 comments.
    
    Args:
        data (List[RedditPostData]): List of Reddit submission data.
    
    Returns:
        List[RedditPostData]: Filtered list of Reddit submission data.
    """
    logging.info('Keeping posts with one or more comments.')
    posts = [post for post in data if post.comments > 0]
    return posts
    
def popular_transformation(data):
    """
    Filters data for posts with greater than 2 standard deviations above
    the mean number of upvotes.
    
    Args:
        data (List[RedditPostData]): List of Reddit submission data.
    
    Returns:
        List[RedditPostData]: Filtered list of Reddit submission data.
    """
    logging.info('Finding the most popular posts.')
    upvotes = np.array([post.score for post in data])
    
    mean_upvotes = upvotes.mean()
    sd_upvotes = upvotes.std()
    min_upvotes = mean_upvotes + (2 * sd_upvotes)
    
    posts = [post for post in data if post.score > min_upvotes]
    return posts
    
def transformation_factory(transform_function):
    """
    Factory to select transformation function.
    
    Args:
        transform_function (str): Filter to apply to data. Defaults to no effect.
        Currently supports [zero, random, discussion, popular] transformations. 
    
    Returns:
        Callable: Transformation function to apply to submissions.
    """
    factory = {
        "zero": zero_transformation,
        "random": random_transformation,
        "discussion": discussion_transformation,
        "popular": popular_transformation
    }
    
    if transform_function in factory:
        return factory[transform_function]
    else:
        raise ValueError(f"{transform_function} is not a valid filter.")
