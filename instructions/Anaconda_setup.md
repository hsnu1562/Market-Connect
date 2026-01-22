# Setting up your project environment with Anaconda
this instruction covers "what does Anaconda do", "how to install Anaconda", "how to create an environment", and "how to set up the project environment for this project"

## what does Anaconda do?
It allows you to create different coding environment for different projects, preventing dependency conflicts.
(eg: project A needs python2, project B needs python3 ...etc)

## how to install Anaconda?
0.  to check if you already got Anaconda installed, type in:
    `conda --version`
    if it returns a version number, you're good to go :D
    if it returns an error, follow the steps below to install Anaconda

1.  go to the link [anaconda.com][anaconda_link], scroll to the bottom to find "miniconda installer", click on the download button

2.  after installing the installer, execute the installer by double-clicking it.

3.  test the conda commands by typing `conda --version`, you should get a version number

[anaconda_link]: https://www.anaconda.com/download

## how create an environment?
1.  to create an environment, go to any directory, and create an env by
    `conda create --name <env_name> [package_specifiers]`
    for example, here we want to create a environment with Python3.11.3 installed, so we type in:
    `conda create Python3_11_3 python=3.11.3`
    and accept all the terms.
    note: the "Python3_11_3" here is just a name for the environment, you can name it whatever you want, but for the sake of convenience, the following instruction will refer to the project environment as "Python3_11_3"

2.  confirm you indeed created the environment:
    `conda env list`
    this command will list out all the environments you have

## how to set up the environment for this project?
1.  activate the environment you just created:
    `conda activate Python3_11_3`
    you should now see `(Python3_11_3)` instead of `(base)` in the front of your command line, which means you are now in the project environment.

2. install the following packages:

- python 3.11.3 (you should already have this installed when setting up the environment)
- psycopg2
    `pip install psycopg2-binary`
- dotenv
    `pip install python-dotenv`
- fastapi
    `pip install fastapi "uvicorn[standard]"`
- psql
    ```
    #for windows
    pip install psql=18.1
    ```
    ```
    #for mac
    brew install libpq
    
    # For Intel Macs
    echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> ~/.zshrc
    # Or for Apple Silicon (M1/M2/M3) Macs
    echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
    ```
