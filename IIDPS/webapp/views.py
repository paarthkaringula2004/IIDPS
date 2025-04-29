

import mimetypes
import os

from django.shortcuts import render
from django.http import HttpResponse, request
from .models import *

import matplotlib.pyplot as plt;
import numpy as np
import numpy
from django.shortcuts import render, redirect
from PIL import ImageTk, Image
from PIL import Image

from .DateTime import getdate

def homepage(request):
	return render(request, 'index.html')

def signuppage(request):
	if request.method=='POST':
		e_mail=request.POST['mail']

		d=usertab.objects.filter(e_mail__exact=e_mail).count()
		if d>0:
			return render(request, 'signup.html',{'msg':"e_mail Already Registered"})
		else:
			
			pass_word=request.POST['pass_word']
			phone=request.POST['phone']
			n_a_m_e=request.POST['n_a_m_e']

			d=usertab(n_a_m_e=n_a_m_e,e_mail=e_mail,pass_word=pass_word,phone=phone)
			d.save()

			return render(request, 'signup.html',{'msg':"Register Success, You can Login.."})
	else:
		return render(request, 'signup.html')


	
def userloginaction(request):
	if request.method=='POST':
		uid=request.POST['uid']
		pass_word=request.POST['pwd']
		d=usertab.objects.filter(e_mail__exact=uid).filter(pass_word__exact=pass_word).count()
		
		if d>0:
			d=usertab.objects.filter(e_mail__exact=uid)
			request.session['e_mail']=uid
			request.session['n_a_m_e']=d[0].n_a_m_e
			request.session['sc_calls']=""
			

			return render(request, 'user_home.html',{'data': d[0]})

		else:
			return render(request, 'user.html',{'msg':"Login Fail"})

	else:
		return render(request, 'user.html')

