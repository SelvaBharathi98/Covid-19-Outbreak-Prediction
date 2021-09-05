from django.shortcuts import redirect, render
def home(request):
    import xlrd
    workbook = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\tamilnadu.xls")
    sheet = workbook.sheet_by_index(0)
    col=sheet.cell_value(0, 0)
    rows=sheet.nrows
    #print(sheet.cell_value(22, 6))
    print(rows)
    ts=[]
    for i in range(1,10):
        ts.append(sheet.cell_value(rows-i,6))
    print(ts)
    #print(ts)
    ts=list(map(int,ts))
    ts=ts[-1::-1]
    y=ts
    x=[-4,-3,-2,-1,0,1,2,3,4]
    print(y)

    a=sum(y)/9
    xy=[y[i]*x[i] for i in range(len(y))]
    xs=[x[i]*x[i] for i in range(len(x))]
    b=sum(xy)/sum(xs)
    #print(a,b)

    #day-10
    #for i in range(5,20):
    print("\nTime series")
    v=a+(b*5)
    v=int(v)
    print("todays expected count",v)

    
    cured=sheet.cell_value(rows-1,3)
    death=sheet.cell_value(rows-1,4)
    total_cases=sheet.cell_value(rows-1,5)
    cured=int(cured)
    death=int(death)
    total_cases=int(total_cases)
    print(cured)
    # Extracting number of columns
    print(sheet.ncols)
     #vaccine
    workbook1 = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\vaccine.xls")
    sheet1=workbook1.sheet_by_index(0)
    n=sheet1.nrows
    
    #for india  population
    noofpeopletoachieveheardimmunity=940000000*0.7
    vaccinated=sheet1.cell_value(n-1,19)
    
    totalvaccinated=int(vaccinated)
    vaccinatedpeople=int(totalvaccinated/2)
    noofpeoplevaccinatedinpercent=(vaccinatedpeople*100)/940000000
    nop1 = "{:.2f}".format(noofpeoplevaccinatedinpercent)
    balancepeople=(940000000*0.7)-vaccinatedpeople
    balancepeople=int(balancepeople)
    noofpeoplenotvaccinatedinpercent=(balancepeople*100)/940000000
    nop2 = "{:.2f}".format(noofpeoplenotvaccinatedinpercent) 
    
    #for tamilnadu population
    workbook1 = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\tamilnadu_vaccine.xls")
    sheet1=workbook1.sheet_by_index(0)
    n=sheet1.nrows
    vaccinated=sheet1.cell_value(n-1,1)
    vaccinatedpeople=int( int(vaccinated)/2)
    noofpeoplevaccinatedinpercent=(vaccinatedpeople*100)/53800000
    nop3 = "{:.2f}".format(noofpeoplevaccinatedinpercent)
    balancepeople=(53800000*0.7)-vaccinatedpeople
    balancepeople=int(balancepeople)
    noofpeoplenotvaccinatedinpercent=(balancepeople*100)/53800000
    nop4 = "{:.2f}".format(noofpeoplenotvaccinatedinpercent)
    return render(request,'home.html',{'cured':cured,'death':death,'total_cases':total_cases,'vaccinated':v,'nop1':nop1,'nop2':nop2,'nop3':nop3,'nop4':nop4}) 

def charts(request):
    import xlrd
    workbook = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\tamilnadu.xls")
    workbook1 = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\vaccine.xls")
    sheet = workbook.sheet_by_index(0)
    sheet1=workbook1.sheet_by_index(0)
    val=[]
    months=[]
    m=[]
    j=0
    #vaccine
    n=sheet1.nrows
    vaccinated=sheet1.cell_value(n-1,17)
    for i in range(0,sheet.nrows):
        if j!=0:
            val.append(int(sheet.cell_value(i,6)))
            xl_date=sheet.cell_value(i,0)
            datetime_date = xlrd.xldate_as_datetime(xl_date, 0)
            date_object = datetime_date.date()
            string_date = date_object.isoformat()
            #months.append(string_date[8:])
            m.append(string_date)
        j=j+1  
    #print(months)
    val=list(map(str,val))
    val=' '.join(val)
    months=list(map(str,months))
    months=' '.join(months)
    return render(request,"charts.html",{'x':val,'y':m})


