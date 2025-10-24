import threading
import jwt
import random
from threading import Thread
import threading
import json
import requests
import google.protobuf
from protobuf_decoder.protobuf_decoder import Parser
import json
import datetime
from datetime import datetime
from google.protobuf.json_format import MessageToJson
import my_message_pb2
import data_pb2
import base64
import logging
import re
import socket
from google.protobuf.timestamp_pb2 import Timestamp
import jwt_generator_pb2
import os
import binascii
import sys
import psutil
import MajorLoginRes_pb2
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import urllib3
from important_zitado import*
from byte import*
tempid = None
sent_inv = False
start_par = False
pleaseaccept = False
nameinv = "none"
idinv = 0
senthi = False
statusinfo = False
tempdata1 = None
tempdata = None
leaveee = False
leaveee1 = False
data22 = None
isroom = False
isroom2 = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def encrypt_packet(plain_text, key, iv):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()
    
def gethashteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['7']
def getownteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['1']

def get_player_status(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)

    if "5" not in parsed_data or "data" not in parsed_data["5"]:
        return "OFFLINE"

    json_data = parsed_data["5"]["data"]

    if "1" not in json_data or "data" not in json_data["1"]:
        return "OFFLINE"

    data = json_data["1"]["data"]

    if "3" not in data:
        return "OFFLINE"

    status_data = data["3"]

    if "data" not in status_data:
        return "OFFLINE"

    status = status_data["data"]

    if status == 1:
        return "SOLO"
    
    if status == 2:
        if "9" in data and "data" in data["9"]:
            group_count = data["9"]["data"]
            countmax1 = data["10"]["data"]
            countmax = countmax1 + 1
            return f"INSQUAD ({group_count}/{countmax})"

        return "INSQUAD"
    
    if status in [3, 5]:
        return "INGAME"
    if status == 4:
        return "IN ROOM"
    
    if status in [6, 7]:
        return "IN SOCIAL ISLAND MODE .."

    return "NOTFOUND"
def get_idroom_by_idplayer(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    idroom = data['15']["data"]
    return idroom
def get_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    leader = data['8']["data"]
    return leader
def generate_random_color():
	color_list = [
    "[00FF00][b][c]",
    "[FFDD00][b][c]",
    "[3813F3][b][c]",
    "[FF0000][b][c]",
    "[0000FF][b][c]",
    "[FFA500][b][c]",
    "[DF07F8][b][c]",
    "[11EAFD][b][c]",
    "[DCE775][b][c]",
    "[A8E6CF][b][c]",
    "[7CB342][b][c]",
    "[FF0000][b][c]",
    "[FFB300][b][c]",
    "[90EE90][b][c]"
]
	random_color = random.choice(color_list)
	return  random_color

def fix_num(num):
    fixed = ""
    count = 0
    num_str = str(num)  # Convert the number to a string

    for char in num_str:
        if char.isdigit():
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0  
    return fixed


def fix_word(num):
    fixed = ""
    count = 0
    
    for char in num:
        if char:
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0  
    return fixed
    
def check_banned_status(player_id):
   
    url = f"http://amin-team-api.vercel.app/check_banned?player_id={player_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data  
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
def send_vvistttt(uid):
    try:
        info_response = newinfo(uid)
        
        if info_response.get('status') != "ok":
            return (
                f"[FF0000]________________________\n"
                f"خطأ في المعرف: {fix_num(uid)}\n"
                f"الرجاء التحقق من الرقم\n"
                f"________________________\n"
                f"WARGOOD OFFICE"
            )
        
        api_url = f"https://add-friend-panel.vercel.app/remove?token=eyJhbGciOiJIUzI1NiIsInN2ciI6IjEiLCJ0eXAiOiJKV1QifQ.eyJhY2NvdW50X2lkIjoxMjE5NDc3OTYwMiwibmlja25hbWUiOiJaSVh-T0ZGSUNJQUwiLCJub3RpX3JlZ2lvbiI6Ik1FIiwibG9ja19yZWdpb24iOiJNRSIsImV4dGVybmFsX2lkIjoiOTRkNzQ0NDkwNTEzMTI1YTZiNjcyYzQyNDViYTY3NGUiLCJleHRlcm5hbF90eXBlIjo0LCJwbGF0X2lkIjowLCJjbGllbnRfdmVyc2lvbiI6IiIsImVtdWxhdG9yX3Njb3JlIjoxMDAsImlzX2VtdWxhdG9yIjp0cnVlLCJjb3VudHJ5X2NvZGUiOiJVUyIsImV4dGVybmFsX3VpZCI6Mzk0NzU5ODgzOSwicmVnX2F2YXRhciI6MTAyMDAwMDA3LCJzb3VyY2UiOjAsImxvY2tfcmVnaW9uX3RpbWUiOjE3NDg2MzM2MjYsImNsaWVudF90eXBlIjoxLCJzaWduYXR1cmVfbWQ1IjoiIiwidXNpbmdfdmVyc2lvbiI6MCwicmVsZWFzZV9jaGFubmVsIjoiIiwicmVsZWFzZV92ZXJzaW9uIjoiT0I0OSIsImV4cCI6MTc1MjE4NTk5Mn0.MgYwMT-1KdiEL48K7L3O_uQogug3ZmnShhK_CxWeEb8&uid={uid}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            return (
                f"{generate_random_color()}________________________\n"
                f"تم حذف الاعب من البوت\n"
                f": {fix_num(uid)}\n"
                f"________________________\n"   
            )
        else:
            return (
                f"[FF0000]________________________\n"
                f"فشل الإرسال (كود الخطأ: {response.status_code})\n"
                f"________________________\n"
            )
            
    except requests.exceptions.RequestException as e:
        return (
            f"[FF0000]________________________\n"
            f"فشل الاتصال بالخادم:\n"
            f"{str(e)}\n"
            f"________________________\n"
        )
        print(error_message)        

    return message
                
def send_vistttt(uid):
    try:
        info_response = newinfo(uid)
        
        if info_response.get('status') != "ok":
            return (
                f"[FF0000]________________________\n"
                f"خطأ في المعرف: {fix_num(uid)}\n"
                f"الرجاء التحقق من الرقم\n"
                f"________________________\n"
                f"WARGOOD OFFICE"
            )
        
        api_url = f"https://add-friend-panel.vercel.app/request?token=eyJhbGciOiJIUzI1NiIsInN2ciI6IjEiLCJ0eXAiOiJKV1QifQ.eyJhY2NvdW50X2lkIjoxMjE5NDc3OTYwMiwibmlja25hbWUiOiJaSVh-T0ZGSUNJQUwiLCJub3RpX3JlZ2lvbiI6Ik1FIiwibG9ja19yZWdpb24iOiJNRSIsImV4dGVybmFsX2lkIjoiOTRkNzQ0NDkwNTEzMTI1YTZiNjcyYzQyNDViYTY3NGUiLCJleHRlcm5hbF90eXBlIjo0LCJwbGF0X2lkIjowLCJjbGllbnRfdmVyc2lvbiI6IiIsImVtdWxhdG9yX3Njb3JlIjoxMDAsImlzX2VtdWxhdG9yIjp0cnVlLCJjb3VudHJ5X2NvZGUiOiJVUyIsImV4dGVybmFsX3VpZCI6Mzk0NzU5ODgzOSwicmVnX2F2YXRhciI6MTAyMDAwMDA3LCJzb3VyY2UiOjAsImxvY2tfcmVnaW9uX3RpbWUiOjE3NDg2MzM2MjYsImNsaWVudF90eXBlIjoxLCJzaWduYXR1cmVfbWQ1IjoiIiwidXNpbmdfdmVyc2lvbiI6MCwicmVsZWFzZV9jaGFubmVsIjoiIiwicmVsZWFzZV92ZXJzaW9uIjoiT0I0OSIsImV4cCI6MTc1MjE4NTk5Mn0.MgYwMT-1KdiEL48K7L3O_uQogug3ZmnShhK_CxWeEb8&uid={uid}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            return (
                f"{generate_random_color()}________________________\n"
                f"تم الإرسال بنجاح للاعب\n"
                f": {fix_num(uid)}\n"
                f"________________________\n"   
            )
        else:
            return (
                f"[FF0000]________________________\n"
                f"فشل الإرسال (كود الخطأ: {response.status_code})\n"
                f"________________________\n"
            )
            
    except requests.exceptions.RequestException as e:
        return (
            f"[FF0000]________________________\n"
            f"فشل الاتصال بالخادم:\n"
            f"{str(e)}\n"
            f"________________________\n"
        )
        print(error_message)        

    return message        

def send_vistttt(uid):
    try:
        # التحقق من صحة ID أولًا
        info_response = newinfo(uid)
        
        if info_response.get('status') != "ok":
            return (
                f"{generate_random_color()}________________________\n"
                f"خطأ في المعرف: {fix_num(uid)}\n"
                f"الرجاء التحقق من الرقم\n"
                f"________________________\n"
                f"GPL TEAM"
            )
        
        # إرسال الطلب إلى API الجديد
        api_url = f"https://ffvisitapi.vercel.app/visit?uid={uid}&region=me&key=free3d"
        response = requests.get(api_url)
        
        # التحقق من استجابة API
        if response.status_code == 200:
            return (
                f"{generate_random_color()}________________________\n"
                f"تم إرسال 1000 زيارة بنجاح ✅\n"
                f"إلى: {fix_num(uid)}\n"
                f"________________________\n"   
            )
        else:
            return (
                f"[FF0000]________________________\n"
                f"فشل الإرسال (كود الخطأ: {response.status_code})\n"
                f"________________________\n"
            )
            
    except requests.exceptions.RequestException as e:
        return (
            f"[FF0000]________________________\n"
            f"فشل الاتصال بالخادم:\n"
            f"{str(e)}\n"
            f"________________________\n"
        )
        print(error_message)        

    return message        


def rrrrrrrrrrrrrr(number):
    if isinstance(number, str) and '***' in number:
        return number.replace('***', '106')
    return number
def newinfo(uid):
    try:
        url = f"https://info-ch9ayfa-production.up.railway.app/{uid}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"Response Data: {data}")  # طباعة البيانات للتحقق منها

            # التحقق من وجود `basicinfo`
            if "basicinfo" in data and isinstance(data["basicinfo"], list) and len(data["basicinfo"]) > 0:
                data["basic_info"] = data["basicinfo"][0]
            else:
                print("Error: 'basicinfo' key not found or empty")
                return {"status": "wrong_id"}

            # التحقق من وجود `claninfo`
            if "claninfo" in data and isinstance(data["claninfo"], list) and len(data["claninfo"]) > 0:
                data["clan_info"] = data["claninfo"][0]
            else:
                data["clan_info"] = "false"

            # التحقق من وجود `clanadmin`
            if "clanadmin" in data and isinstance(data["clanadmin"], list) and len(data["clanadmin"]) > 0:
                data["clan_admin"] = data["clanadmin"][0]  # استخراج أول عنصر
            else:
                data["clan_admin"] = "false"  # تعيين قيمة افتراضية إذا لم يكن هناك مسؤول عشيرة

            return {"status": "ok", "info": data}

        elif response.status_code == 500:
            print("Server Error: 500 - Internal Server Error")
            return {"status": "error", "message": "Server error, please try again later."}

        print(f"Error: Unexpected status code {response.status_code}")
        return {"status": "wrong_id"}

    except Exception as e:
        print(f"Error in newinfo: {str(e)}")
        return {"status": "error", "message": str(e)}
	
import requests

