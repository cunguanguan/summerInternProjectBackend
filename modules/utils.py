import os
import uuid

from modules import faceDetect
from modules import tts


def dataURL_to_face_list(token, dataURL):
    """根据摄像头照片dataURL获取识别数据
    """
    image64 = faceDetect.dataURL_to_image64(dataURL)

    result = faceDetect.detect(token, image64)

    # TODO 可以判断一下有没有人脸，再进行下一步操作

    face_list = result['face_list']

    return face_list

def picfile_to_face_list(token, picfile):
    """根据图片文件流获取识别数据
    """
    image64 = faceDetect.picfile_to_image64(picfile)

    result = faceDetect.detect(token, image64)

    # TODO 可以判断一下有没有人脸，再进行下一步操作

    face_list = result['face_list']

    return face_list

def face_to_display_txt(face):
    """给一个face的json信息，输出前端要显示的文字
    """
    if face['expression']['type']=='none':
        expression = '无'
    elif face['expression']['type']=='smile':
        expression = '微笑'
    else:
        expression = '大笑'

    if face['gender']['type']=='male':
        gender = '男'
    else:
        gender = '女'

    if face['glasses']['type']=='none':
        glasses = '没有戴眼镜'
    elif face['glasses']['type']=='common':
        glasses = '戴了普通眼镜'
    else:
        glasses = '戴了墨镜'


    display_txt = {'age':int(face['age']),'beauty':float(face['beauty']),'expression':expression,'gender':gender,'glasses':glasses}

    #返回的字典
    return display_txt

def _face_to_audio_txt(face):
    """给一个face的json信息，输出处理后要说的文本

    Args:
        face: json字典，形如：
            {
            'face_token': 'bc3b6b1b097c02a074ffe51600f05a5d',
            'location': {'left': 149.72, 'top': 203.17, 'width': 195, 'height': 173, 'rotation': -4},
            'face_probability': 1,
            'angle': {'yaw': -3.85, 'pitch': 23.26, 'roll': -5.66},
            'age': 26,
            'beauty': 86.31,
            'expression': {'type': 'none', 'probability': 1},
            'gender': {'type': 'male', 'probability': 1},
            'glasses': {'type': 'none', 'probability': 1}
            }

    """
     if face['expression']['type'] == 'none':
        expression = '无'
    elif face['expression']['type'] == 'smile':
        expression = '微笑'
    else:
        expression = '大笑'

    if face['gender']['type'] == 'male':
        gender = '男'
    else:
        gender = '女'

    if face['glasses']['type'] == 'none':
        glasses = '没有戴眼镜'
    elif face['glasses']['type'] == 'common':
        glasses = '戴了普通眼镜'
    else:
        glasses = '戴了墨镜'
    audio_txt = {'age': '年龄{}岁，'.format(str(face['age'])), 'beauty': '颜值{}分，'.format(str(face['beauty'])),
                 'expression': '表情{}，'.format(expression), 'gender': '性别{}，'.format(gender), 'glasses': glasses}
    return audio_txt

def _save_file(bytes: bytes, suffix):
    """给定文件二进制流和后缀名（不带点），保存文件在statics/files，返回文件名('xxx.mp3')
    """
    fileName = '{}.{}'.format(uuid.uuid4(), suffix)
    fileFullName = os.path.join(os.getcwd(), 'statics/files/', fileName)

    try:
        with open(fileFullName, 'wb') as f:
            f.write(bytes)
        return fileName
    except Exception as e:
        raise e

def faces_to_audio_files(token, face_list):
    """根据人脸json数组获取对应的音频文件存放路径数组。

    先把人脸json数据转换成需要的文本，
    再把文本转换成音频二进制流，
    再把音频存到本地，
    最后返回每个音频的路径构成的数组。
    """

    audio_files = list()
    for face in face_list:
        txt = _face_to_audio_txt(face)
        audio_item = {}
        for key in txt:
            fileName = _save_file(tts.convert(token, txt[key], AUE=3), 'mp3')
            audio_item[key] = fileName
        audio_files.append(audio_item)

    return audio_files
