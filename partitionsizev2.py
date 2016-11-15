#-*- coding : UTF-8 -*-


import subprocess
import smtplib
from email.mime.text import MIMEText
import time
import math

"""Envoie un message d'alerte si les partititions C et/ou D ont moins de 30% d'espce libre (Warning)
   Critical si moins de 20% d'espace libre
"""

def alarme_mail(niveau, message, monmail):
    """
        fonction envoie un message d'alerte
        Pas d'authentification -> port 25 sur smtp.imm
    """
    date= time.ctime(time.time())
    
    msg = MIMEText(message)  #only ASCII dans message 
    msg['Subject'] = niveau
    msg['From'] = monmail
    msg['To'] = monmail
    msg['Date'] = date
    server_smtp = 'smtp.imm.cnrs.fr:25'
    conn = smtplib.SMTP(server_smtp)
    conn.sendmail(monmail,[monmail],msg.as_string())
    conn.quit()

def freespace_by_part(subprocess_object):
    
    """calcule l'espace libre d'une partition donnée par lettre du lecteur """
    p =subprocess_object
    if p.stderr.readlines():
       msg ='error: '+ p.stderr.readlines()
       alarme_mail('ERROR',msg,monmail)
       exit()
    else:
        diskinfo = [line.split() for line in p.stdout.readlines()]
        free_by_part = dict()
        for i in range(len(diskinfo)):
            #print (str(diskinfo[i][1])[2:4])
            if int(diskinfo[i][2])!=0:
                free_by_part[str(diskinfo[i][1])[2:4]] = math.ceil(100*int(diskinfo[i][0])/int(diskinfo[i][2]))
    return(free_by_part)
    
##MAIN

#Auteur et destinataire des mails    
monmail ="lespinosa@imm.cnrs.fr"
#monmail ="jfguillemot@imm.cnrs.fr"
part_space=dict()

#On filtre sur les partitions C et D
cmd = 'wmic logicaldisk get FreeSpace, Name, Size | findstr /c:"C" /c:"D"'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)   #Le pipe de la commande force shell =True -> securite


part_spce = freespace_by_part(p)

if len(part_spce)==0:
    msg="probleme le dictionnaire des partitions est vide\n"
   # alarme_mail('ERROR2',msg,monmail)
    
for name, val in part_spce.items():
    if val < 20:
        msg="CRITICAL: Il reste {}% d'espace libre sur {}".format(val,name)
        alarme_mail('CRITICAL',msg,monmail)
    elif val < 100:
        msg="WARNING: Il reste {}% d'espace libre sur {}".format(val,name)
        alarme_mail('WARNING',msg,monmail)

    
