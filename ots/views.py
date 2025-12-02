from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ots.models import *
from django.template import loader
import random
# Create your views here.

def welcome(req):
    template=loader.get_template('welcom.html')
    return HttpResponse(template.render())
    # pass

def candidateRegistrationForm(req):
    res=render(req,'registration_form.html')
    return res

def candidateRegistration(req):
    if req.method=='POST':
        username=req.POST['username']
        #check if the user alredy exist
        if(len(Candidate.objects.filter(username=username))):
            userstatus=1
        else:
            candidate=Candidate()
            candidate.username=username
            candidate.password=req.POST['password']
            candidate.name=req.POST['name']
            candidate.save()
            userstatus=2
    else:
        userstatus=3 # if request is not post
    context={
        'userstatus':userstatus,
    }
    res=render(req,'registration.html',context)
    return res


def loginview(req):
    # pass
    # template=loader.get_template('nig.html')
    # return HttpResponse(template.render())
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        candidate=Candidate.objects.filter(username=username,password=password)
        if(len(candidate)==0):
            loginError='Invalid Username or password'
            res=render(req,'login.html',{'loginError':loginError})
        else:
            #login Succcess
            req.session['username']=candidate[0].username
            req.session['name']=candidate[0].name
            res=HttpResponseRedirect('home')
    else:
        res=render(req,'login.html')
            

    return res

def candidatehome(req):
    # pass
    if ('name' not in req.session.keys()):
        res=HttpResponseRedirect('login')
    else:
        numbers=range(1,11)
        context={'num':numbers}
        res=render(req,'home.html',context)
    return res


def testpaper(req):
    if ('name' not in req.session.keys()):
        res=HttpResponseRedirect('login')
    # fetch quesstions from dbs
    n=int(req.GET['n'])
    question_pool=list(Question.objects.all())
    random.shuffle(question_pool)
    questions_list=question_pool[:n]

    context={'questions':questions_list}
    res=render(req,'test_paper.html',context)
    return res
    

def calculateTestResult(req):
    if ('name' not in req.session.keys()):
        res=HttpResponseRedirect('login')
        return res
    
    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]

    # accessing params

    for k in req.POST:
        if k.startswith('qno'):
            qid_list.append(int(req.POST[k]))
    
    print(qid_list)
        
    for n in qid_list:
        question=Question.objects.get(qid=n)
        print("Correct:", question.ans, "User ans:",req.POST['q'+str(n)] )
        try:
            if question.ans == req.POST['q'+str(n)]:
                total_right+=1
            else:
                # total_wrong+=1
                total_wrong=total_wrong+1
            
            total_attempt+=1
        except:
            pass
    points=(total_right-total_wrong)/len(qid_list)*10
        # store result in Result table
    result=Result()
    result.username=Candidate.objects.get(username=req.session['username'])
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()

    #updating candidate table
    candidate=Candidate.objects.get(username=req.session['username'])
    candidate.test_attempted+=1
    candidate.points=((candidate.test_attempted-1+points)/candidate.test_attempted)
    candidate.save()
    return HttpResponseRedirect('result')

def showTestResult(req):
    if ('name' not in req.session.keys()):
        res=HttpResponseRedirect('login')
        return res
    #fetch latest result from result table
    result=Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username=req.session['username'])
    context={'result':result}
    res=render(req,'show_result.html',context)
    return res

def testResultHistory(req):
    if ('name' not in req.session.keys()):
        res=HttpResponseRedirect('login')
        return res
    
    candidate=Candidate.objects.filter(username=req.session['username'])
    results=Result.objects.filter(username=candidate[0].username)
    context={'candidate':candidate[0],'results':results}
    res=render(req,"candidate_history.html",context)
    return res
    



def logoutView(req):
    if ('name' in req.session.keys()):
        del req.session['username']
        del req.session['name']
        res=HttpResponseRedirect('login')
    return res