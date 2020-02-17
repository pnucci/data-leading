# data-leading

Python code related to the article Data-oriented team management: Perception of skills and behaviours
https://medium.com/@pnucci/data-oriented-team-management-perception-of-skills-and-behaviours-part-1-afaa6d80ddb

## Requirements
Python with the libraries in the `requirements.txt` file.

To install them using pip, run:

`pip install -r requirements.txt`


## Survey setup

The `make_report.py` script in this repository is ready to handle surveys like below, made in Google Forms:

<img src="https://raw.githubusercontent.com/pnucci/data-leading/master/survey-screenshot.png" height="500">

Google Forms allows you to download survey responses to a CSV file like `demo-responses.csv`.

Then you just need to run:

`python make_report.py demo-responses.csv`

It will generate one report HTML file per each person in the survey.
