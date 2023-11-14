<h1><center>HCM AI CHALLENGE 2023 <br> Event Retrieval from Visual Data</center></h1>

## Setup
```
pip install git+https://github.com/openai/CLIP.git
pip install -r requirements.txt
```

## Download json
- [drive](https://drive.google.com/drive/folders/1WEFCFHa4xfmUjNce5dk0ZEuDry4-BXkf)
- json for object filter [drive object](https://drive.google.com/drive/folders/1yi0LR3XVZwU2RmAyRyycnrW1QXbOrp4V?usp=drive_link). Tải files, để vào dict/:
  - object_all_s_thr05.json
  - object_all_s_thr03.json
  - object_all_s_thr02.json
  - object_all_s_thr01.json
  - object_all_s_thr005.json
  - object_all_s.json

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
## Hướng dẫn cách sử dụng web
```
python3 app.py
```

Sau khi chạy dòng lệnh trên thì trên URL gõ đường link sau: 

Linux: http://0.0.0.0:5001/thumbnailimg?index=0 

Window: http://127.0.0.1:5001/thumbnailimg?index=0

Lúc này trang web sẽ được hiển thị lên màn hình như sau:

![ảnh UI](images/UI.png)

Ở mỗi tấm ảnh có 2 nút **IR** ở bên trái và **select** ở bên phải. Khi chúng ta ấn vào nút **IR** thì sẽ thực hiện chức năng truy vấn ảnh (tìm kiếm ảnh tương đương trong database). Lúc này sẽ xuất hiện thêm 1 tab khác show ra kết quả của truy vấn ảnh.

![KNN](images/knn.png) 

Nút **sellect** sẽ là lựa chọn ảnh đó cùng với shot ảnh của nó để ghi vào file submit 

Ở phần phía trên, nút **Search** dùng để truy vấn text, khi ta nhập câu text query và ấn nút search thì màn hình sẽ trả ra kết quả của những hình ảnh tương đương theo câu truy vấn.

Sau khi chúng ta đã xác định xong việc lựa chọn kết quả thì bấm nút **Download** để thực hiện tải file submit về để submit kết quả lên hệ thống.

Cuối cùng là nhấn nút **Clear** để reset lại file submit dưới hệ thống và tiếp tục thực hiện cho những kết quả tiếp theo.
