from email.mime import image
from tabnanny import check
import streamlit as st
import json
import time
from requests import get, post
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import matplotlib.image as mping
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import PIL
import os
import cv2

endpoint = r"https://check-form-recogn.cognitiveservices.azure.com/"
apim_key = "cae738e5045c4533b4a172f0d80ea137"
model_id = "4e046492-d24a-4088-b6a7-5f4a88bafa15"
post_url = endpoint + "/formrecognizer/v2.1/custom/models/%s/analyze" % model_id
source = r"Check-1.png"
params = {
    "includeTextDetails": True
}

headers = {
    # Request headers
    'Content-Type': 'image/png',
    'Ocp-Apim-Subscription-Key': apim_key,
}
with open(source, "rb") as f:
    data_bytes = f.read()

try:
    resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
    if resp.status_code != 202:
        print("POST analyze failed:\n%s" % json.dumps(resp.json()))
        quit()
    print("POST analyze succeeded:\n%s" % resp.headers)
    get_url = resp.headers["operation-location"]
except Exception as e:
    print("POST analyze failed:\n%s" % str(e))
    quit()
################################################################################################
n_tries = 3
n_try = 0
wait_sec = 2
max_wait_sec = 60
while n_try < n_tries:
    try:
        resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
        resp_json = resp.json()
        if resp.status_code != 200:
            print("GET analyze results failed:\n%s" % json.dumps(resp_json))
            quit()
        status = resp_json["status"]
        if status == "succeeded":
            print("Analysis succeeded:\n%s" % json.dumps(resp_json))
            #quit()
        if status == "failed":
            print("Analysis failed:\n%s" % json.dumps(resp_json))
            quit()
        # Analysis still running. Wait and retry.
        time.sleep(wait_sec)
        n_try += 1
        wait_sec = min(2*wait_sec, max_wait_sec)
    except Exception as e:
        msg = "GET analyze results failed:\n%s" % str(e)
        print(msg)
        #quit()


################################################################################################
data=resp.text
parse_data=json.loads(data)

##############################################################################################

name=parse_data['analyzeResult']['documentResults'][0]['fields']['Name']['valueString']
amount=parse_data['analyzeResult']['documentResults'][0]['fields']['Amount']['valueNumber']
date=parse_data['analyzeResult']['documentResults'][0]['fields']['Date']['valueString']
checkNumber=parse_data['analyzeResult']['documentResults'][0]['fields']['Check number']['valueString']

##################################################################################################

print(name)
