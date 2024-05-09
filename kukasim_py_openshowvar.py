
'''
A Python port of KUKA VarProxy client (OpenShowVar).
'''

from __future__ import print_function
import sys
import struct
import random
import socket
import time

from vcScript import *
from vcHelpers.Robot2 import *



__version__ = '1.1.7'
ENCODING = 'UTF-8'

PY2 = sys.version_info[0] == 2
if PY2: input = raw_input

a1 = 0
a2 = -90
a3 = 90



def OnRun():
    robot = getRobot()
    robot.driveJoints(a1,a2,a3,0,0,0)
    robot.Controller.moveJoint(0,a1)

    comp = getComponent()

    #get property to set its value
    point = comp.getProperty("P1")

    #I taught robot a position, and now using that position
    #another option is to use the readIn() method in vcMotionStatement
    rx = comp.getBehaviour("Executor")
    statement = rx.Program.MainRoutine.Statements[0]
    print('statement is',statement)
    #s_point = statement.JointValues

    #value is now stored in property
    #point.Value = s_point
    #print('touch point axis are',point.value)
    #ip = input('IP Address: ')
    ip = '192.168.41.64'
    #port = input('Port: ')
    port = '7000'
    print('I am starting this')
    run_shell(ip, int(port),robot,comp)
    

class openshowvar(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.a1 = 0.0
        self.robot = None
        self.port = port
        self.incr_deg = 0
        self.msg_id = random.randint(1, 100)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.ip, self.port))
        except socket.error:
            pass

    def test_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ret = sock.connect_ex((self.ip, self.port))
            return ret == 0
        except socket.error:
            print('socket error')
            return False

    can_connect = property(test_connection)

    def read(self, var, debug=True):
        if not isinstance(var, str):
            raise Exception('Var name is a string')
        else:
            self.varname = var if PY2 else var.encode(ENCODING)
        return self._read_var(debug)

    def write(self, var, value, debug=True):
        if not (isinstance(var, str) and isinstance(value, str)):
            raise Exception('Var name and its value should be string')
        self.varname = var if PY2 else var.encode(ENCODING)
        self.value = value if PY2 else value.encode(ENCODING)
        return self._write_var(debug)

    def _read_var(self, debug):
        req = self._pack_read_req()
        self._send_req(req)
        _value = self._read_rsp(debug)
        if debug:
            #print(_value)
            print('_value')
        return _value

    def _write_var(self, debug):
        req = self._pack_write_req()
        self._send_req(req)
        _value = self._read_rsp(debug)
        if debug:
            # print(_value)
            print('_value')
        return _value

    def _send_req(self, req):
        self.rsp = None
        self.sock.sendall(req)
        self.rsp = self.sock.recv(256)

    def _pack_read_req(self):
        var_name_len = len(self.varname)
        flag = 0
        req_len = var_name_len + 3

        return struct.pack(
            '!HHBH'+str(var_name_len)+'s',
            self.msg_id,
            req_len,
            flag,
            var_name_len,
            self.varname
            )

    def _pack_write_req(self):
        var_name_len = len(self.varname)
        flag = 1
        value_len = len(self.value)
        req_len = var_name_len + 3 + 2 + value_len

        return struct.pack(
            '!HHBH'+str(var_name_len)+'s'+'H'+str(value_len)+'s',
            self.msg_id,
            req_len,
            flag,
            var_name_len,
            self.varname,
            value_len,
            self.value
            )

    def _read_rsp(self, debug=False):
        if self.rsp is None: return None
        var_value_len = len(self.rsp) - struct.calcsize('!HHBH') - 3
        result = struct.unpack('!HHBH'+str(var_value_len)+'s'+'3s', self.rsp)
        _msg_id, body_len, flag, var_value_len, var_value, isok = result
        if debug:
            #print('[DEBUG]', result)
            print('do nithin')
        if result[-1].endswith(b'\x01') and _msg_id == self.msg_id:
            self.msg_id = (self.msg_id + 1) % 65536  # format char 'H' is 2 bytes long
            return var_value

    def close(self):
        self.sock.close()


############### test ###############


