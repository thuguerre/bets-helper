# Getting Started

## Install Required Python3 Libraries

You can run the `install-required-python-libs.sh` to install or upgrade all libraries which are required to execute this Python3 application.

Under MacOS:

    sh install-required-python-libs.sh

## Set `.env` file to provide local environment variable

In `baseball-japan` folder, create a `.env` file what will provide required environment variables to your local context. This file will be read by `python-decouple` library (see `main_local_helper.py`).

The `.env` file must have following values:

    SA_PROJECT_ID=...
    SA_PRIVATE_KEY_ID=...
    SA_PRIVATE_KEY=...
    SA_CLIENT_EMAIL=...
    SA_CLIENT_ID=...
    SA_CLIENT_X509_CERT_URL=...

... where each `...` must be replaced by the right values. Please follow [the procedure](https://docs.gspread.org/en/latest/oauth2.html) from this page to initialize your own values from your own Google Project Account.