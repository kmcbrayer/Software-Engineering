from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from mobileesp.mobile import MobileDetectionMiddleware

from bandsteps_app.models import *
from bandsteps_app.forms import UserProfileForm, UploadFileForm
from urls_settings import settings

import re, StringIO, math

from pyPdf import PdfFileReader


#angular view
def angular(request):
    return render_to_response('angular.html',{})

def ember(request):
    return render_to_response('ember.html',{'drills':Drill.objects.all()})


#end angular view
def home(request):
      
    if request.user.is_authenticated():
        return redirect("/landing/")  
    else:
        return render_to_response('index.html', {}, context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return redirect('/')

def login_page(request):   
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/landing/')
        else:
            return render_to_response('index.html', {'errors': 'Please enter a valid username and password.'})
    else:
        return render_to_response('index.html', {'errors': 'Error logging in. Please try again later.'}, context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST':
        uform = UserCreationForm(request.POST)
        if uform.is_valid():   
            uform.save()
            user = authenticate(username=uform.cleaned_data['username'], password=uform.cleaned_data['password1'])
            user.is_active=True
            login(request, user)
            
            return redirect("/landing/")
        else:
            return render_to_response('register.html', {'errors':'Please correct your mistakes below.', 'uform':uform}, RequestContext(request))
    else:
        return render_to_response('register.html', {'uform':UserCreationForm()}, context_instance=RequestContext(request))

@csrf_exempt
def dispatch(request):
    #so the url==/api/?lat=xx.xxxx&long=xx.xxx&user=id&drill=drill_id#
    drill=Drill.objects.get(id=request.GET.get('drill',None))
    lat=float(request.GET.get('lat', None))
    long=float(request.GET.get('long', None))
    s_id=str(request.GET.get('user', 0))
    # the locations for the drill are stored as comma seperated values this extracts them 
    location_1 = drill.location_1.split(",")
    x_1 = float(location_1[0])
    y_1 = float(location_1[1])
    location_2 = drill.location_2.split(",")
    x_2 = float(location_2[0])
    y_2 = float(location_2[1])
    #find the angle of the field relative to true north (is negative because the resulting angle will be used in reverse)
    field_angle = -math.atan((y_2-y_1)/(x_2-x_1)) #leave in radians
    loc = StudentLoc.objects.filter(set=Set.objects.get(drill=drill,current=True),s_id=s_id)[0]
    #need these checks for division later
    if loc.rel_x==0:
        loc.rel_x=0.00001
    if loc.rel_y==0:
        loc.rel_y=0.00001

    # 0.00000823786268323 = (1/1093.61)/(10000/90) which converts from yards to km to decimal degrees
    point_x = adjust_point_x(loc.rel_x,loc.rel_y,field_angle)*0.00000823786268323
    point_y = adjust_point_y(loc.rel_x,loc.rel_y,field_angle)*0.00000823786268323

    distance = haversine(long,lat,y_1+point_y,x_1+point_x)*1093.61 #haversine returns km this converts to yards
    direction = math.atan((long-point_y)/(lat-point_x))*57.2957 # convert to degrees
    distance = "%.4f" % distance
    direction = "%.2f" % direction
    return HttpResponse(simplejson.dumps({"status":"OK", "user":[{"s_id":s_id,"distance":distance,"direction":direction,"lat":str(x_1+point_x),"long":str(y_1+point_y)}]}), content_type='application/json')

def adjust_point_x(x,y,angle):
    return x * math.cos(angle) - y * math.sin(angle)

def adjust_point_y(x,y,angle):
    return x * math.sin(angle) + y * math.cos(angle)

def distance(lon1,lat1,lon2,lat2):
    print math.sqrt(math.pow(lon2-lon1,2)+(lat2-lat1,2))
    return math.sqrt(math.pow(lon2-lon1,2)+(lat2-lat1,2))

def haversine(lon1, lat1, lon2, lat2):
    #haversine formula from http://www.movable-type.co.uk/scripts/latlong.html converted to python
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    km = 6367 * c
    return km

@csrf_exempt
def lists(request):
    json_list = []
    if request.GET.get('instructor'):
        data_list = Drill.objects.filter(instructor=request.GET.get('instructor'))
        for i in data_list.iterator():
            json_list.append({"drill_id":str(i.id),"drill_name":str(i.name)})
    elif request.GET.get('drill'):
        drill = Drill.objects.get(instructor=request.GET.get('ins'),id=request.GET.get('drill'))
        sets = Set.objects.get(drill=drill,number=1)
        data_list = StudentLoc.objects.filter(set=sets)
        for i in data_list.iterator():
            json_list.append({"student_id":str(i.id),"student_num":str(i.s_id)})
    else:
        data_list = User.objects.all()
        for i in data_list.iterator():
            json_list.append({"instructor_name":i.username,"instructor_id":str(i.id)})

    return HttpResponse(simplejson.dumps({"status":"OK","list":json_list}), content_type='application/json')

def new_drill(request):
    if not request.user.is_authenticated():
        return redirect('/')
    error = None

    if request.method=='POST':
        form = UploadFileForm(request.POST,request.FILES)
        try:
            file = request.FILES['file']
        except:
            error = 'Please select a Pyware pdf to upload'
            return render_to_response('new_drill.html', {'form':form,'errors':error},context_instance=RequestContext(request))
        if not file.content_type == "application/pdf":
            return render_to_response('new_drill.html', {'form':form,'errors':"File is not a pdf"},context_instance=RequestContext(request))
        if form.is_valid():
            #create drill
            drill = Drill(name=form.cleaned_data['name'],location_1=None,location_2=None,instructor=request.user)
            drill.save()
            #initialize the first set 
            s = Set(current=True, drill=drill,number=1)
            s.save()
            #PdfFileReader extracts data from the file as a large string 
            p = PdfFileReader(file)
            content =''
            #read line by line per page
            for i in range(0, p.getNumPages()):
                content += p.getPage(i).extractText()
            #splits the large string "content" on keywords to be used as pseudo data sets
            line = re.split(r'\)|line|Page', content)
            for ln in line:
                #if the word "Set" is in the line create a new set in the database
                if re.search(r'Set', ln):
                    se = re.findall('(?<=Set )\w+', ln)
                    if not se == None:
                        set_num = se[0]
                    if not Set.objects.filter(drill=drill,number=set_num):
                        s = Set(current=False, drill=drill,number=set_num)
                        s.save()
                    continue
                # find the first numbers(up to 3) before a capital letter
                s_id = re.findall(r'[0-9]{1,3}(?=[A-Z])', ln)
                if s_id == []:
                    continue
                student_id = int(s_id[0])

                # find the yard line from the data set
                rel_x = re.findall(r"\d+(?= yd)", ln)
                if not rel_x == []:
                    rel_x = 50-int(rel_x[0])
                # if left or right the yard line is positive or negative
                if re.search(r"Left",ln):
                    rel_x = -rel_x
                rel_y = 0
                # we know how far the hashes are from the sideline so we can save them as relative y coordinates
                if re.search(r'Visitor hash', ln):
                    rel_y = int((160-53.3)/3)
                elif re.search(r'Visitor side', ln):
                    rel_y = 160/3
                elif re.search(r'Home hash', ln):
                    rel_y = 53.4/3
                #create the student location in the data base
                location = StudentLoc(set=s,s_id=student_id,rel_x=rel_x,rel_y=rel_y)
                location.save()

        return redirect('/')

    else:
        form = UploadFileForm()
    return render_to_response('new_drill.html', {'form':form,'errors':error},context_instance=RequestContext(request))

def landing(request):
    if not request.user.is_authenticated():
        return redirect('/')

    drills = Drill.objects.filter(instructor=request.user)
    
    # need to pass user into here 
    return render_to_response('landing.html', { 'user':request.user, 'is_tablet': request.is_tablet, 'drills':drills})

def review(request):
    return render_to_response('review.html', {})

def drill(request,drill_id):
    drill = Drill.objects.get(id=drill_id)
    set = Set.objects.get(drill=drill,current=True)
    loc_list = StudentLoc.objects.filter(set=set)
    return render_to_response('drill.html', {'drill':drill,'set':set,'loc_list':loc_list})

#ajax request to set instructor location in lat/long
def set_loc(request):
    drill = Drill.objects.get(id=int(request.GET['drill']))
    loc = '%s,%s' % (request.GET['lat'],request.GET['long'])
    if int(request.GET['loc_num']) == 1:
        drill.location_1 = loc
    else:
        drill.location_2 = loc
    drill.save()

    return redirect('/drill/'+str(drill.id))

def next_set(request,drill_id):
    drill = Drill.objects.get(id=drill_id)
    init = Set.objects.get(drill=drill,current=True)
    init.current=False
    init.save()
    try:
        next = Set.objects.get(drill=drill.id,id=init.id+1)
    except:
        next = Set.objects.get(drill=drill.id,number=1)
    next.current=True
    next.save()
    return redirect('/drill/'+drill_id)

def prev_set(request,drill_id):
    drill = Drill.objects.get(id=drill_id)
    init = Set.objects.get(drill=drill,current=True)
    init.current=False
    init.save()
    try:
        prev = Set.objects.get(drill=drill.id,id=init.id-1)
    except:
        last = len(Set.objects.filter(drill=drill.id))
        prev = Set.objects.get(drill=drill.id,number=last)
    prev.current=True
    prev.save()
    return redirect('/drill/'+drill_id)


