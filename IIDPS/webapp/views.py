import mimetypes
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

import matplotlib.pyplot as plt
import numpy as np

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
    if request.method == 'POST':
        uid = request.POST['uid']
        pass_word = request.POST['pwd']

        user_obj = usertab.objects.filter(e_mail=uid, pass_word=pass_word).first()

        if user_obj:
            request.session['e_mail'] = uid
            request.session['n_a_m_e'] = user_obj.n_a_m_e
            request.session['sc_calls'] = ""

            return render(request, 'user_home.html', {'data': user_obj})
        else:
            return render(request, 'user.html', {'msg': "Login Fail"})

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
# def userlogoutdef(request):
#     name= request.session["n_a_m_e"]
#     email= request.session["e_mail"]
#     sc=request.session["sc_calls"]
#     from .DateTime import getdate
#     dt=getdate()
#     print('')
#     sc=sc.strip()
#     c=scpattern.objects.filter(user=email).count()
#     print('.............',c)
#     if c==0:
#         d=scpattern(user=email, sc_calls=sc, freq=1)
#         d.save()
#         del request.session['e_mail']
#         print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> New user')

#         return render(request, 'user.html')
#     else:
#         from .Classificaion import NBClassifier
#         puser=NBClassifier.start([sc])

#         if puser==email:
#             del request.session['e_mail']
#             print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Perfect')
#             return render(request, 'user.html')
#         else:

#             from .GetIP import extract
#             d=extract()

#             from .RandomGen import getnum
#             aid=getnum()

