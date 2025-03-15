import copy
import hashlib
import random
import string

temp200 = {
    "status": "200",
    "desc": ""
}


def generate_verification_code():
    digits = random.choices(string.digits, k=3)
    letters = random.choices(string.ascii_uppercase, k=3)
    code_list = digits + letters
    random.shuffle(code_list)
    return ''.join(code_list)


def md555(st):
    return hashlib.md5(st.encode()).hexdigest()


def gen200rsp(desc):
    rsp = copy.copy(temp200)
    rsp["desc"] = desc
    return rsp
