import sys
import shlex
import subprocess
import threading

BYTEORDER = 'big'
players = []
threadLock = threading.Lock()
gameover = False

class judger (threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.subpro = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

    def write(self, msg):
        threadLock.acquire()
        self.subpro.stdin.write(msg)
        self.subpro.stdin.flush()
        threadLock.release()

    def run(self):
        while True:
            if self.subpro.stdout.readable():
                Len = int.from_bytes(sys.stdin.buffer.read(
                    4), byteorder=BYTEORDER, signed=True)
                # print("*******************************************************************\n\n\n\n\n\n")
                Type = int.from_bytes(sys.stdin.buffer.read(
                    4), byteorder=BYTEORDER, signed=True)
                if Type == 0:  # 用户AI发送的包
                    UserCode = int.from_bytes(sys.stdin.buffer.read(
                        4), byteorder=BYTEORDER, signed=True)
                    Len -= 8
                    data = sys.stdin.buffer.read(Len)
                    tosend = Len.to_bytes(4, byteorder=BYTEORDER, signed=True)
                    tosend += data
                    for player in players:
                        player.write(tosend)
                elif Type == 2:
                    Len -= 4
                    data = sys.stdin.buffer.read(Len)
                    tosend = Len.to_bytes(4, byteorder=BYTEORDER, signed=True)
                    tosend += data
                    for player in players:
                        player.write(tosend)
                    gameover = True
                    break

# 在双引号内输入命令
jud = judger("python judger.py --ai-num 5")


class player (threading.Thread):
    def __init__(self, cmd, usercode):
        threading.Thread.__init__(self)
        self.subpro = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.usercode = usercode

    def write(self, msg):
        self.subpro.stdin.write(msg)
        self.subpro.stdin.flush()

    def run(self):
        while True:
            if self.subpro.stdout.readable():
                Len = int.from_bytes(sys.stdin.buffer.read(
                    4), byteorder=BYTEORDER, signed=True)
                # print("*******************************************************************\n\n\n\n\n\n")
                data = sys.stdin.buffer.read(Len)
                Len += 8
                type = 0
                tosend = Len.to_bytes(4, byteorder=BYTEORDER, signed=True)
                tosend += type.to_bytes(4, byteorder=BYTEORDER, signed=True)
                tosend += self.usercode.to_bytes(4, byteorder=BYTEORDER, signed=True)
                tosend += data
                jud.write(tosend)
            if gameover is True:
                break

# 请在双引号内输入命令（ai编号请谨慎设置）
players.append(player("ai1.exe", 0))
players.append(player("ai2.exe", 1))
for pla in players:
    pla.start()
jud.start()

