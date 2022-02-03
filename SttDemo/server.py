from stt_server import SttServer

server_obj = SttServer()
server_obj.transcribe_state = True
server_obj.receive_audio()