def send_spam(uid):
    try:
        # أولاً، التحقق من صحة المعرف باستخدام دالة newinfo
        info_response = newinfo(uid)
        
        if info_response.get('status') != "ok":
            return (
                f"{generate_random_color()}-----------------------------------\n"
                f"خطأ في المعرف: {fix_num(uid)}\n"
                f"الرجاء التحقق من الرقم\n"
                f"-----------------------------------\n"
            )
        
        # ثانيًا، إرسال الطلب إلى الرابط الصحيح باستخدام المعرف
        api_url = f"https://spam-ch9ayfa-v5-production.up.railway.app/spam?id={uid}"        
        api_url = f"https://spam-ch9ayfa-v5-production.up.railway.app/spam?id={uid}"
        response = requests.get(api_url)

        # ثالثًا، التحقق من نجاح الطلب
        if response.status_code == 200:
            return (
                f"{generate_random_color()}-----------------------------------\n"
                f"تم إرسال طلب صداقة بنجاح ✅\n"
                f"إلى: {fix_num(uid)}\n"
                f"-----------------------------------\n"
            )
        else:
            return (
                f"[FF0000]-----------------------------------\n"
                f"فشل الإرسال (كود الخطأ: {response.status_code})\n"
                f"-----------------------------------\n"
            )
            
    except requests.exceptions.RequestException as e:
        # معالجة أخطاء الاتصال بالشبكة
        return (
            f"[FF0000]-----------------------------------\n"
            f"فشل الاتصال بالخادم:\n"
            f"{str(e)}\n"
            f"-----------------------------------\n"
                    
        )

def attack_profail(player_id):
    url = f"https://ch9ayfa-ban-visit.vercel.app/ban_visit?uid={uid}"
    res = requests.get(url)
    if res.status_code() == 200:
        print("Done-Attack")
    else:
        print("Fuck-Attack")


def talk_with_ai(question):
    url = f"https://princeaiapi.vercel.app/prince/api/v1/ask?key=prince&ask={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "حدث خطأ أثناء الاتصال بالخادم."

def send_likes(uid):
    likes_api_response = requests.get(f"https://likes.ffgarena.cloud/api/v2/likes?uid={uid}&amount_of_likes=100&auth=trial-7d&region=me")
    
    if likes_api_response.status_code == 200:
        api_data = likes_api_response.json()
        
        if api_data.get("LikesGivenByAPI", 0) == 0:
            # حالة الحد اليومي (لون أحمر)
            return {
                "status": "failed",
                "message": (
                    f"{generate_random_color()}تم ارسال 100 لايك بنجاح"

                )
            }
        else:
            # حالة النجاح مع التفاصيل (لون أخضر)
            return {
                "status": "ok",
                "message": (
                    f"[C][B][00FF00]________________________\n"
                    f" ✅ تم إضافة {api_data['LikesGivenByAPI']} إعجاب\n"
                    f" الاسم: {api_data['PlayerNickname']}\n"
                    f" الإعجابات السابقة: {api_data['LikesbeforeCommand']}\n"
                    f" الإعجابات الجديدة: {api_data['LikesafterCommand']}\n"
                    f"________________________"
                )
            }
    else:
        # حالة الفشل العامة (لون أحمر)
        return {
            "status": "failed",
            "message": (
                f"{generate_random_color()}________________________\n"
                f" ❌ خطأ في الإرسال!\n"
                f" تأكد من صحة اليوزر ID\n"
                f"________________________"
            )
        }
def Encrypt(number):
    number = int(number)  # تحويل الرقم إلى عدد صحيح
    encoded_bytes = []    # إنشاء قائمة لتخزين البايتات المشفرة

    while True:  # حلقة تستمر حتى يتم تشفير الرقم بالكامل
        byte = number & 0x7F  # استخراج أقل 7 بتات من الرقم
        number >>= 7  # تحريك الرقم لليمين بمقدار 7 بتات
        if number:
            byte |= 0x80  # تعيين البت الثامن إلى 1 إذا كان الرقم لا يزال يحتوي على بتات إضافية

        encoded_bytes.append(byte)
        if not number:
            break  # التوقف إذا لم يتبقى بتات إضافية في الرقم

    return bytes(encoded_bytes).hex()
    


def get_random_avatar():
	avatar_list = [
        '902000306'
    ]
	random_avatar = random.choice(avatar_list)
	return  random_avatar
##########################################	
class FF_CLIENT(threading.Thread):
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.key = None
        self.iv = None
        self.get_tok()                 
    def connect(self, tok, host, port, packet, key, iv):
        global clients
        clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(port)
        clients.connect((host, port))
        clients.send(bytes.fromhex(tok))

        while True:
            data = clients.recv(9999)
            if data == b"":
                print("Connection closed by remote host")
                break
def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None
def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
    return final_result

def encrypt_message(plaintext):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return binascii.hexlify(encrypted_message).decode('utf-8')

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def extract_jwt_from_hex(hex):
    byte_data = binascii.unhexlify(hex)
    message = jwt_generator_pb2.Garena_420()
    message.ParseFromString(byte_data)
    json_output = MessageToJson(message)
    token_data = json.loads(json_output)
    return token_data
    

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def restart_program():
    p = psutil.Process(os.getpid())
    open_files = p.open_files()
    connections = psutil.net_connections()
    for handler in open_files:
        try:
            os.close(handler.fd)
        except Exception:
            pass
            
    for conn in connections:
        try:
            conn.close()
        except Exception:
            pass
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    python = sys.executable
    os.execl(python, python, *sys.argv)
          
