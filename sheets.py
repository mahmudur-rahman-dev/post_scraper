import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetsService:
    def __init__(self, json_keyfile_name):
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, self.scope)
        self.client = gspread.authorize(self.creds)

    def get_urls_from_sheet(self, sheet_name, column_number):
        # Open the Google Spreadsheet by its name
        sheet = self.client.open(sheet_name).sheet1

        # Get all values from the column with URLs
        urls = sheet.col_values(column_number)  # replace column_number with the number of the column with URLs

        return urls





# sheets_service = SheetsService('client_secret.json')
# sheet_name = "Your Google Sheet Name"  # replace with your Google Sheet name
# column_number = 1  # replace with the number of the column that contains the URLs
# urls = sheets_service.get_urls_from_sheet(sheet_name, column_number)
#
# for url in urls:
#     result = scrape_linkedin_posts(driver, url)
#     print(len(result))