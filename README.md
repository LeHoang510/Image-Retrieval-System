<h1><center>HCM AI CHALLENGE 2023 <br> Event Retrieval from Visual Data</center></h1>

## Setup
```
pip install git+https://github.com/openai/CLIP.git
pip install -r requirements.txt
```

## Download json
- [drive](https://drive.google.com/drive/folders/15-XWSpDOi7oMWmrXz8Vq3OG3DgHqwSuF?usp=drive_link)

## Update for new dataset
- Download new `Keyframes`
- Download [clip-features-vit-b32-b2](https://s3-north1.viettelidc.com.vn/aic23-b1/clip-features-vit-b32-b2.zip) and put them in `dataset/clip-features-vit-b32`
- Download [map-keyframes-b2](https://s3-north1.viettelidc.com.vn/aic23-b9/map-keyframes-b2.zip) and put them in `dataset/map-keyframes-b1`
## Dataset folder
```
├───clip-features-vit-b32
│   └───clip-features-vit-b32
├───Keyframes_L01
│   └───keyframes
│       ├───L01_V001
├───Keyframes_L02
│   └───keyframes
│       ├───L02_V001
....
```
## How to use the app
```
python3 app.py
```

Url for web:

- Linux: http://0.0.0.0:5001/thumbnailimg?index=0 

- Window: http://127.0.0.1:5001/thumbnailimg?index=0

## Feature extraction pipeline
![](/doc/extract.png)

## Video retrieval pipeline
![](/doc/query.png)

## ASR pipeline
![](/doc/asr.png)

## Search mode
- **Text Search mode** is the default mode of our system, allows users to enter a query to search for images. They can also optionally apply object filters to narrow down the results to only include images that contain specific objects. Users can also set a minimum confidence threshold of each object to fine-tune search outcomes. The system also provides two "operators": "and" and "or". The user uses the "and" operator when they want the system to keep only keyframes that contain all of the objects provided by the user. Conversely, if the user requires the system to accept at least one of the objects proposed by the user to appear, they select the "or" option.
- **Sequence Search mode** enables users to input two sequences to search for consecutive images within those sequences.
- **Image Search mode** allows users to enter a keyframe ID to receive the corresponding YouTube link for that image and other related images that are also in the same video. The Submit button is used to send selected data or search results to the backend for processing.
- **Transcript Semantic Search mode** allows users to enter a query and return a list of transcript segments, timestamps, and corresponding videos that are relevant to that query. This mode allows users to search for videos based on their transcripts
- Image Retrieval mode allows users to find keyframes that are similar to a given keyframe. The system uses Faiss to compute the cosine similarity of the given keyframe’s CLIP features vector to the CLIP features vectors of all keyframes in the database. The keyframes with the highest cosine similarity scores are returned as the results.
### Text search

#### 1. without object filter
![](/doc/4.3.example-obj-false.png)

#### 2. with object filter
![](/doc/4.3.example-obj-true.png)

### Sequence search

#### 1. without sequence search
![](/doc/4.3.example-hoang-false.png)

#### 2. with sequence search
![](/doc/4.3.example-hoang-true.png)





