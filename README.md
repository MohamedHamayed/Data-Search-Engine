
# Innoscripta Search Engine (ISE)
Main goal of this project is to make researching process for information about companies easy and fast!
<br>It's a project for hackaton hosted by Innoscripta AG

# Table of Contents

1. [Installation](#installation)
3. [Improving scenario](#improving-scenario)
4. [Credits](#credits)

## Installation
If you want to install this project localy, follow steps below
1. Download repo on your machine
```python
git clone https://github.com/MohamedHamayed/innoscripta_search_engine.git
```
2. Setup a virtual environment <br>
#### Important! This project uses one legacy library which is not supported by new versions of python. <br> Please use python not higher than 3.7 version.
You can use "venv" for example
```python
python -m venv env
```
3. Install dependencies from requirements.txt <br>
You can use pip or any other package manager
```python
pip install -r requirements.txt
```
 

4. In main directory find file called
```python
delete_to_dot.env
```
and delete "delete_to_dot" from It's name

5. Inside this file fill in all gaps for credentials. <br>

You will need:
- Clearbit API key
- OpenAI API key
- Linkedin account credentials (email and password)

6. Run "server.py" <br>

It will run an API on localhost:8080/extract_info
You can find documentation for the API on localhost:8080/logs

## Improving scenario

## Credits
Created by <br>
[Mohamed Abu El Hamayed](https://github.com/MohamedHamayed) <br>
[Eugene Poluyakhtov](https://github.com/EPguitars)

## Acknowledgments
Thanks Innoscripta AG for hosting this hackaton event <br>
Also we want to thanks all companies and developers who work on all libraries we used in this project! 
