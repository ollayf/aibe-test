from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
import os

class DriveStorageService:
	SCOPE = ['https://www.googleapis.com/auth/drive']
	CREDENTIALS = 'credentials.json'
	TEAM_DRIVE_ID = '1MMX5leAWVZJSSss6e-bSst4khHAl42Et'

	def __init__(self) -> None:
		self.gauth = GoogleAuth()
		self.gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS, self.SCOPE)
		self.drive = GoogleDrive(self.gauth)
	
	def upload(self, filename):
		# filename = os.path.basename(filename)
		if self.gauth.access_token_expired:
			self.gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS, self.SCOPE)
		gfile = self.drive.CreateFile({
			'title': f'{filename}.wav',
			'parents': [{
				'kind': 'drive#fileLink',
				'teamDriveId': self.TEAM_DRIVE_ID,
				'id': self.TEAM_DRIVE_ID
			}]
		})
		gfile.SetContentFile(f'tmp/{filename}.wav')
		gfile.Upload(param={'supportsTeamDrives': True})

if __name__ == '__main__':
	s = DriveStorageService()
	s.upload('a_fat_cat_aaron')