def covidend(request):  
    import xlrd 
    workbook1 = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\vaccine.xls")
    sheet1=workbook1.sheet_by_index(0)
    n=sheet1.nrows
    noofpeopletoachieveheardimmunity=940000000*0.7
    vaccinated=sheet1.cell_value(n-1,19)
    totalvaccinated=int(vaccinated)
    vaccinatedpeople=int(totalvaccinated/2)
    noofpeoplevaccinatedinpercent=(vaccinatedpeople*100)/920000000
    balancepeople=(940000000*0.7)-vaccinatedpeople
    balancepeople=int(balancepeople)
    herdimmuntiyachievedsofar=(noofpeoplevaccinatedinpercent*90)/100 
    print("vaccinatedpeople",vaccinatedpeople)
    print("noofpeoplevaccinatedinpercent",noofpeoplevaccinatedinpercent)
    print("balancepeople",balancepeople) 
    print("herdimmuntiyachievedsofar",herdimmuntiyachievedsofar)  
    return render(request,"covidend.html",{'vaccinatedpeople':vaccinatedpeople,'noofpeoplevaccinatedinpercent':noofpeoplevaccinatedinpercent,'balancepeople':balancepeople,'herdimmuntiyachievedsofar':herdimmuntiyachievedsofar,'herdimmunityneeded':63})

def district_wise(request):
    import requests
    import lxml.html as lh
    import pandas as pd
    url='https://www.tooloogle.com/coronavirus-statistics/india/Tamil%20Nadu'
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements:
        i+=1
        name=t.text_content()
        #print(i,name)
        col.append(name)
    r=[]
    for i in range(len(col)-3):
        s=col[i].split(" ")
        j=0
        while j<len(s):
            if j+2<len(s):
                if s[j]=='' and s[j+2]=='':
                    s.pop(j)
                    s.pop(j)
                    s.pop(j)
            j=j+1           
        j=0
        while j<len(s):
            if s[j]=='':
                s.pop(j)
            j=j+1
        r.append(s)
    r.pop(0)
    print(r)
    return render(request,"district_wise.html",{'col':r})
    

    
def statewise(request):
    import requests
    import lxml.html as lh
    import pandas as pd
    url='https://www.tooloogle.com/tools/coronavirus-statistics-india'
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements:
        i+=1
        name=t.text_content()
        #print(name)
        col.append(name)
    r=[]
    for i in range(len(col)-2):
        s=col[i].split(" ")
        
        c=0
        w=""
        for j in range(1,len(s)):
            if s[j][0].isalpha():
                w=w+s[j]
                c=c+1
            else:
                break
        for j in range(0,c):
            s.pop(1)
        s.insert(1,w)
        j=0
        w1=""
        w2=""
        while j<len(s[1]):
            if s[1][j].isnumeric():
                w2=w2+s[1][j]
            else:
                w1=w1+s[1][j]
            j=j+1
        s.pop(1)
        s.insert(1,w2)
        s.insert(1,w1)
        j=0
        while j<len(s):
            if j+2<len(s):
                if s[j]=='' and s[j+2]=='':
                    s.pop(j)
                    s.pop(j)
                    s.pop(j)
            j=j+1           
        j=0
        while j<len(s):
            if s[j]=='':
                s.pop(j)
            j=j+1
        r.append(s)
    r.pop(0)
    for i in range(len(r)):
        r[i][1]=r[i][1].replace(',','')
        if len(r[i])==5:
            r[i].append("-")
        print(r[i])
    return render(request,"statewise.html",{'col':r})
        
