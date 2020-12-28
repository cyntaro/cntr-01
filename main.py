import streamlit as st
import requests
import io
from PIL import ImageDraw
from PIL import Image


st.title('顔認識アプリ')

subscription_key = '32dbcc14bef049d5b3c381cdac8c7f53'
assert subscription_key

face_api_url = 'https://cntr2020.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()
        
    headers = {
        'Content-type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,smile'
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()

    for result in results:
        rect = result['faceRectangle']
        fab = result['faceAttributes']
        draw = ImageDraw.Draw(img)
        if fab['gender'] == 'male':
            draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width']), (rect['top']+rect['height'])], fill=None, outline='blue', width=15)
        else:
            draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width']), (rect['top']+rect['height'])], fill=None, outline='pink', width=15)
    st.image(img, caption='Uploaded Image', use_column_width=True)

