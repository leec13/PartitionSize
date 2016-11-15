# -*- coding: UTF-8 -*-


import subprocess
import smtplib
from email.mime.text import MIMEText
import time
import platform
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
        s0 = p.stdout.readlines()
        s1 = [str(i).lstrip("b'") for i in s0]
        s2 = [s.split(" ") for s in s1]
        s3 = [l.pop() for l in s2]
        s3 = ["  ".join(l) for l in s3]
        s4 = "\n".join(s3)
    return(s4)
#        diskinfo = [line.split() for line in p.stdout.readlines()]
#        free_by_part = dict()
#        for i in range(len(diskinfo)):
#            #print (str(diskinfo[i][1])[2:4])
#            if int(diskinfo[i][2])!=0:
#                free_by_part[str(diskinfo[i][1])[2:4]] = math.ceil(100*int(diskinfo[i][0])/int(diskinfo[i][2]))
#    return(free_by_part)
    
def freespace_by_part_Darwin(subprocess_object):
    
    """calcule l'espace libre d'une partition donnée par lettre du lecteur """
    p =subprocess_object
    if p.stderr.readlines():
       msg ='error: '+ p.stderr.readlines()
       alarme_mail('ERROR',msg,monmail)
       exit()
    else:
        return("".join(p.stdout.readlines()))
    
#    else:
#        diskinfo = [line.split() for line in p.stdout.readlines()]
#        print(diskinfo)
#        free_by_part = dict()
#        for i in range(1,len(diskinfo),1):
#            free_by_part[str(diskinfo[i][5])] = int(diskinfo[i][4].split("%")[0])
#    return(free_by_part)
       
       
       
       
##MAIN

#Auteur et destinataire des mails    
monmail ="lespinosa@imm.cnrs.fr"
#monmail ="jfguillemot@imm.cnrs.fr"
#part_space=dict()

#On filtre sur les partitions C et D
#if(platform.system()=="Windows"): cmd = 'wmic logicaldisk get FreeSpace, Name, Size | findstr /c:"C" /c:"D"'
if(platform.system()=="Windows"): cmd = 'wmic logicaldisk Where DriveType="3" get FreeSpace, Name, Size, Volumename
else : cmd = 'df -g -l'
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)   #Le pipe de la commande force shell =True -> securite

if(platform.system()=="Windows"): part_spce = freespace_by_part(p)
else : part_spce = freespace_by_part_Darwin(p)

msg = part_spce
alarme_mail('DiskInfos',msg,monmail)
print("end")