def run_shell(ip, port,robot,comp):
    client = openshowvar(ip, port)
    if not client.can_connect:
        print('Connection error')
        import sys
        sys.exit(-1)
    print('\nConnected KRC Name: ', end=' ')
    client.read('$ROBNAME[]', False)
    loop_list = ['0','1','2','3','4','5','6','7','8','9','8','7','6','5','4','3','2','1','0']
    loop_all = loop_list + loop_list + loop_list
    loop_arr = 0
    incr_deg = 0
    while True:
        #data = input('\nInput var_name [, var_value]\n(`q` for quit): ')
        data = '$AXIS_ACT'
        write_data = 'myaxis'

        #get property to set its value
        # point = comp.getProperty("P1")

        # #I taught robot a position, and now using that position
        # #another option is to use the readIn() method in vcMotionStatement
        # rx = comp.getBehaviour("Executor")
        # statement = rx.Program.MainRoutine.Statements[1]
        # s_point = statement.Positions[0].JointValues

        # #value is now stored in property
        # point.Value = s_point
        # print('touch point axis are',point.value)
        for i in range(0,100):
          #print('data is',data[0])
          #robot.Controller.moveJoint(0,i*0.2)

          if data.lower() == 'q':
              print('Bye')
              client.close()
              break
          else:
              #print(' I am printing',i)
              parts = data.split(',')
              if len(parts) == 1:
                  get_answer =client.read(data.strip(), False)
                  #write_answer = client.read(write_data.strip(), False)
                  write_answer = get_answer
                  #print('get_answer',write_answer)
                  #print('find_index',write_answer.find('A1'))
                  a1_idx = get_answer.find('A1')
                  a1 = get_answer[a1_idx+2:a1_idx+9]

                  a2_idx = get_answer.find('A2')
                  a2 = get_answer[a2_idx+2:a2_idx+9]

                  a3_idx = get_answer.find('A3')
                  a3 = get_answer[a3_idx+2:a3_idx+9]

                  a4_idx = get_answer.find('A4')
                  a4 = get_answer[a4_idx+2:a4_idx+9]

                  a5_idx = get_answer.find('A5')
                  a5 = get_answer[a5_idx+2:a5_idx+9]

                  a6_idx = get_answer.find('A6')
                  a6 = get_answer[a6_idx+2:a6_idx+9]
                  #a2 = 
              else:
                  get_answer = client.write(parts[0], parts[1].lstrip(), False)
                  #get_answer = client._value
                  #print('get_answer',get_answer)

                  a1_idx = get_answer.find('A1')
                  a1 = get_answer[a1_idx+2:a1_idx+9]
                  a2_idx = get_answer.find('A2')
                  a2 = get_answer[a2_idx+2:a2_idx+9]
                  a3_idx = get_answer.find('A3')
                  a3 = get_answer[a3_idx+2:a3_idx+9]
                  a4_idx = get_answer.find('A4')
                  a4 = get_answer[a4_idx+2:a4_idx+9]
                  a5_idx = get_answer.find('A5')
                  a5 = get_answer[a5_idx+2:a5_idx+9]
                  a6_idx = get_answer.find('A6')
                  a6 = get_answer[a6_idx+2:a6_idx+9]
                  
              #robot.Controller.moveJoint(0,float(a1))
              #robot.Controller.moveJoint(1,float(a2))
              #robot.Controller.moveJoint(2,float(a3))
              #robot.Controller.moveJoint(3,float(a4))
              #robot.Controller.moveJoint(4,float(a5))
              #robot.Controller.moveJoint(5,float(a6))
              robot.driveJoints(float(a1),float(a2),float(a3),float(a4),float(a5),float(a6))   
              #incr_deg += 1
              #write_answer_list = list(write_answer)
              #write_answer_list[13] = str(incr_deg)
              #write_answer = str(write_answer_list)

              #write_answer_list = list(write_an)

              
              

              #write_answer.replace("A1 0.0","A1 1.0")
              
              time.sleep(0.02)
              #time.sleep(2)

              

if __name__ == '__main__':
    #ip = input('IP Address: ')
    #port = input('Port: ')
    #run_shell(ip, int(port))

    #ip = input('IP Address: ')
    ip = '192.168.41.64'
    
    #port = input('Port: ')
    port = '7000'
    print('I am starting this')
    #run_shell(ip, int(port))