class FF_CLIENT(threading.Thread):
    def __init__(self, id, password):
        super().__init__()
        self.id = id
        self.password = password
        self.key = None
        self.iv = None
        self.get_tok()

    def parse_my_message(self, serialized_data):
        try:
            MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
            MajorLogRes.ParseFromString(serialized_data)
            key = MajorLogRes.ak
            iv = MajorLogRes.aiv
            if isinstance(key, bytes):
                key = key.hex()
            if isinstance(iv, bytes):
                iv = iv.hex()
            self.key = key
            self.iv = iv
            print(f"Key: {self.key} | IV: {self.iv}")
            return self.key, self.iv
        except Exception as e:
            print(f"{e}")
            return None, None

    def nmnmmmmn(self, data):
        key, iv = self.key, self.iv
        try:
            key = key if isinstance(key, bytes) else bytes.fromhex(key)
            iv = iv if isinstance(iv, bytes) else bytes.fromhex(iv)
            data = bytes.fromhex(data)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = cipher.encrypt(pad(data, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            print(f"Error in nmnmmmmn: {e}")

    def spam_room(self, idroom, idplayer):
        fields = {
        1: 78,
        2: {
            1: int(idroom),
            2: "iG:[C][B][FF0000]3[FF00FF]m[00FFFF]k[00FF00]_eg",
            4: 330,
            5: 6000,
            6: 201,
            10: int(get_random_avatar()),
            11: int(idplayer),
            12: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def send_squad(self, idplayer):
        fields = {
            1: 33,
            2: {
                1: int(idplayer),
                2: "ME",
                3: 1,
                4: 1,
                7: 330,
                8: 19459,
                9: 100,
                12: 1,
                16: 1,
                17: {
                2: 94,
                6: 11,
                8: "1.109.5",
                9: 3,
                10: 2
                },
                18: 201,
                23: {
                2: 1,
                3: 1
                },
                24: int(get_random_avatar()),
                26: {},
                28: {}
            }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final +  self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final +  self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final +  self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final +  self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def start_autooo(self):
        fields = {
        1: 9,
        2: {
            1: 11497463104
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)    
        prefix = "051500" + "0" * (6 - len(header_lenth_final))
        final_packet = prefix + header_lenth_final +  self.nmnmmmmn(packet)   
        return bytes.fromhex(final_packet)
    def invite_skwad(self, idplayer):
        fields = {
        1: 2,
        2: {
            1: int(idplayer),
            10: int(get_random_avatar()),
            2: "ME",
            4: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)   
        prefix = "051500" + "0" * (6 - len(header_lenth_final))
        final_packet = prefix + header_lenth_final +  self.nmnmmmmn(packet)   
        return bytes.fromhex(final_packet)
    def request_skwad(self, idplayer):
        fields = {
        1: 33,
        2: {
            1: int(idplayer),
            2: "ME",
            3: 1,
            4: 1,
            7: 330,
            8: 19459,
            9: 100,
            12: 1,
            16: 1,
            17: {
            2: 94,
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
            18: 201,
            23: {
            2: 1,
            3: 1
            },
            24: int(get_random_avatar()),
            26: {},
            28: {}
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)   
        prefix = "051500" + "0" * (6 - len(header_lenth_final))
        final_packet = prefix + header_lenth_final +  self.nmnmmmmn(packet)    
        return bytes.fromhex(final_packet)
    def skwad_maker(self):
        fields = {
        1: 1,
        2: {
            2: "\u0001",
            3: 1,
            4: 1,
            5: "en",
            9: 1,
            11: 1,
            13: 1,
            14: {
            2: 5756,
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)        
        prefix = "051500" + "0" * (6 - len(header_lenth_final))
        final_packet = prefix + header_lenth_final +  self.nmnmmmmn(packet)        
        return bytes.fromhex(final_packet)
    def changes(self, num):
        fields = {
        1: 17,
        2: {
            1: 11371687918,
            2: 1,
            3: int(num),
            4: 62,
            5: "\u001a",
            8: 5,
            13: 329
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
   
    def leave_s(self):
        fields = {
        1: 7,
        2: {
            1: 11371687918
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def leave_room(self, idroom):
        fields = {
        1: 6,
        2: {
            1: int(idroom)
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def stauts_infoo(self, idd):
        fields = {
        1: 7,
        2: {
            1: 11371687918
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
        #print(Besto_Packet)
    def GenResponsMsg(self, Msg, Enc_Id):
        fields = {
            1: 1,
            2: {
                1: 12947146032,
                2: Enc_Id,
                3: 2,
                4: str(Msg),
                5: int(datetime.now().timestamp()),
                7: 2,
                9: {
                    1: "STEVE", 
                    2: int(get_random_avatar()),
                    3: 901049014,
                    4: 330,
                    5: int(get_random_avatar()),
                    8: "GUILD|Friend",
                    10: 1,
                    11: random.choice([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
                    13: {
                        1: 2,
                        2: 1,
                    },
                    14: {
                        1: 11017917409,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    }
                },
                10: "vn",
                13: {
                    1: "https://graph.facebook.com/v9.0/253082355523299/picture?width=160&height=160",
                    2: 1,
                    3: 1
                },
                14: {
                    1: {
                        1: random.choice([1, 4]),
                        2: 1,
                        3: random.randint(1, 180),
                        4: 1,
                        5: int(datetime.now().timestamp()),
                        6: "VN"
                    }
                }
            }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv)) // 2
        header_lenth_final = dec_to_hex(header_lenth)

        if len(header_lenth_final) == 2:
            final_packet = "1215000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "121500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "12150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "1215000" + header_lenth_final + self.nmnmmmmn(packet)

        return bytes.fromhex(final_packet)
    def createpacketinfo(self, idddd):
        ida = Encrypt(idddd)
        packet = f"080112090A05{ida}1005"
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0F15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0F1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0F150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0F15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def accept_sq(self, hashteam, idplayer, ownerr):
        fields = {
        1: 4,
        2: {
            1: int(ownerr),
            3: int(idplayer),
            4: "\u0001\u0007\t\n\u0012\u0019\u001a ",
            8: 1,
            9: {
            2: 1393,
            4: "fds",
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
            10: hashteam,
            12: 1,
            13: "en",
            16: "OR"
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def info_room(self, idrooom):
        fields = {
        1: 1,
        2: {
            1: int(idrooom),
            3: {},
            4: 1,
            6: "en"
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def sockf1(self, tok, online_ip, online_port, packet, key, iv):
        global socket_client
        global sent_inv
        global tempid
        global start_par
        global clients
        global pleaseaccept
        global tempdata1
        global nameinv
        global idinv
        global senthi
        global statusinfo
        global tempdata
        global data22
        global leaveee
        global isroom
        global isroom2
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        online_port = int(online_port)

        socket_client.connect((online_ip,online_port))
        print(f" Con port {online_port} Host {online_ip} ")
        print(tok)
        socket_client.send(bytes.fromhex(tok))
        while True:
            data2 = socket_client.recv(9999)
            print(data2)
            if "0500" in data2.hex()[0:4]:
                accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                kk = get_available_room(accept_packet)
                parsed_data = json.loads(kk)
                fark = parsed_data.get("4", {}).get("data", None)
                if fark is not None:
                    print(f"haaaaaaaaaaaaaaaaaaaaaaho {fark}")
                    if fark == 18:
                        if sent_inv:
                            accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                            print(accept_packet)
                            print(tempid)
                            aa = gethashteam(accept_packet)
                            ownerid = getownteam(accept_packet)
                            print(ownerid)
                            print(aa)
                            ss = self.accept_sq(aa, tempid, int(ownerid))
                            socket_client.send(ss)
                            sleep(1)
                            startauto = self.start_autooo()
                            socket_client.send(startauto)
                            start_par = False
                            sent_inv = False
                    if fark == 6:
                        leaveee = True
                        print("kaynaaaaaaaaaaaaaaaa")
                    if fark == 50:
                        pleaseaccept = True
                print(data2.hex())

            if "0600" in data2.hex()[0:4] and len(data2.hex()) > 700:
                    accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                    kk = get_available_room(accept_packet)
                    parsed_data = json.loads(kk)
                    print(parsed_data)
                    idinv = parsed_data["5"]["data"]["1"]["data"]
                    nameinv = parsed_data["5"]["data"]["3"]["data"]
                    senthi = True
            if "0f00" in data2.hex()[0:4]:
                packett = f'08{data2.hex().split("08", 1)[1]}'
                print(packett)
                kk = get_available_room(packett)
                parsed_data = json.loads(kk)
                
                asdj = parsed_data["2"]["data"]
                tempdata = get_player_status(packett)
                if asdj == 15:
                    if tempdata == "OFFLINE":
                        tempdata = f"The id is {tempdata}"
                    else:
                        idplayer = parsed_data["5"]["data"]["1"]["data"]["1"]["data"]
                        idplayer1 = fix_num(idplayer)
                        if tempdata == "IN ROOM":
                            idrooom = get_idroom_by_idplayer(packett)
                            idrooom1 = fix_num(idrooom)
                            
                            tempdata = f"id : {idplayer1}\nstatus : {tempdata}\nid room : {idrooom1}"
                            data22 = packett
                            print(data22)
                            
                        if "INSQUAD" in tempdata:
                            idleader = get_leader(packett)
                            idleader1 = fix_num(idleader)
                            tempdata = f"id : {idplayer1}\nstatus : {tempdata}\nleader id : {idleader1}"
                        else:
                            tempdata = f"id : {idplayer1}\nstatus : {tempdata}"
                    statusinfo = True 

                    print(data2.hex())
                    print(tempdata)
                
                    

                else:
                    pass
            if "0e00" in data2.hex()[0:4]:
                packett = f'08{data2.hex().split("08", 1)[1]}'
                print(packett)
                kk = get_available_room(packett)
                parsed_data = json.loads(kk)
                idplayer1 = fix_num(idplayer)
                asdj = parsed_data["2"]["data"]
                tempdata1 = get_player_status(packett)
                if asdj == 14:
                    nameroom = parsed_data["5"]["data"]["1"]["data"]["2"]["data"]
                    
                    maxplayer = parsed_data["5"]["data"]["1"]["data"]["7"]["data"]
                    maxplayer1 = fix_num(maxplayer)
                    nowplayer = parsed_data["5"]["data"]["1"]["data"]["6"]["data"]
                    nowplayer1 = fix_num(nowplayer)
                    tempdata1 = f"{tempdata}\nRoom name : {nameroom}\nMax player : {maxplayer1}\nLive player : {nowplayer1}"
                    print(tempdata1)
                    

                    
                
                    
            if data2 == b"":
                
                print("Connection closed by remote host")
                restart_program()
                break
    
    
    def connect(self, tok, packet, key, iv, whisper_ip, whisper_port, online_ip, online_port):
        global clients
        global socket_client
        global sent_inv
        global tempid
        global leaveee
        global start_par
        global nameinv
        global idinv
        global senthi
        global statusinfo
        global tempdata
        global pleaseaccept
        global tempdata1
        global data22
        clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clients.connect((whisper_ip, whisper_port))
        clients.send(bytes.fromhex(tok))
        thread = threading.Thread(
            target=self.sockf1, args=(tok, online_ip, online_port, "anything", key, iv)
        )
        threads.append(thread)
        thread.start()

        while True:
            data = clients.recv(9999)

            if data == b"":
                print("Connection closed by remote host")
                break
                print(f"Received data: {data}")
            
            if senthi == True:
                
                clients.send(
                        self.GenResponsMsg(
                            f"""[C][B][1E90FF]╔══════════════════════════╗
[FFFFFF]مرحبًا! شكرًا لإضافتي.
[FFFFFF]لمعرفة الأوامر المتاحة،
[FFFFFF]أرسل أي  إيموجي.
[1E90FF]╠══════════════════════════╣
[FFFFFF]هل أنت مهتم بشراء البوت
[FFFFFF]تواصل مع المطور:
[FFD700]تيليغرام: @O000000000000o_X_o000000000000O
[1E90FF]╚══════════════════════════╝""", idinv
                        )
                )
                senthi = False
            
            
##########################################            
            if "1200" in data.hex()[0:4]:
               
                json_result = get_available_room(data.hex()[10:])
                print(data.hex())
                parsed_data = json.loads(json_result)
                try:
                	uid = parsed_data["5"]["data"]["1"]["data"]
                except KeyError:
                	print("Warning: '1' key is missing in parsed_data, skipping...")
                	uid = None  # تعيين قيمة افتراضية
                if "8" in parsed_data["5"]["data"] and "data" in parsed_data["5"]["data"]["8"]:
                    uexmojiii = parsed_data["5"]["data"]["8"]["data"]
                    if uexmojiii == "DefaultMessageWithKey":
                        pass
                    else:
                        clients.send(
                            self.GenResponsMsg(
                            f"""{generate_random_color()}━━━━━━━━━━━━━━━
{generate_random_color()}: ฬєlς๏๓є t๏ ƂΡL ๒๏t ρг๏ 

{generate_random_color()}تيليجرام:  @likeaddlike1
{generate_random_color()}تيليغرام: @O000000000000o_X_o000000000000O

[b][999999]أيت الأوامر؟ أرسل:
{generate_random_color()}++😄N6


[b][999999]━━━━━━━━━━━━━━━
[C][B] [fa95ff]by >صححصححصححصحح
""",uid

                            
                            )
                            
                        )
                else:
                    pass  
            if "1200" in data.hex()[0:4] and b"@SET" in data:
                i = re.split("@SET", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                json_result = get_available_room(data.hex()[10:])
                
                parsed_data = json.loads(json_result)
                uid = parsed_data["5"]["data"]["1"]["data"]
                clients.send(
                    self.GenResponsMsg(
                        f"""#FFHUDT6O3jofy4oxPo7eO""", uid
                    )
                )
            if "1200" in data.hex()[0:4] and b"@gt" in data:
                    try:
                        # استخراج المعرف من الأمر
                        command_split = re.split("@gt", str(data))
                        if len(command_split) > 1:
                            player_id = command_split[1].split('(')[0].strip()

                            # استخراج بيانات المرسل
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]

                            # إرسال رسالة تأكيد
                            clients.send(
                                self.GenResponsMsg(
                                    f"{generate_random_color()}🚀 جاري بدء السبام السولو...", uid
                                )
                            )

                            # عدد مرات التكرار
                            spam_count = 50

                            for i in range(spam_count):
                                try:
                                    # 1. فتح سكواد جديد
                                    packetmaker = self.skwad_maker()
                                    socket_client.send(packetmaker)
                                    time.sleep(0.01)

                                    # 2. إرسال دعوة للاعب
                                    invitess = self.invite_skwad(player_id)
                                    socket_client.send(invitess)
                                    time.sleep(0.01)

                                    # 3. مغادرة السكواد بسرعة
                                    leavee = self.leave_s()
                                    socket_client.send(leavee)
                                    time.sleep(0.01)

                                    # 4. العودة للوضع الفردي
                                    change_to_solo = self.changes(1)
                                    socket_client.send(change_to_solo)
                                    time.sleep(0.01)

                                except Exception as e:
                                    print(f"Error in spam loop: {e}")
                                    
                                    continue

                            # إرسال رسالة انتهاء
                            clients.send(
                                self.GenResponsMsg(
                                    f"{generate_random_color()}✅ تم إرسال {spam_count} دعوة سولو!\n"
                                    f"إلى اللاعب: {player_id}", uid
                                )
                            )

                        else:
                            # إذا لم يتم إدخال المعرف
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]

                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][FF0000]يرجى إدخال معرف اللاعب بعد الأمر\nمثال: @gt 12345678", uid
                                )
                            )

                    except Exception as e:
                        print(f"Error in @gt command: {e}")
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]

                        clients.send(
                            self.GenResponsMsg(
                                f"[C][B][FF0000]حدث خطأ في السبام السولو!", uid
                            )
                        )
            if "1200" in data.hex()[0:4] and b"+ms" in data:

                 json_result = get_available_room(data.hex()[10:])
                 parsed_data = json.loads(json_result)
                 uid = parsed_data["5"]["data"]["1"]["data"]
                 try:
                     decoded_data = data.decode('utf-8')
                 except UnicodeDecodeError:
                     decoded_data = data.decode('latin-1')
                     print(f"Decoded data: {decoded_data}")
                 if "+ms " in decoded_data:
                     message = decoded_data.split("+ms ")[1]
                     message = message.split("\n")[0]
                     print(f"Raw message: {message}")
                     cleaned_message = re.sub(r'\s*[\(\)]|\s*\([^()]*\)\s*', '', re.sub(r'[^\x20-\x7E]+', '', message)).strip().replace('J5', '')
                     print(f"Cleaned message: {cleaned_message}")
                     print(f"Final cleaned message: {cleaned_message}")
                     for i in range(1, len(cleaned_message) + 1):
                         partial_message = cleaned_message[:i]
                         clients.send(
                    self.GenResponsMsg(
                    f"{generate_random_color()}{partial_message}", uid
                    )
                )
                         time.sleep(0.5)
                     
                     
                 ####
                 
            if "1200" in data.hex()[0:4] and b"/dev" in data:
                i = re.split("@dev", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                json_result = get_available_room(data.hex()[10:])
                
                parsed_data = json.loads(json_result)
                uid = parsed_data["5"]["data"]["1"]["data"]
                clients.send(
                    self.GenResponsMsg(
                        f"""{generate_random_color()}━━━━━━━━━━━━━━━
{generate_random_color()}: ฬєlς๏๓є t๏ صححصححصححصححصححصحح ๒๏t VIP

[C][B] [fa95ff]المطور ستيفي لتواصل او الاستفسار ؟؟

{generate_random_color()}تيليجرام:  @Chef_wargood
{generate_random_color()}إنستجرام: @wargood_officiel

[b][999999]━━━━━━━━━━━━━━━
[C][B] [fa95ff]by >صححصححصححصحح + N6 <""", uid
                    )
                )

            if "1200" in data.hex()[0:4] and b"@spy" in data:
                try:
                    command_split = re.split("@spy ", str(data))
                    if len(command_split) > 1:
                        player_id = command_split[1].split('(')[0].strip()
                        if "***" in player_id:
                            player_id = player_id.replace("***", "106")                            
                            
                            
                    
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        clients.send(
                            self.GenResponsMsg(
                                f"[C][B][1E90FF] جاري ارسال سبام طلبات انضمام"                              , uid
                            )
                        )                            

                        
                        json_result = get_available_room(data.hex()[10:])
                        
                        parsed_data = json.loads(json_result)

                        tempid = player_id
                        
                        def send_invite():
                            invskwad = self.request_skwad(player_id)
                            socket_client.send(invskwad)                         

                       


                        threadss = []
                        for _ in range(30):
                            thread = threading.Thread(target=send_invite)
                            thread.start()
                            threadss.append(thread)                                                        
                        
                        for thread in threadss:
                            thread.join()

                        sent_inv = True

                    
                    
                      
                except Exception as e:
                    print(f"Error in /md command: {e}")


            if "1200" in data.hex()[0:4] and b"@x3" in data:
                pass
                # يแยก i من الأمر /3
                i = re.split("@x3", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                
                # استخراج بيانات اللاعب المرسل
                json_result = get_available_room(data.hex()[10:])
                parsed_data = json.loads(json_result)
                uid = parsed_data["5"]["data"]["1"]["data"]

                # 1. إنشاء فريق جديد
                packetmaker = self.skwad_maker()
                socket_client.send(packetmaker)
                sleep(0.5)  # انتظر قليلاً لضمان إنشاء الفريق

                # 2. تغيير وضع الفريق إلى 3 لاعبين (2 = 3-1)
                packetfinal = self.changes(2)
                socket_client.send(packetfinal)
                sleep(0.5)

                # 3. التحقق مما إذا كان هناك ID لدعوته
                room_data = None
                if b'(' in data:
                    split_data = data.split(b'@x5')
                    if len(split_data) > 1:
                        room_data = split_data[1].split(
                            b'(')[0].decode().strip().split()
                        if room_data:
                            iddd = room_data[0]
                            # إرسال دعوة للاعب المحدد
                            invitess = self.invite_skwad(iddd)
                            socket_client.send(invitess)
                        else:
                            # إذا لم يتم تحديد ID، يتم دعوة الشخص الذي أرسل الأمر
                            iddd = uid
                            invitess = self.invite_skwad(iddd)
                            socket_client.send(invitess)

                # 4. إرسال رسالة تأكيد للمستخدم
                if uid:
                    clients.send(
                        self.GenResponsMsg(
                            f"{generate_random_color()}\n\n\n\nجاري  تحويل الفريق الي  ثلاثي\n\n\n\n",
                            uid
                        )
                    )

                # 5. مغادرة الفريق وتغيير الوضع إلى فردي (Solo) بعد فترة
                sleep(2)  # انتظر 5 ثوانٍ
                leavee = self.leave_s()
                socket_client.send(leavee)
                sleep(0.5)
                change_to_solo = self.changes(1)
                socket_client.send(change_to_solo)
                    
            if "1200" in data.hex()[0:4] and b"@x5" in data:   
                pass
                i = re.split("@x5", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                json_result = get_available_room(data.hex()[10:])
                parsed_data = json.loads(json_result)

                # إنشاء الفريق
                packetmaker = self.skwad_maker()
                socket_client.send(packetmaker)

                sleep(0.5)

                # تعيين نوع الفريق
                packetfinal = self.changes(4)
                socket_client.send(packetfinal)

                room_data = None
                if b'(' in data:
                    split_data = data.split(b'@x5')
                    if len(split_data) > 1:
                        room_data = split_data[1].split(
                            b'(')[0].decode().strip().split()
                        if room_data:
                            iddd = room_data[0]
                        else:
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            iddd = parsed_data["5"]["data"]["1"]["data"]

                # إرسال الدعوة
                invitess = self.invite_skwad(iddd)
                socket_client.send(invitess)

                if uid:
                    clients.send(
                        self.GenResponsMsg(
                            f"{generate_random_color()}\n\n\n\nجاري  تحويل الفريق الي  خماسي\n\n\n\n",
                            
                            uid))

                # التأكد من المغادرة بعد 5 ثوانٍ إذا لم تتم المغادرة تلقائيًا
                sleep(2)
                print("Checking if still in squad...")

                leavee = self.leave_s()
                socket_client.send(leavee)

                # تأخير أطول للتأكد من تنفيذ المغادرة قبل تغيير الوضع
                sleep(1)

                # إرسال أمر تغيير وضع اللعبة إلى Solo
                change_to_solo = self.changes(1)  # تأكد أن `1` هو القيمة الصحيحة لـ Solo
                socket_client.send(change_to_solo)

                # تأخير بسيط قبل إرسال التأكيد للمستخدم

                 

                
                    
            if "1200" in data.hex()[0:4] and b"@x6" in data:
                pass                
                i = re.split("@x6", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                json_result = get_available_room(data.hex()[10:])
                parsed_data = json.loads(json_result)
                packetmaker = self.skwad_maker()
                socket_client.send(packetmaker)
                sleep(0.5)
                packetfinal = self.changes(5)
                room_data = None
                if b'(' in data:
                    split_data = data.split(b'@x6')
                    if len(split_data) > 1:
                        room_data = split_data[1].split(
                            b'(')[0].decode().strip().split()
                        if room_data:
                            iddd = room_data[0]
                        else:
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            iddd = parsed_data["5"]["data"]["1"]["data"]
                socket_client.send(packetfinal)
                invitess = self.invite_skwad(iddd)
                socket_client.send(invitess)
                if uid:
                    clients.send(
                        self.GenResponsMsg(
                            f"{generate_random_color()}\n\n\n\nجاري  تحويل الفريق الي  سداسي\n\n\n\n",
                            uid))

                sleep(2)  # انتظار 2 ثواني
                leavee = self.leave_s()
                socket_client.send(leavee)
                sleep(0.5)
                change_to_solo = self.changes(1)  # تغيير إلى Solo
                socket_client.send(change_to_solo)
            if "1200" in data.hex()[0:4] and b"@AIM" in data:
                i = re.split("@AIM", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                json_result = get_available_room(data.hex()[10:])
                
                parsed_data = json.loads(json_result)
                uid = parsed_data["5"]["data"]["1"]["data"]
                clients.send(
                    self.GenResponsMsg(
                                            f"""
                                            [FFFFFF][b][c]✨ أهلًا بك! اليك اقوى حساسيه ✨
                                            
لعام :
>200<
نقطه حمراء :
>7<
عدسه 2 :
>186<
عدسه 4 :
>177<
عدسه قناصه :
>156<
زر الاطلاق :
>30-40<
""",uid
                            )
                        )
            if "1200" in data.hex()[0:4] and b"@s" in data:
                try:
                    print("Received @st command")
                    i = re.split("@s", str(data))[1]
                    if "***" in i:
                        i = i.replace("***", "106")
                    sid = str(i).split("(\\x")[0]
                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    split_data = re.split(rb'/status', data)
                    room_data = split_data[1].split(b'(')[0].decode().strip().split()
                    if room_data:
                        player_id = room_data[0]
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        packetmaker = self.createpacketinfo(player_id)
                        socket_client.send(packetmaker)
                        statusinfo1 = True
                        while statusinfo1:
                            if statusinfo == True:
                                if "IN ROOM" in tempdata:
                                    inforoooom = self.info_room(data22)
                                    socket_client.send(inforoooom)
                                    sleep(0.5)
                                    clients.send(self.GenResponsMsg(f"{tempdata1}", uid))  
                                    tempdata = None
                                    tempdata1 = None
                                    statusinfo = False
                                    statusinfo1 = False
                                else:
                                    clients.send(self.GenResponsMsg(f"{tempdata}", uid))  
                                    tempdata = None
                                    tempdata1 = None
                                    statusinfo = False
                                    statusinfo1 = False
                    else:
                        clients.send(self.GenResponsMsg("[C][B][FF0000] الرجاء إدخال معرف اللاعب!", uid))  
                except Exception as e:
                    print(f"Error in @rs command: {e}")
                    clients.send(self.GenResponsMsg("[C][B][FF0000]ERROR!", uid))
                  

                    
            if "1200" in data.hex()[0:4] and b"@r" in data:
                	i = re.split("@r", str(data))[1] 
                	sid = str(i).split("(\\x")[0]
                	json_result = get_available_room(data.hex()[10:])
                	parsed_data = json.loads(json_result)
                	uid = parsed_data["5"]["data"]["1"]["data"]
                	split_data = re.split(rb'/room', data)
                	room_data = split_data[1].split(b'(')[0].decode().strip().split()
                	if room_data and len(room_data) > 0:
                    		player_id = room_data[0]
                    
                    		if not any(char.isdigit() for char in player_id):
                    			clients.send(self.GenResponsMsg(f"[C][B][ff0000] - Error! ", uid))
                    		else:
                    			player_id = room_data[0]
                    		if player_id.isdigit():
                        		if "***" in player_id:
                            			player_id = rrrrrrrrrrrrrr(player_id)                        			
                        		packetmaker = self.createpacketinfo(player_id)
                        		socket_client.send(packetmaker)
                        		sleep(0.5)
                        		if "IN ROOM" in tempdata:
                            			room_id = get_idroom_by_idplayer(data22)
                            			packetspam = self.spam_room(room_id, player_id)
                            			print(packetspam.hex())
                            			clients.send(
                                self.GenResponsMsg(
                                    f"\n{generate_random_color()}- SpAm StArtEd For uid {fix_num(player_id)} !\n", uid
                                )
                            )
                            
                            
                            			for _ in range(10):
                                			packetspam = self.spam_room(room_id, player_id)

                                			print(" sending spam to "+player_id)
                                			threading.Thread(target=socket_client.send, args=(packetspam,)).start()
                            			clients.send(
                                self.GenResponsMsg(
                                    f"\n\n\n{generate_random_color()} [00FF00]Successfully Spam SeNt !\n\n\n", uid
                                )
                            )
                        		else:
                        		      clients.send(
                                self.GenResponsMsg(
                                    f"\n\n\n[C][B] [FF00FF]The player is not in room\n\n\n", uid
                                )
                            )      
                    		else:
                    		      clients.send(
                            self.GenResponsMsg(
                                f"\n\n\n[C][B] [FF00FF]Please write the id of player not!\n\n\n", uid
                            )
                        )   
                	else:
                	       clients.send(
                        self.GenResponsMsg(
                            f"\n\n\n[C][B] [FF00FF]Please write the id of player !\n\n\n", uid
                        )
                    )                          

            if "1200" in data.hex()[0:4] and b"WELCOME TO GPL BOT" in data:
            	pass
            else:                          
	            if "1200" in data.hex()[0:4] and b"@spm" in data:
	                
	                command_split = re.split("@spm", str(data))
	                if len(command_split) > 1:
	                    player_id = command_split[1].split('(')[0].strip()
	                    print(f"Sending Spam To {player_id}")
	                    json_result = get_available_room(data.hex()[10:])
	                    parsed_data = json.loads(json_result)
	                    uid = parsed_data["5"]["data"]["1"]["data"]
	                    clients.send(
	                    self.GenResponsMsg(
	                        f"{generate_random_color()}جاري ارسال طلبات الصداقه..", uid
	                    )
	                )
	                    
	                    message = send_spam(player_id)
	                    print(message)
	                    json_result = get_available_room(data.hex()[10:])
	                    parsed_data = json.loads(json_result)
	                    uid = parsed_data["5"]["data"]["1"]["data"]
	                    
	                    clients.send(self.GenResponsMsg(message, uid))
	            if "1200" in data.hex()[0:4] and b"@visit" in data:

	                command_split = re.split("@visit", str(data))
	                if len(command_split) > 1:
	                    player_id = command_split[1].split('(')[0].strip()

	                    print(f"[C][B]Sending vist To {player_id}")
	                    json_result = get_available_room(data.hex()[10:])
	                    parsed_data = json.loads(json_result)
	                    uid = parsed_data["5"]["data"]["1"]["data"]
	                    clients.send(
            self.GenResponsMsg(
                f"{generate_random_color()}جارِ إرسال 1000 زيارة إلى {fix_num(player_id)}...", uid
	                    )
	                )
	                    
	                    message = send_vistttt(player_id)
	                    json_result = get_available_room(data.hex()[10:])
	                    parsed_data = json.loads(json_result)
	                    uid = parsed_data["5"]["data"]["1"]["data"]
	                    
	                    clients.send(self.GenResponsMsg(message, uid))	                           
	                    
	            if "1200" in data.hex()[0:4] and b"@info" in data:
	                try:
	                    print("✅ /info command detected.")  
	                    command_split = re.split("/info", str(data))

	                    if len(command_split) <= 1 or not command_split[1].strip():  # ✅ إذا لم يتم إدخال ID
	                        print("❌ No ID provided, sending error message.")
	                        json_result = get_available_room(data.hex()[10:])
	                        parsed_data = json.loads(json_result)
	                        sender_id = parsed_data["5"]["data"]["1"]["data"]
	                        clients.send(self.GenResponsMsg("[C][B][FF0000] Please enter [00FF00َ]a valid[6E00FFَ] player [FFFF00ِ]ID!", sender_id))
	                        
	                    else:
	                        print("✅ Command has parameters.")  
	                        json_result = get_available_room(data.hex()[10:])
	                        parsed_data = json.loads(json_result)

	                        sender_id = parsed_data["5"]["data"]["1"]["data"]
	                        sender_name = parsed_data['5']['data']['9']['data']['1']['data']
	                        print(f"✅ Sender ID: {sender_id}, Sender Name: {sender_name}")  

	                        # ✅ استخراج UID الصحيح فقط
	                        uids = re.findall(r"\b\d{5,15}\b", command_split[1])  # استخراج أول رقم بين 5 و 15 رقمًا
	                        uid = uids[0] if uids else ""  # ✅ أخذ أول UID فقط

	                        if not uid:
	                            print("❌ No valid UID found, sending error message.")
	                            clients.send(self.GenResponsMsg("[C][B][FF0000] Invalid Player ID!", sender_id))
	                            
	                        else:
	                            print(f"✅ Extracted UID: {uid}")  

	                            try:
	                                info_response = newinfo(uid)
	                                print(f"✅ API Response Received: {info_response}")  
	                            except Exception as e:
	                                print(f"❌ API Error: {e}")
	                                clients.send(self.GenResponsMsg("[C][B] [FF0000] Server Error, Try Again!", sender_id))
	                                
	                            if 'info' not in info_response or info_response['status'] != "ok":
	                                print("❌ Invalid ID or API Error, sending wrong ID message.")
	                                clients.send(self.GenResponsMsg("[C][B] [FF0000] Wrong ID .. Please Check Again", sender_id))
	                                
	                            else:
	                                print("✅ Valid API Response, Extracting Player Info.")  
	                                infoo = info_response['info']
	                                basic_info = infoo['basic_info']
	                                clan_info = infoo.get('clan_info', "false")
	                                clan_admin = infoo.get('clan_admin', {})

	                                if clan_info == "false":
	                                    clan_info_text = "\nPlayer Not In Clan\n"
	                                else:
	                                    clan_info_text = (
	                                        f" Clan Info :\n"
	                                        f"Clan ID : {fix_num(clan_info['clanid'])}\n"
	                                        f"[B][FFA500]• Name: [FFFFFF]{clan_info.get('clanname', 'N/A')}\n"
	                                        f"[B][FFA500]• Members: [FFFFFF]{clan_info.get('livemember', 0)}\n"
	                                        f"[B][FFA500]• Level: [FFFFFF]{clan_info.get('guildlevel', 0)}\n"
	                                       f"[C][B][00FF00]«—————— END Info ——————»\n"
	                                         
	                                        
	                                    )

	                                level = basic_info['level']
	                                likes = basic_info['likes']
	                                name = basic_info['username']
	                                region = basic_info['region']
	                                bio = basic_info.get('bio', "No bio available").replace("|", " ")
	                                br_rank = fix_num(basic_info['brrankscore'])
	                                exp = fix_num(basic_info['Exp'])

	                                print(f"✅ Player Info Extracted: {name}, Level: {level}, Region: {region}")

	                                message_info = (
	                                    f"[C][B][00FF00]«—————— Player Info ——————»\n"
    f"[B][FFA500]• Name: [FFFFFF]{name}\n"
    f"[B][FFA500]• Level: [FFFFFF]{level}\n"
    f"[B][FFA500]• Server: [FFFFFF]{region}\n"
    f"[B][FFA500]• Likes: [FFFFFF]{fix_num(likes)}\n"
    f"[B][FFA500]• Bio: [FFFFFF]{bio}\n"
	                          
	                                 f"{clan_info_text}\n"
	                                    
	                                )

	                                print(f"📤 Sending message to game: {message_info}")  

	                                try:
	                                    clients.send(self.GenResponsMsg(message_info, sender_id))
	                                    print("✅ Message Sent Successfully!")  
	                                except Exception as e:
	                                    print(f"❌ Error sending message: {e}")
	                                    clients.send(self.GenResponsMsg("[C][B] [FF0000] Failed to send message!", sender_id))

	                except Exception as e:
	                    print(f"❌ Unexpected Error: {e}")
	                    clients.send(self.GenResponsMsg("[C][B][FF0000] An unexpected error occurred!", sender_id))
	                                   
	            if "1200" in data.hex()[0:4] and b"@name" in data:
	                try:
	                    print("✅ @info command detected.")  
	                    command_split = re.split("@name", str(data))

	                    if len(command_split) <= 1 or not command_split[1].strip():  # ✅ إذا لم يتم إدخال ID
	                        print("❌ No ID provided, sending error message.")
	                        json_result = get_available_room(data.hex()[10:])
	                        parsed_data = json.loads(json_result)
	                        sender_id = parsed_data["5"]["data"]["1"]["data"]
	                        clients.send(self.GenResponsMsg("[C][B][FF0000] Please enter [00FF00َ]a valid[6E00FFَ] player [FFFF00ِ]ID!", sender_id))
	                        
	                    else:
	                        print("✅ Command has parameters.")  
	                        json_result = get_available_room(data.hex()[10:])
	                        parsed_data = json.loads(json_result)

	                        sender_id = parsed_data["5"]["data"]["1"]["data"]
	                        sender_name = parsed_data['5']['data']['9']['data']['1']['data']
	                        print(f"✅ Sender ID: {sender_id}, Sender Name: {sender_name}")  

	                        # ✅ استخراج UID الصحيح فقط
	                        uids = re.findall(r"\b\d{5,15}\b", command_split[1])  # استخراج أول رقم بين 5 و 15 رقمًا
	                        uid = uids[0] if uids else ""  # ✅ أخذ أول UID فقط

	                        if not uid:
	                            print("❌ No valid UID found, sending error message.")
	                            clients.send(self.GenResponsMsg("[C][B][FF0000] Invalid Player ID!", sender_id))
	                            
	                        else:
	                            print(f"✅ Extracted UID: {uid}")  

	                            try:
	                                info_response = newinfo(uid)
	                                print(f"✅ API Response Received: {info_response}")  
	                            except Exception as e:
	                                print(f"❌ API Error: {e}")
	                                clients.send(self.GenResponsMsg("[C][B] [FF0000] Server Error, Try Again!", sender_id))
	                                
	                            if 'info' not in info_response or info_response['status'] != "ok":
	                                print("❌ Invalid ID or API Error, sending wrong ID message.")
	                                clients.send(self.GenResponsMsg("[C][B] [FF0000] Wrong ID .. Please Check Again", sender_id))
	                                
	                            else:
	                                print("✅ Valid API Response, Extracting Player Info.")  
	                                infoo = info_response['info']
	                                basic_info = infoo['basic_info']
	                                clan_info = infoo.get('clan_info', "false")
	                                clan_admin = infoo.get('clan_admin', {})

	                                if clan_info == "false":
	                                    clan_info_text = "\nPlayer Not In Clan\n"
	                                else:

	                                        f"[B][FFA500]• Name: [FFFFFF]"

	                                         
	                                        


	                                name = basic_info['username']

	                                print(f"✅ Player Info Extracted: {name}")

	                                message_info = (
    f"[B][FFA500]• Name: [FFFFFF]{name}\n"
	                          )

	                                print(f"📤 Sending message to game: {message_info}")  

	                                try:
	                                    clients.send(self.GenResponsMsg(message_info, sender_id))
	                                    print("✅ Message Sent Successfully!")  
	                                except Exception as e:
	                                    print(f"❌ Error sending message: {e}")
	                                    clients.send(self.GenResponsMsg("[C][B] [FF0000] Failed to send message!", sender_id))

	                except Exception as e:
	                    print(f"❌ Unexpected Error: {e}")
	                    clients.send(self.GenResponsMsg("[C][B][FF0000] An unexpected error occurred!", sender_id))	                    
	                    
	            if "1200" in data.hex()[0:4] and b"@bio" in data:
	                try:
	                    print("✅ /info command detected.")  
	                    command_split = re.split("@bio", str(data))

	                    if len(command_split) <= 1 or not command_split[1].strip():  # ✅ إذا لم يتم إدخال ID
	                        print("❌ No ID provided, sending error message.")
	                        json_result = get_available_room(data.hex()[10:])
	                        parsed_data = json.loads(json_result)
	                        sender_id = parsed_data["5"]["data"]["1"]["data"]
	                        clients.send(self.GenResponsMsg("[C][B][FF0000] Please enter a valid player ID!", sender_id))
	                        
	                    else:
	                        print("✅ Command has parameters.")  
	                        json_result = get_available_room(data.hex()[10:])
	                        parsed_data = json.loads(json_result)

	                        sender_id = parsed_data["5"]["data"]["1"]["data"]
	                        sender_name = parsed_data['5']['data']['9']['data']['1']['data']
	                        print(f"✅ Sender ID: {sender_id}, Sender Name: {sender_name}")  

	                        # ✅ استخراج UID الصحيح فقط
	                        uids = re.findall(r"\b\d{5,15}\b", command_split[1])  # استخراج أول رقم بين 5 و 15 رقمًا
	                        uid = uids[0] if uids else ""  # ✅ أخذ أول UID فقط

	                        if not uid:
	                            print("❌ No valid UID found, sending error message.")
	                            clients.send(self.GenResponsMsg("[C][B][FF0000] معرف اللاعب غير صالح!", sender_id))
	                            
	                        else:
	                            print(f"✅ Extracted UID: {uid}")  

	                            try:
	                                info_response = newinfo(uid)
	                                print(f"✅ API Response Received: {info_response}")  
	                            except Exception as e:
	                                print(f"❌ API Error: {e}")
	                                clients.send(self.GenResponsMsg("[C][B] [FF0000] Server Error, Try Again!", sender_id))
	                                
	                            if 'info' not in info_response or info_response['status'] != "ok":
	                                print("❌ Invalid ID or API Error, sending wrong ID message.")
	                                clients.send(self.GenResponsMsg("[C][B] [FF0000] Wrong ID .. Please Check Again", sender_id))
	                                
	                            else:
	                                print("✅ Valid API Response, Extracting Player Info.")  
	                                infoo = info_response['info']
	                                basic_info = infoo['basic_info']
	                                clan_info = infoo.get('clan_info', "false")
	                                clan_admin = infoo.get('clan_admin', {})

	                                if clan_info == "false":
	                                    clan_info_text = "\nPlayer Not In Clan\n"
	                                else:
	                                    clan_info_text = (
	                                        f" Clan Info :\n"
	                                        f"Clan ID : {fix_num(clan_info['clanid'])}\n"
	                                        f"Clan Name : {clan_info['clanname']}\n"
	                                        f"Clan Level: {clan_info['guildlevel']}\n\n"
	                                        "Clan Admin Info : \n"
	                                        f"ID : {fix_num(clan_admin.get('idadmin', 'N/A'))}\n"
	                                        f"Name : {clan_admin.get('adminname', 'N/A')}\n"
	                                        f"Exp : {clan_admin.get('exp', 'N/A')}\n"
	                                        f"Level : {clan_admin.get('level', 'N/A')}\n"
	                                        f"Ranked (Br) Score : {fix_num(clan_admin.get('brpoint', 0))}\n"
	                                    )

	                                level = basic_info['level']
	                                likes = basic_info['likes']
	                                name = basic_info['username']
	                                region = basic_info['region']
	                                bio = basic_info.get('bio', "No bio available").replace("|", " ")
	                                br_rank = fix_num(basic_info['brrankscore'])
	                                exp = fix_num(basic_info['Exp'])

	                                print(f"✅ Player Info Extracted: {name}, Level: {level}, Region: {region}")

	                                message_info = (
	                                    f"{bio}"
	                                )

	                                print(f"📤 Sending message to game: {message_info}")  

	                                try:
	                                    clients.send(self.GenResponsMsg(message_info, sender_id))
	                                    print("✅ Message Sent Successfully!")  
	                                except Exception as e:
	                                    print(f"❌ Error sending message: {e}")
	                                    clients.send(self.GenResponsMsg("[C][B] [FF0000] Failed to send message!", sender_id))

	                except Exception as e:
	                    print(f"❌ Unexpected Error: {e}")
	                    clients.send(self.GenResponsMsg("[C][B][FF0000] An unexpected error occurred!", sender_id))	                    
	                    
	                    
	                    
	            if "1200" in data.hex()[0:4] and b"@like" in data:
	                   
	                    json_result = get_available_room(data.hex()[10:])
	                    parsed_data = json.loads(json_result)
	                    uid = parsed_data["5"]["data"]["1"]["data"]
	                    clients.send(
	                    self.GenResponsMsg(
	                        f"{generate_random_color()}جاري العمل علي الطلب", uid
	                    )
	                )
	                    command_split = re.split("@like", str(data))
	                    player_id = command_split[1].split('(')[0].strip()
	                    print(player_id)
	                    likes_response = send_likes(player_id)
	                    status = likes_response['status']
	                    message = likes_response['message']
	                    print(message)
	                    json_result = get_available_room(data.hex()[10:])
	                    parsed_data = json.loads(json_result)
	                    uid = parsed_data["5"]["data"]["1"]["data"]
	                    clients.send(self.GenResponsMsg(message, uid))
	            	
	            if "1200" in data.hex()[0:4] and b"@check" in data:
	                   try:
	                   	print("Received @check command")
	                   	command_split = re.split("@check", str(data))
	                   	json_result = get_available_room(data.hex()[10:])
	                   	parsed_data = json.loads(json_result)
	                   	uid = parsed_data["5"]["data"]["1"]["data"]
	                   	clients.send(
	                   	self.GenResponsMsg(
                            f"{generate_random_color()}جاري فحص الباند...", uid
                        )
                    )
	                   	if len(command_split) > 1:
	                   	   player_id = command_split[1].split("\\x")[0].strip()
	                   	   player_id = command_split[1].split('(')[0].strip()
	                   	   print(player_id)

	                   	   banned_status = check_banned_status(player_id)
	                   	   print(banned_status)
	                   	   player_id = fix_num(player_id)
	                   	   status = banned_status.get('status', 'Unknown')
	                   	   player_name = banned_status.get('player_name', 'Unknown')

	                   	   response_message = (
                            f"{generate_random_color()}Player Name: {player_name}\n"
                            f"Player ID : {player_id}\n"
                            f"Status: {status}"
                        )
	                   	   print(response_message)
	                   	   clients.send(self.GenResponsMsg(response_message, uid))
	                   except Exception as e:
	                   	print(f"Error in @check command: {e}")
	                   	clients.send(self.GenResponsMsg("[C][B][FF0000]An error occurred, but the bot is still running!", uid))
	            if "1200" in data.hex()[0:4] and b"++WAR" in data:
	                lines = "_"*20
	                
	                json_result = get_available_room(data.hex()[10:])
	                parsed_data = json.loads(json_result)
	                user_name = parsed_data['5']['data']['9']['data']['1']['data']
	                uid = parsed_data["5"]["data"]["1"]["data"]
	                if "***" in str(uid):
	                	uid = rrrrrrrrrrrrrr(uid)
	                time.sleep        
	                clients.send(
	                    self.GenResponsMsg(	
f"""
{generate_random_color()} ⌯ 𝑊𝑒𝑙𝑐𝑜𝑚𝑒 𝑡𝑜 ⌯ صححصححصححصححصحح ρг๏  VIP

{generate_random_color()} ⌯ IПƧƬΛGЯΛM :Insta : ﵥﵥﵥﵥﵥﵥﵥﵥﵥﵥﵥﶹ

━━━━━━━━━━━━━━━
[FFFFF0ِ][bٍ]فتح سكواد 

[FF0000ِ][bٍ]@💪x3

[FF0000ِ][bٍ]@🫠x5

[FF0000ِ][bٍ]@👌x6

[FFFFF0ِ][bٍ]فتح فريق لصديقك  
[FF0000ِ][bٍ]@👌inv id 

[FFFFF0ِ][bٍ]جلب صديقك  
[2E2EF7َ][bٍ]@🫤send id

[FFFFF0ِ][bٍ]سبام طلبات انضمام  
[00FF00ِ][bٍ]+sl id

[FFFFF0ِ][bٍ] سبام طلبات صداقة  
[F07F00ِ][bٍ]@🍆spm id 

[FFFFF0ِ][bٍ] سبام روم  
[2EFEF7َ][bٍ]@🍆r id

[FFFFF0ِ][bٍ]حالة الحساب  
[F07F70ِ][bٍ]@🍆check id

[FFFFF0ِ][bٍ]معرفة منطقة اللعب  
[FFFF00ِ][bٍ]@🍆region id 
━━━━━━━━━━━━━━━

""", uid
	                    )
	                )
	                time.sleep(0.1)
	                clients.send(
		                    self.GenResponsMsg(	
f"""
{generate_random_color()}⇦ حـالـة الـلاعب  :
{generate_random_color()}⇨@🍆s id

{generate_random_color()}⇦ معلومات لاعب:
{generate_random_color()}⇨@🍆info id 

{generate_random_color()}⇦ لاغ بتيمكود  :
{generate_random_color()}⇨+🍆lag timcod

{generate_random_color()}⇦ لاغ+بدأ اجباري:
{generate_random_color()}⇨@🍆za timcod

{generate_random_color()}⇦ دخول البوت الى سكواد:
{generate_random_color()}⇨@🍆yji timcod

{generate_random_color()}⇦ اخراج البوت من اي مجموعة    
{generate_random_color()}⇨@🍆solo

{generate_random_color()}⇦ سبام صولو    
{generate_random_color()}⇨@🍆gt id 

{generate_random_color()}⇦ سبام رساءل:
{generate_random_color()}⇨+🍆ms message 

{generate_random_color()}⇦ جلب بايو لاعب  :
{generate_random_color()}⇨@🍆bio id

{generate_random_color()}⇦ جلب اسم لاعب :
{generate_random_color()}⇨@🍆name id 
""", uid
	                    )
	                )
	                time.sleep(0.2)
	                clients.send(
		                    self.GenResponsMsg(		                       
f"""
{generate_random_color()}━━━━━━━━━━━━━━━
 
[FFFFF0ِ][bٍ]دخول مع بوتات في غيم
[FFFF00ِ][bٍ]@😰bot team cod

[FFFFF0ِ][bٍ]وضع لاعب في حماي
[00FF00ِ][bٍ]@WRG id


[00FF00ِ][bٍ] تابعنا على صفحتنا رئيسي
{generate_random_color()}تيليجرام: @likeaddlike1
{generate_random_color()}إنستجرام:ﵥﵥﵥﵥﵥﵥﵥﵥﵥﵥﵥﶹ

[b][999999]━━━━━━━━━━━━━━━
[C][B] [fa95ff]by > صححصححصححصحح <

""", uid
	                    )
	                )
#########################################                            
def handle_data(self, data, clients):
    if "1200" in data.hex()[0:4] and b"@WRG" in data:
                    
                    lines = "_"*20
                    
                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    user_name = parsed_data['5']['data']['9']['data']['1']['data']
                    uid = parsed_data["5"]["data"]["1"]["data"]
                    if "***" in str(uid):
                        uid = rrrrrrrrrrrrrr(uid)
                    
                    print(f"\nUser With ID : {uid}\nName : {user_name}\nStarted Help\n")
 
                    time.sleep        
                    clients.send(
                        self.GenResponsMsg(
                                f"""[cَ][bَ][F9F460]┄────────╮
[FE0202]تم وضع الاعب في حماية""", uid
                        )
                    )
def handle_data(self, data, clients):
    if "1200" in data.hex()[0:4] and b"+sl" in data:
                try:
                    i = re.split("+sl", str(data))[1]
                    if "***" in i:
                        i = i.replace("***", "106")
                    sid = str(i).split("(\\x")[0].strip()  # المعرف المدخل من المستخدم
                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    uid = parsed_data["5"]["data"]["1"]["data"]  # معرف المرسل

                    # التحقق من أن المعرف صالح (أرقام فقط)
                    if not sid.isdigit():
                        clients.send(
                            self.GenResponsMsg(
                                f"[C][B][FF0000]Error: Please provide a valid numeric ID after /CH\nExample: /sl 12345678", uid
                            )
                        )
                        return

                    tempid = sid  # استخدام المعرف المدخل
                    sent_count = 0  # عداد لتتبع عدد المرات التي تم الإرسال فيها

                    # إرسال رسالة تأكيد قبل اكتمال الإرسال
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B][00ff00]تم وضع الاعب في مقبره بنجاح ✅", uid
                        )
                    )
                       
                    # إرسال طلب الفرقة 5 مرات
                    for _ in range(50):
                        invskwad = self.request_skwad(sid)  # إنشاء حزمة طلب الفرقة
                        socket_client.send(invskwad)  # إرسال الطلب
                        sent_inv = True
                        sent_count += 1
                        logging.info(f"Squad requestsent to ID: {sid}")
                        time.sleep(0.5)  # تأخير 0.5 ثانية بين كل إرسال

                    # إرسال رسالة تأكيد بعد اكتمال الإرسال
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B][00ff00]انتهت وضع الاعب بمقبره بنجاح ✅", uid
                        )
                    )
                except Exception as e:
                    logging.error(f"Error processing +sl {e}")
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B][FF0000]Error: Something went wrong. Please try again.", uid
                        )
                    )
                except Exception as e:
                    logging.error(f"Error processing +sl {e}")
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B][FF0000]Error: Something went wrong. Please try again.", uid
                        )
                    )
                except Exception as e:
                    print(f"An error occurred during +sl spam: {e}")
                    pass                                       
    if "1200" in data.hex()[0:4] and b"+ai" in data:
                try:
                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    uid = parsed_data["5"]["data"]["1"]["data"]                    
                    clients.send(self.GenResponsMsg("يتم تواصل معا سيرفر رجاء الانتظار...", uid))
                    try:
                        raw_message = data.decode('utf-8', errors='ignore').replace('\x00', '')
                        question_part = raw_message.split('+ai')[1]                        
                        unwanted_chars = ["***", "\\x", "\x00"]
                        cleaned_question = question_part
                        for char in unwanted_chars:
                            cleaned_question = cleaned_question.replace(char, "")                          
                        question = cleaned_question.strip()
                        if not question:
                            raise ValueError("No question provided")
                        question = question.replace("***", "106") if "***" in question else question
                        
                        ai_msg = talk_with_ai(question)
                        clients.send(self.GenResponsMsg(ai_msg, uid))
                        
                    except Exception as ai_error:
                        print(f"AI Processing Error: {ai_error}")
                        restart_program()            
                except Exception as e:
                    print(f"AI Command Error: {e}")
                    restart_program()
    if '1200' in data.hex()[0:4] and b'/res' in data:
                if uid:
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B][FF0000]هاد الامر مخصص للادمن ❎ ",
                            uid))                	                                             
    if '1200' in data.hex()[0:4] and b'/ref' in data:
                if uid:
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B][FF0000]تمت اعادة تشغيل لبوت بنجاح ✅ ",
                            uid))
                    restart_program()                                              
                    pass                          
    if '1200' in data.hex()[0:4] and b'+lag' in data:
                try:
                    # تقسيم البيانات القادمة بعد الأمر
                    split_data = re.split(rb'/lag', data)
                    command_parts = split_data[1].split(b'(')[0].decode().strip().split()

                    # التأكد من وجود الكود على الأقل
                    if not command_parts:
                        clients.send(self.GenResponsMsg("[C][B][FF0000]Please provide a code.", uid))
                    return

                    # استخراج الكود وعدد التكرارات
                    room_id = command_parts[0]
                    repeat_count = 1  # القيمة الافتراضية هي مرة واحدة

                    # التحقق مما إذا كان المستخدم قد أدخل عددًا للتكرار
                    if len(command_parts) > 1 and command_parts[1].isdigit():
                        repeat_count = int(command_parts[1])

                    # تطبيق الحد الأقصى للتكرار (3 مرات)
                    if repeat_count > 3:
                        repeat_count = 3
                    
                    # استخراج هوية المرسل لإرسال الرسائل له
                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    uid = parsed_data['5']['data']['1']['data']
                    
                    clients.send(
                        self.GenResponsMsg(f"[C][B][32CD32]Starting spam process. Will repeat {repeat_count} time(s).", uid)
                    )
                    
                    # الحلقة الخارجية الجديدة لتكرار العملية كلها
                    for i in range(repeat_count):
                        # إعلام المستخدم بالدفعة الحالية إذا كان هناك تكرار
                        if repeat_count > 1:
                             clients.send(self.GenResponsMsg(f"[C][B][FFA500]Running batch {i + 1} of {repeat_count}...", uid))

                        # الحلقة الداخلية الأصلية (25 طلبًا)
                        for _ in range(400):
                            # الانضمام إلى الفريق
                            join_teamcode(socket_client, room_id, key, iv)
                            time.sleep(0.00001)
                            
                            # مغادرة الفريق
                            leavee = self.leave_s()
                            socket_client.send(leavee)
                            time.sleep(0.000001)
                        
                        # إضافة تأخير بسيط بين الدفعات إذا كان هناك تكرار
                        if repeat_count > 1 and i < repeat_count - 1:
                            time.sleep(0.1000) # تأخير لمدة ثانية واحدة

                    clients.send(
                        self.GenResponsMsg(f"[C][B][00FF00]All spam batches finished!", uid)
                    )

                except Exception as e:
                    print(f"An error occurred during /code spam: {e}")
                    pass
    if "1200" in data.hex()[0:4] and b"@solo" in data:
                json_result = get_available_room(data.hex()[10:])
                parsed_data = json.loads(json_result)
                uid = parsed_data["5"]["data"]["1"]["data"]

                # إرسال أمر مغادرة الفريق
                leavee = self.leave_s()
                socket_client.send(leavee)

                sleep(1)  # انتظار للتأكد من تنفيذ الخروج

                # تغيير الوضع إلى Solo
                change_to_solo = self.changes(1)
                socket_client.send(change_to_solo)

                

                clients.send(
                    self.GenResponsMsg(
                        f"[C][B][00FF00] تم الخروج من المجموعة.", uid
                    )
                )
    if '1200' in data.hex()[0:4] and b'@za' in data:
                try:
                    # --- 1. استخراج البيانات من الرسالة ---
                    split_data = re.split(rb'@gp', data)
                    command_parts = split_data[1].split(b'(')[0].decode().strip().split()

                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    uid = parsed_data['5']['data']['1']['data']

                    # --- التحقق من وجود كود الفريق ---
                    if not command_parts:
                        clients.send(self.GenResponsMsg("[C][B][FF0000]الرجاء إدخال كود الفريق. مثال:\n/attack [TeamCode]", uid))
                    return

                    team_code = command_parts[0]
                    
                    # --- إعلام المستخدم ببدء الهجوم ---
                    clients.send(
                        self.GenResponsMsg(f"[C][B][FFA500]بدء هجوم مزدوج ومكثف على {team_code}...", uid)
                    )

                    # --- 2. دمج هجوم اللاج والبدء في حلقة واحدة سريعة ---
                    start_packet = self.start_autooo()
                    leave_packet = self.leave_s()

                    # تنفيذ الهجوم المدمج لمدة 45 ثانية
                    attack_start_time = time.time()
                    while time.time() - attack_start_time < 20:
                        # انضمام
                        join_teamcode(socket_client, team_code, key, iv)
                        
                        # إرسال أمر البدء فورًا
                        socket_client.send(start_packet)
                        
                        # إرسال أمر المغادرة فورًا
                        socket_client.send(leave_packet)
                        
                        # انتظار بسيط جدًا لمنع الضغط الزائد على الشبكة
                        time.sleep(0.15)

                    # --- 3. إعلام المستخدم بانتهاء الهجوم ---
                    clients.send(
                        self.GenResponsMsg(f"[C][B][00FF00]اكتمل الهجوم المزدوج على الفريق {team_code}!", uid)
                    )

                except Exception as e:
                    print(f"An error occurred in /attack command: {e}")
                    try:
                        clients.send(self.GenResponsMsg("[C][B][FF0000]حدث خطأ أثناء تنفيذ الهجوم.", uid))
                    except:
                        pass     
                
    if "1200" in data.hex()[0:4] and b"@yji" in data:
                try:
                    # تقسيم البيانات القادمة بعد الأمر
                    split_data = re.split(rb'@yji', data)
                    command_parts = split_data[1].split(b'(')[0].decode().strip().split()

                    # التأكد من وجود التيم كود على الأقل
                    if not command_parts:
                        clients.send(self.GenResponsMsg("[C][B][FF0000]Please provide a team code.", uid))
                    return

                    team_code = command_parts[0]
                    spam_count = 1000  # إرسال أمر البدء 15 مرة بشكل افتراضي
                    team_code = command_parts[0]
                    spam_count = 1000  # إرسال أمر البدء 15 مرة بشكل افتراضي

                    # السماح للمستخدم بتحديد عدد مرات الإرسال
                    if len(command_parts) > 1 and command_parts[1].isdigit():
                        spam_count = int(command_parts[1])
                    
                    # وضع حد أقصى 50 مرة لمنع المشاكل
                    if spam_count > 20:
                        spam_count = 20

                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    uid = parsed_data['5']['data']['1']['data']

                    clients.send(
                        self.GenResponsMsg(f"[C][B][FFA500]جاري تسجيل الدخول", uid)
                    )
                    # 1. الانضمام إلى الفريق باستخدام الكود
                    join_teamcode(socket_client, team_code, key, iv)
                    time.sleep(0)  # انتظار لمدة ثانيتين للتأكد من الانضمام بنجاح

                    clients.send(
                        self.GenResponsMsg(f"[C][B][FF0000]تم تسجيل دخول الى سكواد", uid)
                    )

                    # 2. إرسال أمر بدء اللعبة بشكل متكرر
                    start_packet = self.start_autooo()
                    for _ in range(spam_count):
                        socket_client.send(start_packet)
                        time.sleep(0) # تأخير بسيط بين كل أمر

                    # 3. مغادرة الفريق بعد الانتهاء
                    leave_packet = self.leave_s()
                    socket_client.send(leave_packet)

                    clients.send(
                        self.GenResponsMsg(f"رحب بالبوت", uid)
                    )

                except Exception as e:
                    print(f"An error occurred in /start command: {e}")      
                    
                    
###################################################################################
####################################################################################          
                    pass   
    if "1200" in data.hex()[0:4] and b"@send" in data:
                pass                
                i = re.split("@send", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                json_result = get_available_room(data.hex()[10:])
                parsed_data = json.loads(json_result)
                split_data = re.split(rb'/send', data)
                room_data = split_data[1].split(b'(')[0].decode().strip().split()
                if room_data:
                    print(room_data)
                    iddd = room_data[0]
                    numsc1 = room_data[1] if len(room_data) > 1 else None

                    if numsc1 is None:
                        clients.send(
                            self.GenResponsMsg(
                                f"[C][B] [FF00FF]Please write id and count of the group\n[ffffff]Example : \n/ send 123[c]456[c]78 4\n/ send 123[c]456[c]78 5", uid
                            )
                        )
                    else:
                        numsc = int(numsc1) - 1
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        if int(numsc1) < 3 or int(numsc1) > 6:
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][FF0000] Usage : /send <uid> <Squad Type>\n[ffffff]Example : \n/send 12345678 4\n/ send 12345678 5", uid
                                )
                            )
                        else:
                            packetmaker = self.skwad_maker()
                            socket_client.send(packetmaker)
                            sleep(1)
                            packetfinal = self.changes(int(numsc))
                            socket_client.send(packetfinal)
                            
                            invitess = self.invite_skwad(iddd)
                            socket_client.send(invitess)
                            iddd1 = parsed_data["5"]["data"]["1"]["data"]
                            invitessa = self.invite_skwad(iddd1)
                            socket_client.send(invitessa)
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][00ff00]- AcCept The Invite QuickLy ! ", uid
                                )
                            )
                            leaveee1 = True
                            while leaveee1:
                                if leaveee == True:
                                    print("Leave")
                                    leavee = self.leave_s()
                                    sleep(2.5)
                                    socket_client.send(leavee)   
                                    leaveee = False
                                    leaveee1 = False
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B] [FF00FF]succes !", uid
                                        )
                                    )    
                                if pleaseaccept == True:
                                    print("Leave")
                                    leavee = self.leave_s()
                                    socket_client.send(leavee)   
                                    leaveee1 = False
                                    pleaseaccept = False
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B] [FF00FF]Please accept the invite", uid
                                        )
                                    )   
                else:
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B] [FF00FF]Please write id and count of the group\n[ffffff]Example : \n/ send 123[c]456[c]78 4\n/send 123[c]456[c]78 5", uid
                        )
                    )                    
                    pass                    
    if "1200" in data.hex()[0:4] and b"@inv" in data:
                pass                
                i = re.split("@inv", str(data))[1]
                if "***" in i:
                    i = i.replace("***", "106")
                sid = str(i).split("(\\x")[0]
                json_result = get_available_room(data.hex()[10:])
                parsed_data = json.loads(json_result)
                split_data = re.split(rb'/inv', data)
                room_data = split_data[1].split(b'(')[0].decode().strip().split()
                if room_data:
                    print(room_data)
                    iddd = room_data[0]
                    numsc1 = room_data[1] if len(room_data) > 1 else None

                    if numsc1 is None:
                        clients.send(
                            self.GenResponsMsg(
                                f"[C][B] [FF00FF]Please write id and count of the group\n[ffffff]Example : \n/ inv 123[c]456[c]78 4\n/ inv 123[c]456[c]78 5", uid
                            )
                        )
                    else:
                        numsc = int(numsc1) - 1
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        if int(numsc1) < 3 or int(numsc1) > 6:
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][FF0000] Usage : /inv <uid> <Squad Type>\n[ffffff]Example : \n/inv 12345678 4\n/ inv 12345678 5", uid
                                )
                            )
                        else:
                            packetmaker = self.skwad_maker()
                            socket_client.send(packetmaker)
                            sleep(1)
                            packetfinal = self.changes(int(numsc))
                            socket_client.send(packetfinal)
                            
                            invitess = self.invite_skwad(iddd)
                            socket_client.send(invitess)
                            iddd1 = parsed_data["5"]["data"]["1"]["data"]
                            invitessa = self.invite_skwad(iddd1)
                            socket_client.send(invitessa)
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][00ff00]- تم ارسال للاعب السكواد خمسه ✅ ", uid
                                )
                            )
                            leaveee1 = True
                            while leaveee1:
                                if leaveee == True:
                                    print("Leave")
                                    leavee = self.leave_s()
                                    sleep(2.5)
                                    socket_client.send(leavee)   
                                    leaveee = False
                                    leaveee1 = False
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B] [FF00FF]تم انتهاء العملية بنجاح ✅ !", uid
                                        )
                                    )    
                                if pleaseaccept == True:
                                    print("Leave")
                                    leavee = self.leave_s()
                                    socket_client.send(leavee)   
                                    leaveee1 = False
                                    pleaseaccept = False
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B] [FF00FF]Please accept the invite", uid
                                        )
                                    )   
                else:
                    clients.send(
                        self.GenResponsMsg(
                            f"[C][B] [FF00FF]Please write id and count of the group\n[ffffff]Example : \n/ inv 123[c]456[c]78 4\n/ inv 123[c]456[c]78 5", uid
                        )
                    )      
                    
    if "1200" in data.hex()[0:4] and b"@bot" in data:
                try:
                    split_data = re.split(rb'@bot', data)
                    command_parts = split_data[1].split(b'(')[0].decode().strip().split()

                    if not command_parts:
                        clients.send(self.GenResponsMsg("[C][B][FF0000]ضع التيم كود", uid))
                    return

                    team_code = command_parts[0]
                    spam_count = 20

                    if len(command_parts) > 1 and command_parts[1].isdigit():
                        spam_count = int(command_parts[1])
                    
                    if spam_count > 50:
                        spam_count = 50

                    json_result = get_available_room(data.hex()[10:])
                    parsed_data = json.loads(json_result)
                    uid = parsed_data['5']['data']['1']['data']

                    clients.send(
                        self.GenResponsMsg(f"[C][B][FFA500]يتم البدأ مع بوتات", uid)
                    )

                    join_teamcode(socket_client, team_code, self.key, self.iv)
                    time.sleep(9)

                    clients.send(
                        self.GenResponsMsg(f"[C][B][FF0000]يتم عمل البدأ في وقت {spam_count} times!", uid)
                    )

                    start_packet = self.start_autooo()
                    for _ in range(spam_count):
                        socket_client.send(start_packet)
                        time.sleep(0.1)

                    leave_packet = self.leave_s()
                    socket_client.send(leave_packet)

                    clients.send(
                        self.GenResponsMsg(f"[C][B][00FF00]سيتم البدأ", uid)
                    )

                except Exception as e:
                    print(f"حدث خطأ في امر @bot{e}")                            
