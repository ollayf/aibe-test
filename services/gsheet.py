import pygsheets

# TODO move into env vars
SHEET_NAME = '[SHINE] AIBE test data'


class GoogleSheetService:
    TEAM_DRIVE_ID = '1mchPmcE7q-A3JNTxxcGR15DCF3LPWKOy'
    SHEET_URL = 'https://docs.google.com/spreadsheets/d/1WtnaWtzbJnVSmNuvp7QBbVwDW0__MPoROCpyUT6Z_OI'
    def __init__(self) -> None:
        gc = pygsheets.authorize(
            service_file='credentials.json')
        # gc.enableTeamDriveSupport = True
        # gc.teamDriveId = self.TEAM_DRIVE_ID
        # gc.drive.enable_team_drive(self.TEAM_DRIVE_ID)
        # print(gc.spreadsheet_titles())

        # sh = gc.open(SHEET_NAME)
        sh = gc.open_by_url(self.SHEET_URL)
        self.metadata_sheet = sh[0]
        self.data_sheet = sh[1]

    def _get_total(self):
        total_count = self.metadata_sheet.cell('B1').value
        return total_count

    def increment_total(self):
        self.metadata_sheet.update_value('B1', f'{int(self._get_total()) + 1}')
        return int(self._get_total()) + 1

    def add_result(self, record):
        row = self.increment_total()
        self.data_sheet.update_values(
            f'A{row}:R{row}', record)
