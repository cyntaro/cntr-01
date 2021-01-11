import streamlit as st
import requests
import io
import json
from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont


st.title('顔認識アプリ')
st.write('jpg or JPGのファイルを読み込めます。')
st.write('顔を認識し、性別と年齢を推測します。')

with open('secret.json') as f:
    secret_json = json.load(f)   
subscription_key = secret_json['subscription_key']
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
        'returnFaceAttributes': 'age,gender'
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()
    fnt = ImageFont.truetype("Arial Bold.ttf", 80)

    for result in results:
        rect = result['faceRectangle']
        fab = result['faceAttributes']
        d = ImageDraw.Draw(img)
        text = str(list(fab.values()))
        if fab['gender'] == 'male':
            d.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width']), (rect['top']+rect['height'])], fill=None, outline='blue', width=15)
            d.text((rect['left'], rect['top']), text, font=fnt, fill=(255,255,255,255))

        else:
            d.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width']), (rect['top']+rect['height'])], fill=None, outline='pink', width=15)
            d.text((rect['left'], rect['top']), text, font=fnt, fill=(255,255,255,255))
    st.image(img, caption='Faces are recognized', use_column_width=True)

