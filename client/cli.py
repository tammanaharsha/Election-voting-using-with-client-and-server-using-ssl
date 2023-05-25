import socket
import ssl
import sys

# Set up SSL context
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Create TCP socket and wrap with SSL
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname(sys.argv[1]) 
PORT = int(sys.argv[2])
#ssock = context.wrap_socket(client_socket, server_hostname='remote01.cs.binghamton.edu')
ssock = context.wrap_socket(client_socket, server_hostname=HOST)
ssock.connect((HOST, PORT))
#ssock.connect(('remote01.cs.binghamton.edu', 9995))
flag= int(0)

while True:
    if(flag==1):
        break
    # Prompt user for name, registration number, and password
    name = input("Enter your name: ")
    reg_num = input("Enter your voter registration number: ")
    password = input("Enter your password: ")

    # Send user info to server
    ssock.send(f"{name},{reg_num},{password}".encode())

    # Receive response from server
    response = ssock.recv(1024).decode()
    #print('response'+response)
    # If response is 0, user info was incorrect
    if not response == '1':
        print("Invalid name, registration number, or password. Please try again.\n")
        continue

    # Otherwise, user info was correct
    while True:
        # Display main menu options
        print("1. Vote")
        print("2. View election results")
        print("3. My vote history")
        print("4. Exit")

        # Prompt user for selection
        selection = input("Enter your selection (1-4): ")

        # Send selection to server
        try:
            ssock.send(selection.encode())
        except BrokenPipeError:
            print("Socket connection closed prematurely")
            break

        # If user selects "Vote"
        if selection == '1':
            # Receive response from server
            vote_response = ssock.recv(1024).decode()
            #print('345677'+vote_response)
            # If response is 0, user has already voted
            if vote_response == '0':
                print("You have already voted.\n")
                # continue
            else:

            # Otherwise, display candidate options
                print("Candidates:")
                print("1. Chris")
                print("2. Linda")

            # Prompt user for candidate selection
                candidate = input("Enter your candidate selection (1 or 2): ")

            # Send candidate selection to server
                ssock.send(candidate.encode())

            # Receive confirmation message from server
            # confirmation = ssock.recv(1024).decode()
            # print(confirmation)

            # Exit vote loop
            #break

        # If user selects "View election results"
        elif selection == '2':
            # Receive election results from server
            #rr= ssock.recv(1024).decode()
            #rs= ssock.recv(1024).decode()
            results = ssock.recv(1024).decode()
            print(results)

        # If user selects "My vote history"
        elif selection == '3':
            # Receive vote history from server
            vote_history = ssock.recv(1024).decode()
            print(vote_history)

        # If user selects "Exit"
        elif selection == '4':
            # Send exit message to server and exit client loop
            flag=1
            ssock.send("exit".encode())
            ssock.close()
            break

        # If user enters invalid selection
        else:
            print("Invalid selection. Please try again.\n")

# Close the socket
#ssock.close()