##########################################                                                     
    def parse_my_message(self, serialized_data):
        MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
        MajorLogRes.ParseFromString(serialized_data)
        
        timestamp = MajorLogRes.kts
        key = MajorLogRes.ak
        iv = MajorLogRes.aiv
        BASE64_TOKEN = MajorLogRes.token
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp, key, iv, BASE64_TOKEN

    def GET_PAYLOAD_BY_DATA(self,JWT_TOKEN , NEW_ACCESS_TOKEN,date):
        token_payload_base64 = JWT_TOKEN.split('.')[1]
        token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
        decoded_payload = json.loads(decoded_payload)
        NEW_EXTERNAL_ID = decoded_payload['external_id']
        SIGNATURE_MD5 = decoded_payload['signature_md5']
        now = datetime.now()
        now =str(now)[:len(str(now))-7]
        formatted_time = date
        payload = bytes.fromhex("1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131342e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033")
        payload = payload.replace(b"2025-07-30 11:02:51", str(now).encode())
        payload = payload.replace(b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a", NEW_ACCESS_TOKEN.encode("UTF-8"))
        payload = payload.replace(b"996a629dbcdb3964be6b6978f5d814db", NEW_EXTERNAL_ID.encode("UTF-8"))
        payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
        PAYLOAD = payload.hex()
        PAYLOAD = encrypt_api(PAYLOAD)
        PAYLOAD = bytes.fromhex(PAYLOAD)
        whisper_ip, whisper_port, online_ip, online_port = self.GET_LOGIN_DATA(JWT_TOKEN , PAYLOAD)
        return whisper_ip, whisper_port, online_ip, online_port
    
    def dec_to_hex(ask):
        ask_result = hex(ask)
        final_result = str(ask_result)[2:]
        if len(final_result) == 1:
            final_result = "0" + final_result
            return final_result
        else:
            return final_result
    def convert_to_hex(PAYLOAD):
        hex_payload = ''.join([f'{byte:02x}' for byte in PAYLOAD])
        return hex_payload
    def convert_to_bytes(PAYLOAD):
        payload = bytes.fromhex(PAYLOAD)
        return payload
    def GET_LOGIN_DATA(self, JWT_TOKEN, PAYLOAD):
        url = "https://clientbp.common.ggbluefox.com/GetLoginData"
        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JWT_TOKEN}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB50',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.common.ggbluefox.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        
        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.post(url, headers=headers, data=PAYLOAD,verify=False)
                response.raise_for_status()
                x = response.content.hex()
                json_result = get_available_room(x)
                parsed_data = json.loads(json_result)
                print(parsed_data)
                
                whisper_address = parsed_data['32']['data']
                online_address = parsed_data['14']['data']
                online_ip = online_address[:len(online_address) - 6]
                whisper_ip = whisper_address[:len(whisper_address) - 6]
                online_port = int(online_address[len(online_address) - 5:])
                whisper_port = int(whisper_address[len(whisper_address) - 5:])
                return whisper_ip, whisper_port, online_ip, online_port
            
            except requests.RequestException as e:
                print(f"Request failed: {e}. Attempt {attempt + 1} of {max_retries}. Retrying...")
                attempt += 1
                time.sleep(2)

        print("Failed to get login data after multiple attempts.")
        return None, None

    def guest_token(self,uid , password):
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {"Host": "100067.connect.garena.com","User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)","Content-Type": "application/x-www-form-urlencoded","Accept-Encoding": "gzip, deflate, br","Connection": "close",}
        data = {"uid": f"{uid}","password": f"{password}","response_type": "token","client_type": "2","client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3","client_id": "100067",}
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        NEW_ACCESS_TOKEN = data['access_token']
        NEW_OPEN_ID = data['open_id']
        OLD_ACCESS_TOKEN = "ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a"
        OLD_OPEN_ID = "996a629dbcdb3964be6b6978f5d814db"
        time.sleep(0.2)
        data = self.TOKEN_MAKER(OLD_ACCESS_TOKEN , NEW_ACCESS_TOKEN , OLD_OPEN_ID , NEW_OPEN_ID,uid)
        return(data)
        
    def TOKEN_MAKER(self,OLD_ACCESS_TOKEN , NEW_ACCESS_TOKEN , OLD_OPEN_ID , NEW_OPEN_ID,id):
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB50',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.common.ggbluefox.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        data = bytes.fromhex('1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131342e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033')
        data = data.replace(OLD_OPEN_ID.encode(),NEW_OPEN_ID.encode())
        data = data.replace(OLD_ACCESS_TOKEN.encode() , NEW_ACCESS_TOKEN.encode())
        hex = data.hex()
        d = encrypt_api(data.hex())
        Final_Payload = bytes.fromhex(d)
        URL = "https://loginbp.ggblueshark.com/MajorLogin"
 
        RESPONSE = requests.post(URL, headers=headers, data=Final_Payload, verify=False)
        
        combined_timestamp, key, iv, BASE64_TOKEN = self.parse_my_message(RESPONSE.content)
        if RESPONSE.status_code == 200:
            if len(RESPONSE.text) < 10:
                return False
            whisper_ip, whisper_port, online_ip, online_port = self.GET_PAYLOAD_BY_DATA(BASE64_TOKEN, NEW_ACCESS_TOKEN, 1)
            self.key = key
            self.iv = iv
            print(key, iv)
            return(BASE64_TOKEN, key, iv, combined_timestamp, whisper_ip, whisper_port, online_ip, online_port)
        else:
            return False


    def time_to_seconds(hours, minutes, seconds):
        return (hours * 3600) + (minutes * 60) + seconds

    def seconds_to_hex(seconds):
        return format(seconds, '04x')

    def extract_time_from_timestamp(timestamp):
        dt = datetime.fromtimestamp(timestamp)
        h = dt.hour
        m = dt.minute
        s = dt.second
        return h, m, s

    def get_tok(self):
        global g_token
        token, key, iv, Timestamp, whisper_ip, whisper_port, online_ip, online_port = self.guest_token(self.id, self.password)
        g_token = token
        print(whisper_ip, whisper_port)
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            account_id = decoded.get('account_id')
            encoded_acc = hex(account_id)[2:]
            hex_value = dec_to_hex(Timestamp)
            time_hex = hex_value
            BASE64_TOKEN_ = token.encode().hex()
            print(f"Token decoded and processed. Account ID: {account_id}")
        except Exception as e:
            print(f"Error processing token: {e}")
            return

        try:
            head = hex(len(encrypt_packet(BASE64_TOKEN_, key, iv)) // 2)[2:]
            length = len(encoded_acc)
            zeros = '00000000'

            if length == 9:
                zeros = '0000000'
            elif length == 8:
                zeros = '00000000'
            elif length == 10:
                zeros = '000000'
            elif length == 7:
                zeros = '000000000'
            else:
                print('Unexpected length encountered')
            head = f'0115{zeros}{encoded_acc}{time_hex}00000{head}'
            final_token = head + encrypt_packet(BASE64_TOKEN_, key, iv)
            print("Final token constructed successfully.")
        except Exception as e:
            print(f"Error constructing final token: {e}")
        token = final_token
        self.connect(token, 'anything', key, iv, whisper_ip, whisper_port, online_ip, online_port)
        
        return token, key, iv


with open('accs.txt', 'r') as file:
    data = json.load(file)
ids_passwords = list(data.items())

def run_client(id, password):
    print(f"ID: {id}, Password: {password}")
    client = FF_CLIENT(id, password)
    client.start()
    
max_range = 300000
num_clients = len(ids_passwords)
num_threads = 1
start = 0
end = max_range
step = (end - start) // num_threads
threads = []
for i in range(num_threads):
    ids_for_thread = ids_passwords[i % num_clients]
    id, password = ids_for_thread
    thread = threading.Thread(target=run_client, args=(id, password))
    threads.append(thread)
    time.sleep(3)
    thread.start()

for thread in threads:
    thread.join()
    
if __name__ == "__main__":
    try:
        client_thread = FF_CLIENT(id="4140236419", password="408B8A7FCCDA67579C54AF15C165F8DA643EEA131E9F7419A60F3CF816FE1A1A")
        client_thread.start()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        restart_program()
        