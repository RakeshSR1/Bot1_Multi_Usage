import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class GoogleDriveHelper:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("credentials.json")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile("credentials.json")
        self.drive = GoogleDrive(gauth)

    def upload(self, file_path):
        file_name = os.path.basename(file_path)
        gfile = self.drive.CreateFile({'title': file_name})
        gfile.SetContentFile(file_path)
        gfile.Upload()
        return f"https://drive.google.com/file/d/{gfile['id']}/view?usp=sharing"
