from google.cloud import storage

# TODO move into env vars
GCP_PROJECT_ID = 'project-name'
BUCKET_NAME = 'aibe-audio'
class StorageService:
  def __init__(self) -> None:
    self.storage_client = storage.Client(project=GCP_PROJECT_ID)
    self.bucket = self.storage_client.bucket(BUCKET_NAME)

  def upload(self, filename):
    blob = self.bucket.blob(f'{filename}')
    blob.upload_from_filename(f'tmp/{filename}.wav')


if __name__ == '__main__':
  s = StorageService()
  s.upload()