# Prediction  Code <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def userlogoutdef(request):
    name = request.session["n_a_m_e"]
    email = request.session["e_mail"]
    sc = request.session["sc_calls"]

    from .DateTime import getdate
    dt = getdate()

    print('')
    sc = sc.strip()
    c = scpattern.objects.filter(user=email).count()
    print('.............', c)

    if c == 0:
        sc_entry = scpattern(user=email, sc_calls=sc, freq=1)
        sc_entry.save()
        del request.session['e_mail']
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> New user')

        return render(request, 'user.html')

    else:
        from .Classificaion import NBClassifier
        puser = NBClassifier.start([sc])

        if puser == email:
            del request.session['e_mail']
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Perfect')
            return render(request, 'user.html')
        else:
            from .GetIP import extract
            host_ip = extract()   # ✅ now it's clear

            from .RandomGen import getnum
            aid = getnum()

            # Fix: Ensure intruder is always a string
            intruder_value = str(puser) if puser not in [None, ""] else "Unknown"

            from .models import alerts
            alerts.objects.create(
                aid=str(aid),
                user=email,
                sc_calls=sc,
                datetime=dt,
                hostaddr=host_ip[0],   # ✅ hostname
                ipaddr=host_ip[1],     # ✅ IP
                intruder=intruder_value,  # ✅ never null
                stz="waiting"  # 🔄 changed from "active" → "waiting" (based on your email flow)
            )

            del request.session['e_mail']
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Intruder detected')







    # Html & Css Code:

        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import html

        # Escape data for safety in HTML
        name = html.escape(name)
        host_ip = [html.escape(x) for x in host_ip]

        # Email subject
        subject = "Intrusion Alert"

        from django.urls import reverse

        itsme_url = request.build_absolute_uri(reverse('itsme', args=[aid]))
        detection_url = request.build_absolute_uri(reverse('detection', args=[aid]))
        

        body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                @media only screen and (max-width: 600px) {{
                    .container {{
                        padding: 15px !important;
                    }}
                    table {{
                        width: 100% !important;
                        display: block;
                        overflow-x: auto;
                        -webkit-overflow-scrolling: touch;
                    }}
                    th, td {{
                        white-space: nowrap;
                        font-size: 14px !important;
                        text-align: left !important;
                    }}

                    /* #Here you can change the mobile button styles */
                    .button {{
                        display: block !important;
                        width: 70% !important;   /* Change button width here */
                        margin-bottom: 10px !important;
                        text-align: center !important;
                    }}
                    .button a {{
                        display: block !important;
                        width: 70% !important;   /* Change anchor (button) width here */
                        padding: 14px 20px !important;  /* You can change padding here */
                        font-size: 16px !important;     /* Adjust font size here */
                    }}
                }}
            </style>
        </head>
        <body style="margin:0; padding:0; background-color:#f9f9f9;">

            <div class="container" style="background: #f9f9f9;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    max-width: 600px;
                    margin: auto;
                    border-left: 5px solid #e74c3c;
                    font-family: 'Segoe UI', sans-serif;
                    color: #333;
                    line-height: 1.5;
                    font-size: 16px;">

                <h2 style="color: #e74c3c; font-size: 22px; margin-top: 0; margin-bottom: 20px;">
                    Hello {html.escape(name)},
                </h2>

                <p style="margin: 0 0 20px 0;">
                    We noticed a new sign-in to your account and found some suspicious activities.
                </p>

                <table style="width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 25px;
                            font-size: 15px;">
                    <tr>
                        <th style="background-color: #f2f2f2;
                                color: #555;
                                text-align: left;
                                padding: 12px;
                                border: 1px solid #ddd;
                                width: 30%;">Host Name</th>
                        <td style="padding: 12px;
                                border: 1px solid #ddd;">{html.escape(host_ip[0])}</td>
                    </tr>
                    <tr>
                        <th style="background-color: #f2f2f2;
                                color: #555;
                                text-align: left;
                                padding: 12px;
                                border: 1px solid #ddd;">IP Address</th>
                        <td style="padding: 12px;
                                border: 1px solid #ddd;">{html.escape(host_ip[1])}</td>
                    </tr>
                    <tr>
                        <th style="background-color: #f2f2f2;
                                color: #555;
                                text-align: left;
                                padding: 12px;
                                border: 1px solid #ddd;">Date & Time</th>
                        <td style="padding: 12px;
                                border: 1px solid #ddd;">{html.escape(dt)}</td>
                    </tr>
                </table>

                <p style="margin: 0 0 20px 0;">
                    If this was you, please confirm your activity:
                </p>

                

                <div class="button" style="display: inline-block; margin: 0 10px 20px 0;">
                    <a href="{itsme_url}"
                    style="display: inline-block;
                            padding: 12px 20px;
                            background-color: #e74c3c;
                            color: #ffffff;
                            text-decoration: none;
                            border-radius: 4px;
                            font-weight: bold;
                            text-align: center;">
                        Yes, It Was Me
                    </a>
                </div>

                <div class="button" style="display: inline-block;">
                    <a href="{detection_url}"
                    style="display: inline-block;
                            padding: 12px 20px;
                            background-color: #e74c3c;
                            color: #ffffff;
                            text-decoration: none;
                            border-radius: 4px;
                            font-weight: bold;
                            text-align: center;">
                        Report Intrusion
                    </a>
                </div>

                <p style="margin-top: 30px;">
                    Good Day...
                </p>
            </div>

        </body>
        </html>
        """



        # Write HTML to a file if you also want to save it locally
        with open('alert.html', 'w') as f:
            f.write(body)
            

        # Set up email parameters
        sender_email = "iidpsofficial@gmail.com"
        sender_password = "qged bevu ooxw ioby"  # App password
        receiver_email = email

        # Compose the email
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Attach the HTML body
        message.attach(MIMEText(body, "html"))

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Mail sent successfully!")



        from .models import alerts
        alerts.objects.create(
            aid=str(aid),
            user=email,
            sc_calls=sc,
            datetime=dt,
            hostaddr=host_ip[0],   # ✅ hostname from extract()
            ipaddr=host_ip[1],     # ✅ IP from extract()
            intruder=str(puser) if puser else "Unknown",  # ✅ never null
            stz="waiting"
        )




        request.session.pop('e_mail', None)

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
        dataset = [row.split()[1:100] for row in open(os.path.join(settings.BASE_DIR, "MalwareAnalyisis", "malware_analysis_data.csv")).readlines()[1:]]
        l = []

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



        filepath = os.path.join(settings.BASE_DIR, "Data", fname)
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