def prediction(request):  
    import xlrd 
    workbook1 = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\vaccine.xls")
    sheet1=workbook1.sheet_by_index(0)
    n=sheet1.nrows
    noofpeopletoachieveheardimmunity=940000000*0.7
    vaccinated=sheet1.cell_value(n-1,19)
    
    totalvaccinated=int(vaccinated)
    vaccinatedpeople=int(totalvaccinated/2)
    noofpeoplevaccinatedinpercent=(vaccinatedpeople*100)/920000000
    nop = "{:.2f}".format(noofpeoplevaccinatedinpercent)
    balancepeople=(940000000*0.7)-vaccinatedpeople
    balancepeople=int(balancepeople)
    herdimmuntiyachievedsofar=(noofpeoplevaccinatedinpercent*90)/100 
    herd = "{:.2f}".format(herdimmuntiyachievedsofar)
    #for difference
    
    diffvaccinated=sheet1.cell_value(n-2,19)
    diffvaccinatedpeople=int(int(diffvaccinated)/2)
    diffnoofpeoplevaccinatedinpercent=(diffvaccinatedpeople*100)/920000000
    diffnop = "{:.2f}".format(diffnoofpeoplevaccinatedinpercent)
    diffbalancepeople=(940000000*0.7)-diffvaccinatedpeople
    diffbalancepeople=int(diffbalancepeople)
    diffherdimmuntiyachievedsofar=(diffnoofpeoplevaccinatedinpercent*90)/100 
    
    d1=vaccinated-diffvaccinated
    d1=int(d1)
    d2=noofpeoplevaccinatedinpercent-diffnoofpeoplevaccinatedinpercent
    d2="{:.2f}".format(d2)
    d3=diffbalancepeople-balancepeople
    d4=herdimmuntiyachievedsofar-diffherdimmuntiyachievedsofar
    d4= "{:.2f}".format(d4)
    
    
    
    print("vaccinatedpeople",vaccinatedpeople)
    print("noofpeoplevaccinatedinpercent",noofpeoplevaccinatedinpercent)
    print("balancepeople",balancepeople) 
    print("herdimmuntiyachievedsofar",herdimmuntiyachievedsofar) 
     
    return render(request,"prediction.html",{'vaccinatedpeople':vaccinatedpeople,'noofpeoplevaccinatedinpercent':nop,'balancepeople':balancepeople,'herdimmuntiyachievedsofar':herd,'herdimmunityneeded':63,'d1':d1,'d2':d2,'d3':d3,'d4':d4})

def tamilnadu_prediction(request):  #
    import xlrd 
    workbook1 = xlrd.open_workbook("C:\\5th_Semester\\Mini Project 2\\covid\\tamilnadu_vaccine.xls")
    sheet1=workbook1.sheet_by_index(0)
    n=sheet1.nrows
    noofpeopletoachieveheardimmunity=53800000*0.7
    vaccinated=sheet1.cell_value(n-1,1)
    noofpeopletoachieveheardimmunity= 21985022
    vaccinatedpeople=int( int(vaccinated)/2)
    noofpeoplevaccinatedinpercent=(vaccinatedpeople*100)/53800000
    nop = "{:.2f}".format(noofpeoplevaccinatedinpercent)
    
    balancepeople=(53800000*0.7)-vaccinatedpeople
    balancepeople=int(balancepeople)
    herdimmuntiyachievedsofar=(noofpeoplevaccinatedinpercent*90)/100
    herd = "{:.2f}".format(herdimmuntiyachievedsofar)
    
    #difference
    diffvaccinated=sheet1.cell_value(n-2,1)
    diffvaccinatedpeople=int(int(diffvaccinated)/2)
    diffnoofpeoplevaccinatedinpercent=(diffvaccinatedpeople*100)/53800000
    diffnop = "{:.2f}".format(diffnoofpeoplevaccinatedinpercent)
    diffbalancepeople=(53800000*0.7)-diffvaccinatedpeople
    diffbalancepeople=int(diffbalancepeople)
    diffherdimmuntiyachievedsofar=(diffnoofpeoplevaccinatedinpercent*90)/100 
    
    d1=vaccinated-diffvaccinated
    d1=int(d1)
    d2=noofpeoplevaccinatedinpercent-diffnoofpeoplevaccinatedinpercent
    d2="{:.2f}".format(d2)
    d3=diffbalancepeople-balancepeople
    d4=herdimmuntiyachievedsofar-diffherdimmuntiyachievedsofar
    d4= "{:.2f}".format(d4)
    print("-------------------------------------")
    print("vaccinatedpeople",vaccinatedpeople)
    print("noofpeoplevaccinatedinpercent",noofpeoplevaccinatedinpercent)
    print("balancepeople",balancepeople) 
    print("herdimmuntiyachievedsofar",herdimmuntiyachievedsofar) 
    print("****************************")
    print("diffvaccinatedpeople",diffvaccinatedpeople)
    print("diffnoofpeoplevaccinatedinpercent",diffnoofpeoplevaccinatedinpercent)
    print("diffbalancepeople",diffbalancepeople) 
    print("diffherdimmuntiyachievedsofar",diffherdimmuntiyachievedsofar) 
    return render(request,"tamilnadu_prediction.html",{'vaccinatedpeople':vaccinatedpeople,'noofpeoplevaccinatedinpercent':nop,'balancepeople':balancepeople,'herdimmuntiyachievedsofar':herd,'herdimmunityneeded':63,'d1':d1,'d2':d2,'d3':d3,'d4':d4})


def covid_news(request):
    return render(request,"covid_news.html")