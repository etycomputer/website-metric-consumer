![GitHub](https://img.shields.io/github/license/etycomputer/website-metric-consumer)

# website-metric-consumer

## Introduction

This is a background app that subscribes to a kafka topic and processes the messages. 
The messages contain website metric measurements collected by another process.
These measurements are then stored on a Postgres database.

---

## Project Setup

### First Steps

You can begin by either downloading a zip file of the project through github, or using a git command to clone the project by:

```bash
git clone https://github.com/etycomputer/website-metric-consumer.git
```

### Virtual Environment Setup

Create a [Python 3.8.1](https://www.python.org/downloads/release/python-381/) based virtual environment (venv) for this project directory.
```bash
virtualenv venv -p python3.8.1
```
After you have your virtual environment directory Setup, you need to activate it.

#### On Linux
```bash
source venv/bin/activate
```
#### On Windows
```bash
venv\Scripts\activate
```
### Dependency installations

To install the necessary packages:

```bash
pip install -r requirements.txt
```

### Setting up environment variables

This app requires setting up a few environment variables

#### On Linux
```bash
export POSTGRES_DB_USER=xxx
export POSTGRES_DB_PASSWORD=xxx
export POSTGRES_DB_HOST=xxx
export POSTGRES_DB_PORT=xxx
export POSTGRES_DB_DATABASE=xxx
export TARGET_SIMULATOR_HOST=https://simple-flask-website-simulator.herokuapp.com
```

#### On Windows
```bash
set POSTGRES_DB_USER=xxx
set POSTGRES_DB_PASSWORD=xxx
set POSTGRES_DB_HOST=xxx
set POSTGRES_DB_PORT=xxx
set POSTGRES_DB_DATABASE=xxx
set TARGET_SIMULATOR_HOST=https://simple-flask-website-simulator.herokuapp.com
```
---

##Requirements

This project utilizes the following requirements:

1. Python v3.8.1
1. pytest v6.2.3
1. kafka-python v2.0.2
1. psycopg2 v2.8.6
