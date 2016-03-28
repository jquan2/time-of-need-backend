# time-of-need-backend
Infrastructure for the UAF-CS Spring 2016 Time Of Need project.


----


[![Build Status](https://travis-ci.org/tjslauson/time-of-need-backend.svg?branch=master)](https://travis-ci.org/tjslauson/time-of-need-backend)

## Table of Contents

* **[Installation](#installation)**
* **[Configuration](#configuration)**
* **[Usage](#usage)**


----


## Installation

```
# Clone the project
git clone https://github.com/tjslauson/time-of-need-backend.git

# Install virtualenv and set up a virtualenv
cd time-of-need-backend
pip install virtualenv
virtualenv venv
source venv/bin/activate

# Install application stack
pip install -r requirements.txt
```


----


# Configuration

```
# Build/seed database
python main.py initialize_db
```


----


## Usage
Run a development server:

```
python main.py runserver
```

Point your browser at localhost:8000

