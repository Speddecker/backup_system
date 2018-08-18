import hashlib
from os import system
from datetime import date, time, datetime


def getName(path):
	tmp = path.split("/")
	tmp.remove("")
	tmp.remove("")
	return tmp[::-1][0] + ".tar.gz"
	
	
def checkHashsum(file1, file2):
	local_hashsum = hashlib.md5(file1.read()).hexdigest()
	remote_hashsum = hashlib.md5(file2.read()).hexdigest()
	print("Local  backup hashsum: ", local_hashsum)
	print("Remote backup hashsum: ", remote_hashsum)
	
	if(local_hashsum == remote_hashsum):
		print("Данный бэкап уже хранится удалённо!")
	else:
		print("Локальный и удалённый бэкапы не совпадают!\nТребуется отправка %s на сервер!" %archive_name)
	
	
def checkBackup(archive_name):
	f1 = open("local_storage/%s" %archive_name, "rb")
	try:
		f2 = open("remote_storage/%s" %archive_name, "rb")
	except FileNotFoundError:
		#Случай, когда отсутствует бэкап на удалённом сервере (либо ошибка при обработке имени)
		#Заменить следующую команду на реальную отправку на удалённый сервер
		system("cp local_storage/%s remote_storage/%s" %(archive_name.replace(" ", "\ "), archive_name.replace(" ", "\ "))) 
	else:
		checkHashsum(f1, f2)
		f1.close()
		f2.close()
		

def createBackup(file):
	path_list = file.read().split("\n")
	path_list.remove("")
	
	for path in path_list:
		archive_name = getName(path)
		system("cd /home/stanislav/Desktop/Backup\ system/local_storage/; tar -czf %s %s" %(archive_name.replace(" ", "\ "), path.replace(" ", "\ ")))
		checkBackup(archive_name)


#main
PATH_TO_SYSTEM = "/home/stanislav/Desktop/Backup system/"

isDayEnd = datetime.time(datetime.now()) > time(21, 0)
isWeekEnd = datetime.weekday(datetime.now()) == 6
isMonthEnd = datetime.date(datetime.now()).day == 28

#daily backup
if(isDayEnd):
	file = open("daily.txt", "r")
	createBackup(file)
	file.close()
	
	
#weekly backup
if(isWeekEnd and isDayEnd):
	file = open("weekly.txt", "r")
	createBackup(file)
	file.close()
	

#monthly backup
if(isMonthEnd and isWeekEnd and isDayEnd):
	file = open("monthly.txt", "r")
	createBackup(file)
	file.close()
	
