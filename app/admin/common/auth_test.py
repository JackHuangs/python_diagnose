#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 16:38
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : auth_test.py
# @Software: PyCharm
import time
import base64
import hmac


# 生成token 入参：用户id
def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte,'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 验证token 入参：用户id 和 token
def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True


# 用人脸级联分类器引擎进行人脸识别，返回的faces为人脸坐标列表，1.3是放大比例，5是重复识别次数
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.38, minNeighbors=4)
    eye_num = 0
    # 对每一张脸，进行处理操作
    for (x, y, w, h) in faces:
        face_dst = src[y - 10: y + h + 10, x - 10: x + w + 10]
        new_face_name = file_rename("face.jpg", "face")
        face_name = '{}/{}'.format(PROCESSED_URL, new_face_name)
        FACE_ORGAN_URL['face_url'] = STATIC_URL + new_face_name
        cv.imwrite(face_name, face_dst)
        # 画出人脸框，蓝色（BGR色彩体系），画笔宽度为2
        img = cv.rectangle(src, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # 在人脸分割出眼睛区域，节省计算资源
        face_area = img[y:y++h, x:x+w]
        eyes = eye_detector.detectMultiScale(face_area)
        # 人眼识别，返回的eyes为眼睛坐标列表
        for (ex, ey, ew, eh) in eyes:
            eye_dst = face_area[ey - 10: ey + eh + 10, ex - 10: ex + ew + 10]
            new_eye_name = file_rename("eye.jpg", "eye" + str(eye_num))
            eye_name = "{}/{}".format(PROCESSED_URL, new_eye_name)
            if eye_num == 0:
                FACE_ORGAN_URL['left_eye_url'] = STATIC_URL + new_eye_name
            else:
                FACE_ORGAN_URL['right_eye_url'] = STATIC_URL + new_eye_name
            eye_num += 1
            cv.imwrite(eye_name, eye_dst)
            cv.rectangle(face_area, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 1)
        eye_num = 0
        # 鼻子识别
        for (ex, ey, ew, eh) in noses:
            nose_dst = face_area[ey - 10: ey + eh + 10, ex - 10: ex + ew + 10]
            new_nose_name = file_rename("nose.jpg", "nose")
            nose_name = "{}/{}".format(PROCESSED_URL, new_nose_name)
            FACE_ORGAN_URL['nose_url'] = STATIC_URL + new_nose_name
            cv.imwrite(nose_name, nose_dst)
            cv.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
        # 嘴巴识别
        for (ex, ey, ew, eh) in mouths:
            mouth_dst = face_area[ey - 10: ey + eh + 10, ex - 10: ex + ew + 10]
            new_mouth_name = file_rename("mouth.jpg", "mouth")
            mouth_name = "{}/{}".format(PROCESSED_URL, new_mouth_name)
            FACE_ORGAN_URL['mouth_url'] = STATIC_URL + new_mouth_name
            cv.imwrite(mouth_name, mouth_dst)
            cv.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
        # 舌头识别
        for (ex, ey, ew, eh) in faces:
            tongue_dst = face_area[ey - 10: ey + eh + 10, ex - 10: ex + ew + 10]
            new_tongue_name = file_rename("tongue.jpg", "tongue")
            tongue_name = "{}/{}".format(PROCESSED_URL, new_tongue_name)
            FACE_ORGAN_URL['tongue_url'] = STATIC_URL + new_tongue_name
            cv.imwrite(tongue_name, tongue_dst)
            cv.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
