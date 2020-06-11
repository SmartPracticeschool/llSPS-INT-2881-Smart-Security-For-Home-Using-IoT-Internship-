import cv2
import numpy as np
import datetime
from speechtotextcode import word
import winsound
#ObjectStorage
import ibm_boto3
from ibm_botocore.client import Config, ClientError

#CloudantDB
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import requests

face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# Constants for IBM COS values
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "2Q01ukIVnfjr1On2DQfWPjtLDoPkxCb__qohxQkDVhOh" # eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/903e0896e820417eb419fb8540c75a32:ff80d312-54c8-45ab-8225-7300f2142c22::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

#Provide CloudantDB credentials such as username,password and url

client = Cloudant("fc30a7e7-a627-4ab6-a09e-f339c0ce40d5-bluemix", "743f1218c74c0cb56c4a60ab4a5b95db5692da4a620aa3a7103df934514b31f3",url="https://fc30a7e7-a627-4ab6-a09e-f339c0ce40d5-bluemix:743f1218c74c0cb56c4a60ab4a5b95db5692da4a620aa3a7103df934514b31f3@fc30a7e7-a627-4ab6-a09e-f339c0ce40d5-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()

#Provide your database name

database_name = "emergencyalert"

my_database = client.create_database(database_name)

if my_database.exists():
   print(f"'{database_name}' successfully created.")



def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))


#It will read the first frame/image of the video
video=cv2.VideoCapture(0)
winsound.Beep(2500,1000)
while word=="help help ":
    #capture the first frame
    check,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    #detect the faces from the video using detectMultiScale function
    faces=face_classifier.detectMultiScale(gray,1.3,5)

    print(faces)
    
    #drawing rectangle boundries for the detected face
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (127,0,255), 2)
        cv2.imshow('Face detection', frame)
        picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        cv2.imwrite(picname+".jpg",frame)
        multi_part_upload("sreejamugada1", picname+".jpg", picname+".jpg")
        json_document={"link":COS_ENDPOINT+"/"+"sreejamugada1"+"/"+picname+".jpg"}
        new_document = my_database.create_document(json_document)
        # Check that the document exists in the database.
        if new_document.exists():
            print(f"Document successfully created.")
        r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=Pg1DKz8AwHGL0ydvitrfxsamoWkIC4O95ZYNbnqechUul62jTR3QjpwZOLDEeutbHBGd1iNmWMc2krUP&sender_id=FSTSMS&message=EMERGENCY ALERT:SOMEONE IS IN DANGER..&language=english&route=p&numbers=8179639950')
        print(r.status_code)


    #waitKey(1)- for every 1 millisecond new frame will be captured
    Key=cv2.waitKey(1)
    if Key==ord('q'):
        #release the camera
        video.release()
        #destroy all windows
        cv2.destroyAllWindows()
        break


