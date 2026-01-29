# Market-Connect-API
the api built for market-connect

## environment settings:
please make sure you set up a new environment for this project, so it won't be mixed up with your default system environment.
to setup the environment, please follow the instructions in [Anaconda set up][Anaconda_set_up_link].

The following instructions of this README will assume you have already installed the requirements.

[Anaconda_set_up_link]: ./instructions/Anaconda_setup.md

## test the API online:
1. go to the link [market-coonnect-api][market-connect-api_link]. if you don't see the commands, you might need to reload the page after a minute.

2. you can now test out all the API routes. 
    for example: you want to test the function `/test-stalls`, simply find the function on the page, click it, then click "try it out", then click "execute".
    you should see the results below the "execute" button.

[market-connect-api_link]:https://market-connect-api-o4hq.onrender.com/

## test the API locally:
1.  make sure you are in the same directory as `main.py` (which should be `Market-Connect`) and run：
    `uvicorn main:app`
    this command will start a local server on your device,
    you should see a message that says "Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"

2.  go to any web browser, enter the link [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3.  you can now test out all the API routes. 
    for example: you want to test the function `/test-stalls`, simply find the function on the page, click it, then click "try it out", then click "execute".
    you should see the results below the "execute" button.

## structure of the database:
please read the instruction [Tables.md][Tables_link]

[Tables_link]: ./instructions/Tables.md

## workflow:
if you want to make contribution to this project, please follow the [workflow][workflow_link]

[workflow_link]: ./instructions/Workflow.md