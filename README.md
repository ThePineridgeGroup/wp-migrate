# app-model-py3 #

This is a model for setting up a python application:
* uses nosetest
* includes a data directory which is optional


To run the application:
    from the main folder xxxxxxxxxxxx enter

    python xxxxxx data/xxxxx


    the data folder contains the test result files to be processed


To test the application:
     from the main folder enter

     nosetests

## Structure ##

The application code in is the xxxxx folder, data in the data folder and
tests are in the tests folder.

The data folder should contain sub-folders which hold the original files
generated from the test.  All results related to the test are kept in the
the sub-folder.

* config.ini - this file contains the run parameters (see discussion below)

## Config File ##

describe the config file

## Data ##

The data/ folder will contain a sub-folder for each test.  Usually the folder
name is the test number.

