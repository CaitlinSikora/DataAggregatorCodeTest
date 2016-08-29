Data_P_Score
=========

This is a quick stab at calculating a P-score for a particular small business using only publicly available APIs.

It considers the data available for the business's Facebook page, assigning a higher score for a greater amount of information available, greater frequency and consistency of posts, and greater sentiment analysis of recent posts.

It considers the data available for the business's Yelp page, assigning a higher score for a greater amount of information available, higher ratings, more reviews and higher performance compared to businesses in direct competition.

It uses the Google API to search the owner, looking for news articles related to the owner and this type of business. It also uses the yelp data found in the google search to make a projection of the business's ratings over time.

Each consulted API is used to assign the business a score. The scores from each source are averaged and displayed on the Results page, along with alert messages associated with each score.


Installation
------------

This flask app is created using a virtual environment. Dependencies are listed in requirements.txt.

Running
-------

To run the application in the development web server just execute `run.py` with the Python interpreter from a virtual environment with the required dependencies.

