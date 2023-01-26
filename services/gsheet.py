import pygsheets
import pandas as pd

class GoogleSheetService:
  def __init__(self) -> None:
    gc = pygsheets.authorize(
        service_file='./assets/shine-google-drive.json')
    sh = gc.open('Google Drive')
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

