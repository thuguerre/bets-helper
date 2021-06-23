# Getting Started

## Install Required Python3 Libraries

You can run the `requirements.txt` to install or upgrade all libraries which are required to execute this Python3 application.

    pip install -r requirements.txt

## Set `.env` file to provide local environment variable

In root folder, create a `.env` file what will provide required environment variables to your local context. This file will be read by `python-decouple` library (see `LocalExecHelper.py`).

The `.env` file must have following values:

    SA_PROJECT_ID=...
    SA_PRIVATE_KEY_ID=...
    SA_PRIVATE_KEY=...
    SA_CLIENT_EMAIL=...
    SA_CLIENT_ID=...
    SA_CLIENT_X509_CERT_URL=...

    MONGODB_USER=...
    MONGODB_PWD=...
    MONGODB_NAME=...

... where each `...` must be replaced by the right values.

* For all `SA_*` values, please follow [the procedure](https://docs.gspread.org/en/latest/oauth2.html) from this page to initialize your own values from your own Google Project Account.
* For all `MONGODB_*` values, please use a cluster MONGO from [mongodb.com](https://www.mongodb.com).

As `.env` file will contain secrets, it is ignored from any committing to GitHub.