def adminloginaction(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        pwd = request.POST['pwd']

        if uid == 'admin' and pwd == 'admin':
            request.session['adminid'] = 'admin'
            return render(request, 'admin_home.html')

        else:
            return render(request, 'admin.html', {'msg': "Login Fail"})

    else:
        return render(request, 'admin.html')



def adminhomedef(request):
    if "adminid" in request.session:
        uid = request.session["adminid"]
        return render(request, 'admin_home.html')

    else:
        return render(request, 'admin.html')

def adminlogoutdef(request):
    try:
        del request.session['adminid']
    except:
        pass
    return render(request, 'admin.html')


# Prediction  Code <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def userlogoutdef(request):
    name= request.session["n_a_m_e"]
    email= request.session["e_mail"]
    sc=request.session["sc_calls"]
    from .DateTime import getdate
    dt=getdate()
    print('')
    sc=sc.strip()
    c=scpattern.objects.filter(user=email).count()
    print('.............',c)
    if c==0:
        d=scpattern(user=email, sc_calls=sc, freq=1)
        d.save()
        del request.session['e_mail']
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> New user')

        return render(request, 'user.html')
    else:
        from .Classificaion import NBClassifier
        puser=NBClassifier.start([sc])

        if puser==email:
            del request.session['e_mail']
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Perfect')
            return render(request, 'user.html')
        else:

            from .GetIP import extract
            d=extract()

            from .RandomGen import getnum
            aid=getnum()

            sub="<h4>Intrusion Alert<br><br>"
            body="<h5>Hello "+name+"<br><br>"
            body=body+"We noticed a new sign-in to your Account and found few suspicious activities. "
            body=body+"<br><table border cellspacing=10><tr><th>Host Name<td>"+d[0]+"<tr><th>IP Address<td>"+d[1]+" <tr><th>Date & Time <td>"+dt+"</table> <br>"
                
            body=body+"If this was you, <a href=http://localhost:8000/itsme/"+str(aid)+"/ target=_blank>click here. </a> If not, <a href=http://localhost:8000/detection/"+str(aid)+"/ target=_blank>click here. </a>"
            body=body+"<br><br>Good Day.."


            file='alert.html'
            f=open(file, 'w')
            f.write(sub)
            f.write(body)
            f.close()





            d=alerts(aid=aid, user=email, sc_calls=sc, datetime=dt, hostaddr=d[0], ipaddr=d[1], intruder=puser, stz='waiting' )
            d.save()


            del request.session['e_mail']
            return render(request, 'user.html')




def itsme(request,aid):
    d=alerts.objects.filter(aid__exact=aid)
    sc=d[0].sc_calls
    email=d[0].user
    d=scpattern(user=email, sc_calls=sc, freq=1)
    d.save()
    d=alerts.objects.filter(aid__exact=aid).update(stz='Negative')
    return render(request, 'display.html',{'msg': "Thank you for your feedback"})

def detection(request,aid):
    d=alerts.objects.filter(aid__exact=aid).update(stz='Intrusion')
    return render(request, 'display.html',{'msg': "Thank you for your feedback, please change your login credentials.."})

	




def userhomedef(request):
	if "e_mail" in request.session:
		e_mail=request.session["e_mail"]
		d=usertab.objects.filter(e_mail__exact=e_mail)
	
		return render(request, 'user_home.html',{'data': d[0]})

	else:
		return redirect('n_userlogout')

		
def viewprofilepage(request):
	if "e_mail" in request.session:
		uid=request.session["e_mail"]
		d=usertab.objects.filter(e_mail__exact=uid)
		scupdate(request,"ViewProfile")

		return render(request, 'viewpprofile.html',{'data': d[0]})

	else:
		return render(request, 'user.html')


def scupdate(request, call):
	sc=request.session['sc_calls']
	sc=sc+call+" "
	request.session['sc_calls']=sc
	print(sc)
	
		
def viewsc(request):
	if "e_mail" in request.session:
		sc=request.session["sc_calls"]
		sc=sc.strip()
		sc=sc.split(" ")
		
		return render(request, 'viewsc.html',{'data': sc})

	else:
		return render(request, 'user.html')


def fileupload(request):
    if request.method == 'POST':
        file = request.POST['file']
        filen=file
        file2 = 'Data/' + file
        title = request.POST['Title']
        access = request.POST['access']
    
        email = request.session["e_mail"]
        name = request.session["n_a_m_e"]
        f = open(file2, "r")
        dt = f.read()


        #---------------------------------------------
        dataset = [row.split()[1:100] for row in open('D:\\Django\\IIDPS\\MalwareAnalyisis\\malware_analysis_data.csv').readlines()[1:]]
        l=[]
        for l1 in dataset:
	        for l2 in l1:
		        l.append(l2)
        S1=set(l)

        
        filename=file2

        file = open(filename, 'rt')
        text = file.read()
        file.close()
        from nltk.tokenize import word_tokenize
        tokens = word_tokenize(text)

        words = [word for word in tokens if word.isalpha()]
        calls=""
        set3 = S1&set(words) 
        print(set3)

        if len(set3)>0:
            for s in set3:
                calls=calls+s+" "
            calls=calls.strip()
            print(calls)
            from .Detection import Detection
            
            r=Detection.main(calls)
            print(r,'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            return render(request, 'user_home.html', {'msg': 'File has malware activity of '+str(r)+', and upload action has failed ! '})
        else:
            d = files(user=email, username=name, filename=filen, filetitle=title, access=access, filedata=dt, stz='Online')
            d.save()
    
            scupdate(request, "FileUpload")
            return render(request, 'user_home.html', {'msg': 'File Uploaded ! '})
    

        #-------------------------------------------




        
    
    else:
        scupdate(request, "FileSelect")
        return render(request, 'uploadfile.html')
        

def viewfiles(request):
    if "e_mail" in request.session:
        email = request.session["e_mail"]
        d = files.objects.filter(stz='Online')
    
        scupdate(request, "ViewFiles")
    
        return render(request, 'viewfiles.html', {'data': d})
    
    else:
        return render(request, 'user.html')

def viewfile(request, op):
    if "e_mail" in request.session:
        d = files.objects.filter(id=op)

        scupdate(request, "ViewFile")

        return render(request, 'viewfile.html', {'d': d[0]})

    else:
        return render(request, 'user.html')

def filedownload(request):
    if "e_mail" in request.session:
        fid = request.POST['fid']
        fname = request.POST['fname']
        data = request.POST['data']

        print(fname,'<<<<<<<<<<<<<<<<<<<<<<<<<<<')

        scupdate(request, "FileDownload")

        d = files.objects.filter(id=fid)



        filepath = 'D:\\Django\\IIDPS\\Data\\'+fname
        print(filepath)
        path = open(filepath)
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % fname
        return response

        return render(request, 'viewfile.html', {'d': d[0]})

    else:
       return render(request, 'user.html')
	   

def fileupdate(request, op):
    if request.method == 'POST':
        pass

    else:
        scupdate(request, "ViewFile")
        d = files.objects.filter(id=op)
        return render(request, 'fileupdate.html', {'d': d[0]})


def fileupdateaction(request):
    if request.method == 'POST':
        fid = request.POST['fid']
        fname = request.POST['fname']
        data = request.POST['data']

        files.objects.filter(id=fid).update(filedata=data)

        scupdate(request, "UpdateFile")

        return redirect('viewfiles')
    else:
        pass


def chgaccess(request, op):
    if request.method == 'POST':
        pass
    else:
        scupdate(request, "ViewAccess")
        d = files.objects.filter(id=op)
        return render(request, 'fileaccess.html', {'d': d[0]})

def chgaccessaction(request):
    if request.method == 'POST':
        fid = request.POST['fid']
        access = request.POST['access']

        files.objects.filter(id=fid).update(access=access)

        scupdate(request, "ChgAccess")

        return redirect('viewfiles')
    else:
        pass


def delete(request, op):
    if request.method == 'POST':
        pass
    else:
        scupdate(request, "FileDelete")
        d = files.objects.filter(id=op).update(stz="ofline")
        return redirect('viewfiles')

def search(request):
    if request.method == 'POST':
        keys = request.POST['keys']
        print(keys)
       
        d=files.objects.filter(filetitle__icontains=keys)
        scupdate(request, "SeachView")
        return render(request, 'searchresults.html', {'data': d})
        
    else:
        scupdate(request, "Search")
        return render(request, 'search.html')

def newmail(request):
    if request.method == 'POST':
        email = request.session["e_mail"]
        name = request.session["n_a_m_e"] 
        sub = request.POST['sub']
        body = request.POST['body']
        t_o = request.POST['t_o']
        dt=getdate()
        
        d = mails(sender=email, sendername=name, recipient=t_o, title=sub, data=body, datetime=dt)
        d.save()
    
        scupdate(request, "SendMail")
        return render(request, 'user_home.html',{'msg':'Mail Sent !!'} )
        
    else:
        scupdate(request, "MailCompose")

        return render(request, 'compose.html')


def inbox(request):
    if "e_mail" in request.session:
        email = request.session["e_mail"]
        d = mails.objects.filter(recipient=email).order_by("-id")
    
        scupdate(request, "MailList")
    
        return render(request, 'viewmails.html', {'data': d})
    
    else:
        return render(request, 'user.html')


def viewmail(request, op):
    if request.method == 'POST':
        pass

    else:
        scupdate(request, "ViewMail")
        d = mails.objects.filter(id=op)
        return render(request, 'viewmail.html', {'d': d[0]})


def updateprofile(request):
    if request.method == 'POST':
        name = request.POST["name"] 
        phone = request.POST['phone']
        email = request.session["e_mail"]
        usertab.objects.filter(e_mail=email).update(n_a_m_e=name, phone=phone)
        scupdate(request, "ChgProfile")
        return render(request, 'user_home.html',{'msg':'Profile Updated !!'} )
       
    else:
        email = request.session["e_mail"]
        d = usertab.objects.filter(e_mail=email)
   
        scupdate(request, "UpdateProfile")
    
        return render(request, 'updateprofile.html', {'data': d[0]})




def updatepwd(request):
    if request.method == 'POST':
        newpwd = request.POST["newpwd"] 
        old = request.POST['old']
        email = request.session["e_mail"]
        d=usertab.objects.filter(e_mail=email).filter(pass_word=old).count()
        if d>0:
            usertab.objects.filter(e_mail=email).update(pass_word=newpwd)
        scupdate(request, "ChgPassword")
        return render(request, 'user_home.html',{'msg':'Password Updated !!'} )
       
    else:
        scupdate(request, "UpdatePassword")
    
        return render(request, 'updatepwd.html')




def viewint(request):
    if "adminid" in request.session:
        
        d = alerts.objects.filter(stz='Intrusion')
    
        return render(request, 'viewintrusions.html', {'data': d})
    
    else:
        return render(request, 'admin.html')
