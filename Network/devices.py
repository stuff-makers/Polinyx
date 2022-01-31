import subprocess
from pygrabber.dshow_graph import FilterGraph


def run(cmd):
    completed = subprocess.run(
        ["powershell", "-Command", cmd], capture_output=True)
    return completed

# def return_device_list():
#     data = run(
#         "Get-PnpDevice -FriendlyName *cam*  -Status OK| select FriendlyName")
#     device_list = data.stdout.decode("utf-8")

#     f = open("assets\\device.txt", "w+", newline="")
#     f.write(device_list)
#     f.seek(0)
#     l = f.readlines()
#     s = list()
#     for i in l:
#         a = i.replace("\r\n", "").strip()
#         if len(a) > 0:
#             s.append(a)
#         else:
#             continue
#     f.close()
#     device_dict = dict(

#     device_dict = dict()
#     id = 0
#     for i in s[2:]:
#         print(device_dict, i)
#         device_dict[i] = id
#         id += 1
#     return s[2:], device_dict


def return_device_list():
    graph = FilterGraph()
    device_list = graph.get_input_devices()
    device_dict = dict()
    id = 0
    for i in device_list:
        device_dict[i] = id
        id += 1

    return device_list, device_dict
