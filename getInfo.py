import imaplib
import re
import requests
import json
from email.parser import Parser



def getEmail(ind):															#returns the (ind)th email in inbox
	url = "outlook.office365.com"
	conn = imaplib.IMAP4_SSL(url,993)
	user,password = ("c22grady.phillips@edu.usafa.edu","hackcuP$ss12")
	conn.login(user,password)
	conn.select('INBOX')
	results,data = conn.search(None,'ALL')
	msg_ids = data[0]
	msg_id_list = msg_ids.split()
	#print(msg_id_list)

	latest_email_id = msg_id_list[-ind]
	result,data = conn.fetch(latest_email_id,"(RFC822)")
	raw_email = data[0][1]
	return raw_email



def getSub(email):															#returns the subject of the passed email
	p = Parser()
	msg = p.parsestr(email)

	subject = msg.get('Subject')

	return subject



def compareSubs(cSub,tSub):													#boolean: is this the email?
	if tSub.find(cSub) != -1:												#    compares two subjects to determine if the subject of the 
		return True															#    email (tSub) contains the searched string (cSub)
	else:
		return False



def getRO():
	correct_sub = "Wing Operations Routine Order"

	is_RO = False
	i = 0
	while is_RO == False:
		i += 1
		temp_sub = getSub(getEmail(i))
		is_RO = compareSubs(correct_sub,temp_sub)
	return getEmail(i)



def getUOD(email):
	if email.find("ABUs") != -1: return "ABUs"
	elif email.find("Blues") != -1: return "Blues"
	elif email.find("Flight Suits") != -1: return "Flight Suits"



def getDays(email):
	days = []
	nstr = email[8000:-1]
	lines = nstr.split('\n')
	for line in lines:
		if ("2019" in line or "Ring Dance" in line or "Commitment" in line or "Recognition" in line) and "<" not in line and ":" not in line:
			num = lines.index(line) + 2
			days.append(lines[num].replace("( ",'').replace(" )",'').replace('\r',''))
	return days



def getMeals(email):
	meals = []
	lines = email.split('\n')
	for line in lines:
		if ("Breakfast" in line or "Lunch" in line or "Dinner" in line) and "<" not in line:
			num = lines.index(line) + 4
			meals.append(lines[num].replace('\r',''))
	return meals



roemail = getRO()
'''
#print(roemail)
print(getUOD(roemail))
print(getDays(roemail))
print(getMeals(roemail))
'''

uod = getUOD(roemail)
days = getDays(roemail)
meals = getMeals(roemail)

ROData = {
	"UOD": uod, 
	"Breakfast": meals[0],
	"Lunch": meals[1],
	"Dinner": meals[2],
	"Commissioning": days[0],
	"Ring Dance": days[1],
	"Commitment": days[2],
	"Recognition": days[3]
}



# convert into JSON:
y = json.dumps(ROData)

# the result is a JSON string:
print(y)


res = requests.post('http://10.203.154.170:5000/update', json=ROData)
if res.ok:
    print res.text