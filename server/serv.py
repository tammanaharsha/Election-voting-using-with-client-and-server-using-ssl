import socket
import ssl
import datetime
import os
import sys
import hashlib
from Crypto.Cipher import DES3
import binascii

# set up SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
ff=open('history.txt','w')
ff.close()
# create socket and bind to port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '' 
PORT = int(sys.argv[1])
#s.bind(('', 9995))
s.bind((HOST, PORT))
s.listen(1)

# loop to accept incoming connections
while True:
    # accept connection and wrap in SSL socket
    print('connection....')
    conn, addr = s.accept()
    conn = context.wrap_socket(conn, server_side=True)

    # receive data from client
    while True:
        #print('start')
        data = conn.recv(1024).decode()
        data = data.split(',')
        #print(data)
        # verify user's name and registration number
        keyy=open('symmetrickey','rb')
        key=keyy.read()
        keyy.close()
        name = data[0]
        reg_num = data[1]
        password = data[2]
        hash_object = hashlib.sha256(password.encode())
        hash_value = hash_object.digest()
        iv=b'\xe9#E\x1b\x10\x89^j'
#print(key)
# print(iv)

        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        ciphertext = cipher.encrypt(hash_value)
        passcheck=0
        with open('voterinfo.txt', 'r') as f:
            x=f.readlines()
        #print(x)
        for line in x:
            #print(line)
            info = line.strip().split(' ')
            #print(info)
            if info[0] == name and info[1] == reg_num and info[2] == str(binascii.hexlify(ciphertext)):
    
                # send options to client
                #print(12345)
                #conn.send('1'.encode())
                passcheck=1
                break

        if(passcheck==1):
            #print('yes')
            conn.send('1'.encode())
            break
        else:
            #print('no')
            conn.send('0'.encode())
            continue
        # if(passcheck==1):
        #     break

    #f.close()
            #else:
            # credentials not found, send 0 to client
             #   conn.send('0'.encode())

    # send menu options to client
    # menu_options = "1. Vote\n2. View election result\n3. My vote history\n4. Exit"
    # conn.send(menu_options.encode())

    # receive client's menu choice
    
    
    
    
    while True:
        choice = conn.recv(1024).decode()
        #print('choice:'+choice)
        if choice == '1':
            #print('enter')
            #try:
            history_check=False
            with open('history.txt', 'r') as f:
                # history = f.readlines()
                for line in f:
                    info = line.strip().split(',')
                    #print(info[0])
                    if info[0] == name:
                        #print("in the history check")
                        history_check=True
                        # print('hist case')
                        # conn.send('0'.encode())
                        break
                    # error_msg = "You have already voted."
                    # conn.send(error_msg.encode())
            #         else:
            # # user has not voted yet
            #         print('yessss')
            #         conn.send('1'.encode())
            #         break
                    #candidates = "Candidates: (enter 1 or 2)\n1. Chris\n2. Linda"
                    #conn.send(candidates.encode())
            f.close()
            """except:
                print('excep')
                f1=open('history.txt','w')
                conn.send('1'.encode())
                f1.close()"""
            
            if history_check:
                #print("already voted")
                conn.send('0'.encode())
            else:
                #print("not voted")
                conn.send('1'.encode())
                
            
        
                vote_choice = conn.recv(1024).decode()
                #print('votechoise:'+vote_choice)
                # update election results file
                if os.path.exists('results.txt'):
                    with open('results.txt', 'r+') as f:
                        lines = f.readlines()
                        if vote_choice == '1':
                            lines[0] = f"Chris {int(lines[0].split()[1])+1}\n"
                        elif vote_choice == '2':
                            lines[1] = f"Linda {int(lines[1].split()[1])+1}\n"
                        f.seek(0)
                        f.writelines(lines)
                    f.close()
                    # conn.send('cnfirm1'.encode())
                else:
                    with open('results.txt','w') as fd:
                        fd.write("Chris 0\n")
                        fd.write("Linda 0\n")
                    fd.close()
                    with open('results.txt', 'r+') as f:
                        lines = f.readlines()
                        if vote_choice == '1':
                            lines[0] = f"Chris {int(lines[0].split()[1])+1}\n"
                            # conn.send('1'.encode())
                        if vote_choice == '2':
                            lines[1] = f"Linda {int(lines[1].split()[1])+1}\n"
                            # conn.send('1'.encode())
                        f.seek(0)
                        f.writelines(lines)
                    f.close()
                #continue
                    
                
                fh=open('history.txt','a')
                #print("file append")
                fh.write(f"{name},{datetime.datetime.now()}\n")
                fh.close()

            #conn.send('1'.encode())
            """else:
                fl=open('history.txt','w')
                fl.close()
                conn.send('1'.encode())"""

        # elif choice == '9':
        #     # read election results from file and send to client
        #     with open('results.txt', 'r') as f:
        #         results = f.read()
        #         conn.send(results.encode())

        elif choice == '2':
        # read election results from file
            with open('history.txt', 'r') as f:
                results = f.readlines()
            
            #print(results)

            # calculate total number of votes cast
            total_votes_cast = 0
            for result in results:
                total_votes_cast += 1
            
            #print("votes casted",total_votes_cast)

            # check if total number of votes is equal to the total number of voters
            
            num_voters = 0
            with open('voterinfo.txt', 'r') as f:
                for line in f:
                    num_voters += 1
            #print(f'Total number of voters: {num_voters}')

            if total_votes_cast == num_voters:
                # find the candidate with the most votes
                winner = ''
                max_votes = 0
                with open('results.txt', 'r') as f:
                    results = f.readlines()
                for result in results:
                    candidate, votes = result.split()
                    votes = int(votes)
                    if votes > max_votes:
                        winner = candidate
                        max_votes = votes

                # send the winner and election results to client
                election_results = f"{winner} Win\n"
                for result in results:
                    election_results += result
                conn.send(election_results.encode())
            else:
                # send error message to client
                conn.send("The result is not available".encode())
            

        elif choice == '3':
            #print(5678)
            # read user's vote history from file and send to client
            view_history=False
            with open('history.txt', 'r') as f:
                # user_history = []
                for line in f:
                    fields = line.strip().split(',')
                    if fields[0] == name:
                        view_history=True
                        break
            
            if view_history:
                conn.send(line.encode())
            else:
                conn.send("not voted".encode())
                # print(user_history)
                # #gh="\n".join(user_history)
                # """if user_history:
                #     history_str = "\n".join([f"{uh[1]}: Voted for {uh[2]}" for uh in user_history])
                # else:
                #     history_str = "No vote history found for this user."
                # """
                # conn.send(user_history.encode())

        elif choice == '4':
            # exit program
            break

conn.close()
#fh.close()
s.close()
