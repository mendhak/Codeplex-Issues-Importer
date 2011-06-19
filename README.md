# Codeplex to Github Issues Importer

## Instructions

1 - Download the [github2 Python library](http://packages.python.org/github2/).

2 - Install the [github2 Python library](http://packages.python.org/github2/install.html).

3 - Download the codepleximport.py script

4 - Open it in a text editor and modify the values at the top


* CODEPLEX\_PROJECT - the subdomain of the project on codeplex _(yourproject.codeplex.com)_
* GITHUB\_PROJECT - the name of the repository on github _(Codeplex-Issues-Importer)_
* GITHUB\_USERNAME - your github username _(mendhak)_
* GITHUB\_ISSUELABEL - a tag that will be applied to all issues imported _(CodePlex)_
* GITHUB\_APITOKEN - your API Token which you can get from your [account admin page](https://github.com/account/admin)


5 - Run the script.


## Notes

* This script will close an imported issue if it is closed on Codeplex
* You can see a test import [here](https://github.com/mendhak/Codeplex-Issues-Importer/issues?sort=created&direction=desc&state=closed&page=1). 
* All issues and comments will be under your username, but containing the codeplex user's name
* Apologies if I'm not following a proper code style, this is my first Python script 
