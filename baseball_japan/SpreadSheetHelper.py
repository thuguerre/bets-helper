import os
import datetime
import gspread

SPREADSHEET_NAME = "Suivi paris"
SPREADSHEET_INDEX = 6               # index of 'Baseball Japan RAW', starting from 0


class SpreadSheetHelper:

    jpn_raw_sheet = None

    def __init__(self):
        self.jpn_raw_sheet = self.get_jpn_raw_results_sheet()

    def get_last_result_date(self):
        values_list = self.jpn_raw_sheet.col_values(1)
        values_list.remove('Date')  # removing column title from values
        values_list.sort(key=lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'))
        return values_list[-1]

    def next_available_row(self):
        str_list = list(filter(None, self.jpn_raw_sheet.col_values(1)))
        return str(len(str_list)+1)

    def get_jpn_raw_results_sheet(self):

        # use creds to create a client to interact with the Google Drive API
        # example from: https://docs.gspread.org/en/latest/oauth2.html
        credentials = {
            "type": "service_account",
            "project_id": os.environ["SA_PROJECT_ID"],
            "private_key_id": os.environ["SA_PRIVATE_KEY_ID"],
            "private_key": os.environ["SA_PRIVATE_KEY"],
            "client_email": os.environ["SA_CLIENT_EMAIL"],
            "client_id": os.environ["SA_CLIENT_ID"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.environ["SA_CLIENT_X509_CERT_URL"]
        }
        client = gspread.service_account_from_dict(credentials)

        return client.open(SPREADSHEET_NAME).get_worksheet(SPREADSHEET_INDEX)

    def upload_results(self, results):

        for result in results:
            next_row = self.next_available_row()
            self.jpn_raw_sheet.insert_row(['temp'], int(next_row))
            self.jpn_raw_sheet.update(
                'A' + next_row + ':U' + next_row,
                [
                    [
                        result.date,
                        '=WEEKDAY(A' + next_row + ';2)',
                        result.league,
                        '=IF(G'+next_row+'<K'+next_row+';G'+next_row+';K'+next_row+')',
                        '=IF(G'+next_row+'>K'+next_row+';G'+next_row+';K'+next_row+')',
                        result.home_team + " " + result.home_score + " - " + result.visitor_score + " " + result.visitor_team,
                        '=SPLIT(F'+next_row+';" ")',
                        '',
                        '',
                        '',
                        '',
                        '=IF(H'+next_row+'="*";0;1)',
                        '=IF(L'+next_row+'=0;"*";IF(H'+next_row+'>J'+next_row+';G'+next_row+';K'+next_row+'))',
                        '=IF(L'+next_row+'=1;$H'+next_row+'+$J'+next_row+';"")',
                        '=IF(AND(L'+next_row+'=1;N'+next_row+'>3,5);1;0)',
                        '=IF(AND(L'+next_row+'=1;N'+next_row+'>4,5);1;0)',
                        '=IF(AND(L'+next_row+'=1;N'+next_row+'>5,5);1;0)',
                        '=IF(AND(L'+next_row+'=1;N'+next_row+'>6,5);1;0)',
                        '=IF(AND(L'+next_row+'=1;N'+next_row+'>7,5);1;0)',
                        '=IF(AND(L'+next_row+'=1;N'+next_row+'>8,5);1;0)',
                        '=IF(AND(L'+next_row+'=1;N'+next_row+'>9,5);1;0)'
                    ]
                ],
                raw=False
            )
