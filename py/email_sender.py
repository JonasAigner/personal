# NOTE: your inputs will be stored in yagmail. This script itself stores no data
# For safety: use an email account you don't need

import yagmail
import csv
import sys


print("----- E-mail sender ------")
print("")
print("Type in your G-mail information(username is your yout gmail address without '@gmail.com')")
print("=======================")
username = input("username: ")
password = input("password: ")
print("=======================")

yag = yagmail.SMTP(username, password)

contacts = {}

print("Note: Contact list has to be a csv file. In the first slot are the names and in the second the mail address'")
print("")
contacts_path = input("Contact list path(leave empty to skip):")
if contacts_path == "":
    contacts_path = False

else:
    with open(contacts_path) as c:
        reader = csv.reader(c, delimiter=";")
        print("Your Contacts:\n")
        for zeile in reader:
            name = zeile[0]
            addr = zeile[1]
            print("{} : {}".format(name, addr))
            contacts[name] = addr
        print("--------------------\n\n")
        
def helptext():
	print("----------- help -----------")
	print(" 'send'...................send emails")
	print(" 'help'...................show help")
	print("")
	print("")
	
def send_act():
	use_c = input("Do you want to use your contacts?[y/n]: ")
	if use_c == "y" or use_c == "yes":
		if len(contacts.items()) > 0:
			count = 1
			for c in contacts.items():
				print("{}.  {} : {}".format(count, c[0], c[1]))
				count += 1
			print("")
			contact_list = list(contacts.items())
			num = input("Type contact number: ")
			num = int(num) - 1
			contact = contact_list[num]
			name = contact[0]
			addr = contact[1]
		else:
			print("You have no saved contacts")
			addr = input("Type receiver's mail: ")
			name = False
		
		#mail
		mail_subject = input("Subject: ")
		mail_body = input("\n")
		print("\nSending...")
		yag.send(addr, mail_subject, mail_body)
	
	else:
		addr = input("Type receiver's mail: ")
		mail_subject = input("Subject: ")
		mail_body = input("\n")
		print("\nSending...")
		yag.send(addr, mail_subject, mail_body)
		
        
running = True       
while running:
	action = input(">>>")
	if action == "help" or action == "hilfe" or action == "?":
		helptext()
	elif action == "send":
		send_act()
	elif action == "quit" or action == "exit":
		sys.exit(0)
	
	else:
		print("[ERROR]:invalid input! Type help for inputs")
    

