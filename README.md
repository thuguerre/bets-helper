# Bets Helper

Personal project to help me retrieving useful* results for my bets on Winamax.

## Getting Started

Please refer to [Getting Started procedure](./getting-started/README.md).

## Actions operated

* Using a GitHub Scheduled Workflow, Japan Baseball's NPB Regular Season results are retrieved each day and sent to a private SpreadSheet, where they are then humanly analyzed and used to bet.


*For the moment, useful means looseful.

## Mongo DB Dump & Restore commands

Under MacOS, following commands pre-requisite their installation using:
    brew install mongodb-community

To dump from remote MongoDB Atlas database, to a local default `dump/<db_name>` directory:

    mongodump --uri mongodb+srv://<user>:<pwd>@cluster0.gu9bi.mongodb.net/<db_name>

To restore from a local `dump/<db_name>` to a remote MongoDB Atlas database:

    mongorestore --uri mongodb+srv://<user>:<pwd>@cluster0.gu9bi.mongodb.net/<db_name> --dir dump/<db_name>