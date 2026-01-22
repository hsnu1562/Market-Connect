# Market-Connect
make it easier to find available spots for marketing

## environment settings:
please make sure you set up a new environment for this project, so it won't be mixed up with your default system environment.
for more information, please read the instruction [Anaconda set up][Anaconda_set_up_link]

after setting up the environment, make sure to install the following resource packs *IN THE PROJECT ENVIRONMENT* with the command lines respectively

- python 3.11.3 (you should already have this installed when setting up the environment)
- psycopg2
    `pip install psycopg2-binary`
- dotenv
    `pip install python-dotenv`
- fastapi
    `pip install fastapi "uvicorn[standard]"`

The following instructions of this README will assume you have already installed the resource packs.

[Anaconda_set_up_link]: https://docs.google.com/document/d/1G99eqzaWmX9gbTUe_8kaidgMXl2Rng-4gZrOozwhj2k/edit?tab=t.0

## how to test the API:
1.  make sure you are in the same directory as `main.py` (which should be `Market-Connect`) and run：
    `uvicorn main:app --reload`
    this command will start a local server on your device,
    you should see a message that says "Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"

2.  go to any web browser, enter the link [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3.  you can now test out all the API routes. 
    for example: you want to test the function `/test-stalls`, simply find the function on the page, click it, then click "try it out", then click "execute".
    you should see the results below the "execute" button.