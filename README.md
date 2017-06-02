# Codeplex to Github Issues Importer

A Python 2.x script.

## Instructions

1 - Install [github3 Python library](https://github.com/sigmavirus24/github3.py) using either 
    
    easy_install github3.py 

or

    pip install github3.py

2 - Download the codepleximport.py script

3 - Open it in a text editor and modify the values at the top


    CODEPLEX\_PROJECT - the subdomain of the project on codeplex _(yourproject.codeplex.com)_
    GITHUB\_PROJECT - the name of the repository on github _(Codeplex-Issues-Importer)_
    GITHUB\_USERNAME - your github username _(mendhak)_
    GITHUB\_ISSUELABEL - a tag that will be applied to all issues imported _(CodePlex)_
    GITHUB\_PASSWORD - your github password


4 - Run the script.


## Notes

* This script will close an imported issue if it is closed on Codeplex
* You can see a test import [here](https://github.com/mendhak/Codeplex-Issues-Importer/issues?sort=created&direction=desc&state=closed&page=1). 
* All issues and comments will be under your username, but containing the codeplex user's name
* Apologies if I'm not following a proper code style, this is my first Python script 
