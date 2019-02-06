import yagmail
import csv

username = "your username"
password = "your password"

yagmail.register(username, password)
kontakte = {}

# ~ yag = yagmail.SMTP()
# ~ contents = [
    # ~ "This is the body, and here is just text http://somedomain/image.png",
    # ~ "You can find an audio file attached.", 'bild2.webp'
# ~ ]
# ~ #yag.send('jonasaigner10@gmail.com', 'test mit Yagmail', contents)

# ~ # Alternatively, with a simple one-liner:
# ~ yagmail.SMTP('fabianholz2018@gmail.com').send('jonasaigner10@gmail.com', 'test von yag', contents)

with open("email_kontakte.csv") as c:
	reader = csv.reader(c, delimiter=";")
	for zeile in reader:
		for spalte in zeile:
			print(spalte, end="")
		print("")
		text = "Hallo {}, dies ist eine e-mail von meinem python programm(ich bin der jonas)".format(zeile[0])
		yagmail.SMTP("fabianholz2018").send(zeile[1], "Von Jonas", text)

print("Fertig")
		
