import random
import socket
from UserData.ServerConnection import cursor, db


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def associate_id(id):
    ip = local_ip()
    cursor.execute(f"delete from meeting_id where ip=\"{ip}\"")
    cursor.execute(f"insert into meeting_id values(\"{str(id)}\",\"{ip}\")")
    db.commit()


def set_new_meeting_id(label, frame):
    cursor.execute("select id from meeting_id")
    id_tup_list = cursor.fetchall()
    id_list = list()
    for i in id_tup_list:
        for j in i:
            id_list.append(j)
    while True:
        elements = "abcdefghijklmnopqrstuvwxyz"
        id = random.choices(elements, k=6)
        str_id = ''.join([str(elem) for elem in id])
        if str_id not in id_list:
            associate_id(str_id)
            break
        else:
            continue
    label['text'] = str_id
    frame.update()


def create_new_meeting_id():
    cursor.execute("select id from meeting_id")
    id_tup_list = cursor.fetchall()
    id_list = list()
    for i in id_tup_list:
        for j in i:
            id_list.append(j)
    while True:
        elements = "abcdefghijklmnopqrstuvwxyz"
        id = random.choices(elements, k=6)
        str_id = ''.join([str(elem) for elem in id])
        if str_id not in id_list:
            associate_id(str_id)
            break
        else:
            continue


def fetch_ip(id):
    try:
        cursor.execute(f"select ip from meeting_id where id =\"{id}\"")
        ip = cursor.fetchone()
        db.commit()
        return ip[0]
    except:
        return False


def fetch_user_meeting_id():
    ip = local_ip()
    cursor.execute(f"select id from meeting_id where ip=\"{ip}\"")
    id = cursor.fetchone()
    db.commit()
    return str(id[0])


fetch_user_meeting_id()
