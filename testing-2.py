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


image=plt.imread("Check-1.png")
crop_position= image.shape[0] // 5 
half_image = image[image.shape[0] - crop_position:,:]
fin_img=Image.fromarray((half_image* 255).astype(np. uint8))
fin_img.save('cropped_img.png')

endpoint = "https://check-form-recogn.cognitiveservices.azure.com/"
key ="cae738e5045c4533b4a172f0d80ea137"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Make sure your document's type is included in the list of document types the custom model can analyze
with open(r'cropped_img.png', "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-read", document=f
    )
result = poller.result()
final_String=""
for idx, document in enumerate(result.documents):
    print("--------Analyzing document #{}--------".format(idx + 1))
    print("Document has type {}".format(document.doc_type))
    print("Document has confidence {}".format(document.confidence))
    print("Document was analyzed by model with ID {}".format(result.model_id))
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        print("......found field of type '{}' with value '{}' and with confidence {}".format(field.value_type, field_value, field.confidence))

# iterate over tables, lines, and selection marks on each page
for page in result.pages:
    #print("\nLines found on page {}".format(page.page_number))
    for line in page.lines:
        #print("...Line '{}'".format(line.content))
        final_String+=line.content
    #for word in page.words:
    #   print( "...Word '{}' has a confidence of {}".format(word.content, word.confidence))
    for selection_mark in page.selection_marks:
        print(
            "...Selection mark is '{}' and has a confidence of {}".format(
                selection_mark.state, selection_mark.confidence
            )
        )

for i, table in enumerate(result.tables):
    print("\nTable {} can be found on page:".format(i + 1))
    for region in table.bounding_regions:
        print("...{}".format(i + 1, region.page_number))
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
                cell.row_index, cell.column_index, cell.content
            )
        )
print("-----------------------------------")
if final_String.find("⑈")==0:
    Transit_number=final_String[final_String.find("⑆")+1:final_String.find("⑉")]
    Bank_Code=final_String[final_String.find("⑉")+1:final_String.find("⑆",final_String.find("⑆")+1)]
    Designation_Number=final_String[final_String.find("⑆",final_String.find("⑆")+1)+1:final_String.find("⑉",final_String.find("⑉")+1)]
    Account_number=final_String[final_String.find("⑉",final_String.find("⑉")+1)+1:final_String.find("⑈",final_String.find("⑈",final_String.find("⑈")+1)+1)]
    st.write("Transit Number:- "+str(Transit_number))
    st.write("Bank_Code:- "+str(Bank_Code))
    st.write("Designation Number:- "+str(Designation_Number))
    st.write("Account Number:- "+str(Account_number))
else:
    Routing_number=final_String[final_String.find("⑆")+1:final_String.find("⑆",final_String.find("⑆")+1)]
    Account_number=final_String[final_String.find("⑆",final_String.find("⑆")+1)+1:final_String.find("⑈")]
    accnum=""
    for ch in Account_number:
        if ch.isnumeric():
            accnum+=str(ch)

    st.write("Routing Number:- "+str(Routing_number))
    st.write("Account Number:- "+str(accnum))