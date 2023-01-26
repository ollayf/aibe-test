from google.cloud import storage


class StorageService:
  def __init__(self) -> None:
    self.storage_client = storage.Client(project='loocurse')
    self.bucket_name = 'aibe-audio'
    self.bucket = self.storage_client.bucket(self.bucket_name)

  def upload(self, filename):
    blob = self.bucket.blob(f'{filename}')
    blob.upload_from_filename(f'tmp/{filename}.wav')


if __name__ == '__main__':
  s = StorageService()
  s.upload()
