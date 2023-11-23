from dataclasses import dataclass
from pathlib import Path

import boto3
import requests


@dataclass
class ServerAPI:
    base_url: str = 'https://web.ssnetworks.kr/serverapi' #가산서버
    # base_url: str = 'https://hsg.ssnetworks.kr/serverapi' #횡성서버
    bucket_name: str = 'ssnetworks'
    aws_access_key_id = ""
    aws_secret_access_key = ""
    region_name = "ap-northeast-2"

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )
    s3_client = session.client('s3')
    bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)

    def __get_s3_url(self, file_name: str):
        return f"https://s3-{self.bucket_location['LocationConstraint']}.amazonaws.com/{self.bucket_name}/{file_name}"

    def upload_visitor(
            self,
            file_path: str,
            phone: str,
            created_at: str,
            camera_name: str,
    ):
        file_name = Path(file_path).name
        self.s3_client.upload_file(file_path, self.bucket_name, file_name)
        file_url = self.__get_s3_url(file_name)
        return requests.post(f"{self.base_url}/detected_visitor", json={
            "fileUrl": file_url,
            "phone": phone,
            # "createdAt": created_at,
            "fileName": file_name,
            "cameraName": camera_name,
            "withoutNotification": False,
        })

    def upload_cow_mount(
            self,
            file_path: str,
            phone: str,
            camera_name: str,
            created_at: str=None,
    ):
        file_name = Path(file_path).name
        self.s3_client.upload_file(file_path, self.bucket_name, file_name)
        file_url = self.__get_s3_url(file_name)
        return requests.post(f"{self.base_url}/cow_mount", json={
            "fileUrl": file_url,
            "phone": phone,
            # "createdAt": created_at,
            "fileName": file_name,
            "cameraName": camera_name,
            "withoutNotification": False,
        })


if __name__ == '__main__':
    api = ServerAPI(
        # base_url='http://localhost:3000/serverapi',
    )
    result = api.upload_cow_mount(
        file_path='/data/www/stream/media/01048116262/01048116262_20221106162132_1.jpg',
        camera_name='1',
        created_at='2022-11-06 11:11:11',
        phone="01048116262",
    )
    print(result)
    result2 = api.upload_cow_mount(
        file_path='/data/www/stream/media/01048116262/01048116262_20221106162132_1.jpg',
        camera_name='1',
        #created_at='2022-11-06 11:11:11',
        phone="01048116262",
    )
    print(result2)
