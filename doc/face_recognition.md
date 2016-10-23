# logic of using facc++ api
1. 发布失踪者，紧急求助：
    - 获得上传的url数据集 face_url_list；
    - 进入 dection/detect 进行人脸检测，获得face_id_list；
    - 将face_id_list 加入一个新的person，等待训练完成.
    - 调用等待方法，等待训练完成，利用第三方进行推送
    - 将face_id_list 加入faceset 进行人脸搜索的训练；异步操作。
2. 上传人脸进行验证，验证置信度：
    - 获得上传的url face_url 和 person_id;
    - 进入 dection/detect 进行人脸检测，获得face_id;
    - 将 获得的face_id 带入 recognition/verify;
    - 返回:
        {
            "confidence": 55.039787, 
            "is_same_person": true, 
            "session_id": "a58bbfc672abce074111166dd9961163"
        }       
3. 摄像头进行人脸搜索：
    - 获得上传的url face_url；
    - 进入 dection/detect 进行人脸检测，获得face_id;
    - 将 获得的 face_id 带入 recognition/earch；
    - 返回
        "candidate": [
        {
            "face_id": "a9cebf8d5ae6fff514d8d2d8e07fa55b", 
            "similarity": 100,
            "tag": ""
        }, 