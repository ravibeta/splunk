from django.contrib.auth.decorators import login_required
from splunkdj.decorators.render import render_to
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from .forms import SecuredIndexForm
import httplib2
import base64
import logging
logger = logging.getLogger('spl.django.service')

user = "ravi"
password = "ravi"
http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
http.add_credentials(user, password)
auth = base64.encodestring(user + ':' + password)
vcocred="Mybase64encodedusernamecolonpassword"
vcoserver="myvcoserverurl"
strategy = "SplunkLDAPStrategy"

@render_to('SplunkAppPrivateIndex:home.html')
@login_required
def home(request):
    return {
        "message": "Hello World from SplunkAppPrivateIndex!",
        "app_name": "SplunkAppPrivateIndex"
    }   
        
@render_to('SplunkAppPrivateIndex:splunk.html')
@login_required
def splunk_view(request):
    service = request.service
    indexes = service.indexes
    return {
        "indexes": indexes
    }

@render_to('SplunkAppPrivateIndex:index.html')
@login_required
def index_create(request):
    service = request.service
    indexname = "reserved_index123"
    indexes = service.indexes
    index = None
    msg = ''
    try:
        if request.GET.get('index') and request.GET['index']:
           indexname = 'reserved_' + request.GET['index']
           index = indexes.create(indexname)
           if index:
               import splunklib.client
               myindex = indexes["logstore_metadata"]
               if myindex:
                  logger.warn('logstore_metadata available as myindex2 at '  + repr(myindex))
                  #myindex.submit("This is my Metadata event", sourcetype="logstore_metadata.log", host="local")
                  mysocket = myindex.attach()
                  mysocket.send("user=" + service.username + " method=create indexname=" + indexname + " created event\r\n")
                  mysocket.close()
                  """
                  mysocket = myindex.attach()
                  mysocket.send("user="+service.username+ " method=create indexname=" + indexname)
                  mysocket.close()
                  logger.warn('myindex='+repr(myindex))
                  #myindex.submit("user="+service.username+ " method=create indexname=" + indexname)
                  import socket
                  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  s.connect(('10.5.184.254', 9999))
                  s.send("user="+service.username+ " method=create indexname=" + indexname)
                  #data = s.recv(1024)
                  s.close()
                  """
           msg = indexname + ' created'
        else:
           msg = 'You have not specified an index in the query string.'
    except:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        return {
               'status': 'error',
               'msg': repr(traceback.format_exception(exc_type, exc_value, exc_traceback)),
               'index' : index
               }
    finally:
        pass
    return {
        'status': 'success',
        'msg': msg,
        'index': index
    }

@render_to('SplunkAppPrivateIndex:splunk.html')
@login_required
def index_delete(request):
    service = request.service
    indexname = "reserved_index123"
    indexes = service.indexes
    index = None
    msg = ''
    try:
        if request.GET.get('index') and request.GET['index']:
           if 'reserved_' not in request.GET['index']:
               indexname = 'reserved_' + request.GET['index']
           else:
               indexname = request.GET['index']
           for item in indexes.list():
               if item.name and indexname == item.name:
                  item.delete()
                  import splunklib.client
                  myindex = indexes["logstore_metadata"]
                  if myindex:
                     mysocket = myindex.attach()
                     mysocket.send("user=" + service.username + " method=delete indexname=" + indexname + " deleted event\r\n")
                     mysocket.close()
    except:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        return {
               'status': 'error',
               'msg': repr(traceback.format_exception_only(exc_type, exc_value)),
               'indexes' : indexes
               }
    finally:
        pass
    indexes = service.indexes
    return {
        "msg" : msg,
        "indexes": indexes
    }


@render_to('SplunkAppPrivateIndex:roles.html')
@login_required
def role_view(request):
    service = request.service
    roles = service.roles
    return {
        "roles":roles
    }

@render_to('SplunkAppPrivateIndex:role.html')
@login_required
def role_create(request):
    service = request.service
    rolename = "reserved_index123"
    roles = service.roles
    role = None
    msg = ''
    allowed = ''
    try:
        if request.GET.get('role') and request.GET['role']:
           rolename = 'reserved_' + request.GET['role']
           if request.GET.get('srchIndexesAllowed') and request.GET['srchIndexesAllowed']:
              allowed = request.GET['srchIndexesAllowed']
           if allowed:
              role = roles.create(rolename, srchIndexesAllowed=allowed)
           else:
              role = roles.create(rolename)
           if role:
               import splunklib.client
               myindex = service.indexes["logstore_metadata"]
               if myindex:
                  mysocket = myindex.attach()
                  mysocket.send("user="+service.username+ " method=create rolename=" + rolename)
                  mysocket.close()
                  #logger.warn('myindex='+repr(myindex))
                  #myindex.submit("user="+service.username+ " method=create rolename=" + rolename)
           msg = rolename + ' created'
        else:
           msg = 'You have not specified an role in the query string.'
    except:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        return {
               'status': 'error',
               'msg': repr(traceback.format_exception_only(exc_type, exc_value)),
               'role' : role
               }
    finally:
        pass
    return {
        'status': 'success',
        'msg': msg,
        'role': role
    }

@render_to('SplunkAppPrivateIndex:roles.html')
@login_required
def role_delete(request):
    service = request.service
    rolename = "reserved_index123"
    roles = service.roles
    role = None
    msg = ''
    try:
        if request.GET.get('role') and request.GET['role']:
           if 'reserved_' not in request.GET['role']:
               rolename = 'reserved_' + request.GET['role']
           else:
               rolename = request.GET['role']
           for item in roles.list():
               if item.name and rolename == item.name:
                  item.delete()
                  import splunklib.client
                  myindex = indexes["logstore_metadata"]
                  if myindex:
                     mysocket = myindex.attach()
                     mysocket.send("user=" + service.username + " method=delete rolename=" + rolename + " deleted event\r\n")
                     mysocket.close()
    except:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        return {
               'status': 'error',
               'msg': repr(traceback.format_exception_only(exc_type, exc_value)),
               'roles' : roles
               }
    finally:
        pass
    roles = service.roles
    return {
        "msg" : msg,
        "roles": roles
    }


@render_to('SplunkAppPrivateIndex:securedindex.html')
@login_required
@csrf_exempt
def securedindex_form_process(request):
    if request.method == 'GET':
        form = SecuredIndexForm()
        return render(request, 'securedindex.html', {
               'form': form,
               })
    import sys
    import string
    import random
    import json
    import urllib
    import httplib2
    http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
    #http.add_credentials(user, password)

    indexname = ''.join([random.choice(string.digits + string.ascii_uppercase) for x in range(0, 6)])
    rolename = 'role_' + indexname
    groupname = 'itcloudgroup_' + indexname
    service = request.service
    indexes = service.indexes
    index=None
    msg = ''
    try:
        if request.POST.get('index_name'):
           indexname = request.POST['index_name']
        if request.POST.get('role_name'):
           rolename = request.POST['role_name']
        if request.POST.get('group_name'):
           groupname = request.POST['group_name']
        logger.info('Creating a secured index with index_name='+indexname+' and role='+rolename+' and security group=' + groupname)
        if indexname:
           existingIndex = None
           if indexname in service.indexes and service.indexes[indexname]:
              existingIndex = service.indexes[indexname]
           if not existingIndex:
              index = indexes.create(indexname)
              if index:
                 import splunklib.client
                 myindex = indexes["logstore_metadata"]
                 if myindex:
                    logger.warn('logstore_metadata available as myindex2 at '  + repr(myindex))
                    #myindex.submit("This is my Metadata event", sourcetype="logstore_metadata.log", host="local")
                    mysocket = myindex.attach()
                    mysocket.send("user=" + service.username + " method=create indexname=" + indexname + " created event\r\n")
                    mysocket.close()
              else:
                 return HttpResponse('index ' + indexname + ' creation failed.')
              msg = indexname + ' created'
              logger.info(msg)
           else:
              logger.info('Index already existing by name: ' + indexname)  
        allowed = indexname
        if rolename:
           existingRole = None
           if rolename in service.roles and service.roles[rolename]:
              existingRole = service.roles[rolename]
           if not existingRole:
              if allowed:
                 role = service.roles.create(rolename, srchIndexesAllowed=allowed)
              else:
                 role = service.roles.create(rolename)
              if role:
                 import splunklib.client
                 myindex = service.indexes["logstore_metadata"]
                 if myindex:
                    mysocket = myindex.attach()
                    mysocket.send("user="+service.username+ " method=create rolename=" + rolename)
                    mysocket.close()
                    #logger.warn('myindex='+repr(myindex))
                    #myindex.submit("user="+service.username+ " method=create rolename=" + rolename)
                    msg = rolename + ' created'
                    logger.info(msg)
              else:
                 return HttpResponse('role ' + rolename + ' creation failed.')
           else:
              logger.info('Role already existing by name: ' + rolename)
        else:
            logger.warn(rolename + ' not specified.')
        name = groupname
        #the url already checks if group is existing, don't need to repeat it here
        url = vcoserver + '/vco/api/workflows/faa723e7-cf2f-45be-83fc-85ee59c9c437/executions/'
        headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Basic "+vcocred}
        params = {"parameters":[{"value":{"string":{"value": name }},"type":"string","name":"groupName","scope":"local"},{"value":{"string":{"value":str(len(name))}},"type":"string","name":"length","scope":"local"}]}
        print 'params='+repr(params)
        sys.stdout.flush()
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(params))
        print 'response=' + repr(response)
        print 'content=' + repr(content)
        if response.status != 202:
           return HttpResponse(json.dumps({'status':'error', 'msg': 'VCO did not respond favorably'}))
        newrun = response['location']
        import time
        time.sleep(1)
        response, content = http.request(newrun, 'GET', headers=headers)
        print 'content=' + repr(content)
        if response.status != 200:
           return HttpResponse('group ' + groupname + ' creation failed.')
        logger.info('security group created: ' + repr(content))
        with open("/apps/splunk/etc/system/local/authentication.conf", "ab") as myfile:
             myfile.write("[roleMap_"+ strategy + "]\r\nuser = " + groupname)
        logger.info('group mapping entry added to conf')
        group = groupname
        user  = 'vcoaprod'
        url = vcoserver + '/vco/api/workflows/a2f56b22-4110-45e7-9c0f-fd517a067050/executions'
        headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Basic "+vcocred}
        params = {"parameters":[{"value":{"string":{"value": group }},"type":"string","name":"groupName","scope":"local"},{"value":{"string":{"value":str(len(group))}},"type":"string","name":"length","scope":"local"}, {"value":{"string":{"value": user }},"type":"string","name":"userName","scope":"local"},{"value":{"string":{"value":str(len(user))}},"type":"string","name":"length","scope":"local"}]}
        print 'params='+repr(params)
        sys.stdout.flush()
        response, content = http.request(url,'POST', headers=headers, body=json.dumps(params))
        print 'response=' + repr(response)
        print 'content=' + repr(content)
        if response.status != 202:
           return HttpResponse(json.dumps({'status':'error', 'msg': 'VCO did not respond favorably'}), status=response.status)
        newrun = response['location']
        import time
        time.sleep(1)
        response, content = http.request(newrun, 'GET', headers=headers)
        print 'content=' + repr(content)
        logger.info(repr(content))
        if response.status != 200:
           return HttpResponse(json.dumps({'status':'error', 'msg': 'VCO did not respond favorably' + content}), status = response.status)
        indexport = ''
        unique = False
        retry = 0
        while not unique:
            if retry > 3:
               break
            retry = retry + 1
            import random
            name = '63' + ''.join([random.choice(string.digits) for x in range(0, 3)]) # port
            indexport = name
            url = 'https://127.0.0.1:8089/services/data/inputs/tcp/raw?output_mode=json'
            response, content = http.request(url,
            headers={"Content-Type": "application/json", 'Authorization' : 'Basic ' + auth})
            if response.status != 200:
               logger.error("tcp input port for index:"+indexname +"could not be opened - skipping")
               break
            if name in content:
               logger.error("tcp input port:"+name+" for index:"+indexname +"already exists - skipping")
               continue;
            unique = True
        if unique:
            params = urllib.urlencode({'name':name, 'index':indexname, 'source':role, 'sourcetype':'tcp', 'queue': 'indexQueue'})
            url = 'https://127.0.0.1:8089/services/data/inputs/tcp/raw?output_mode=json'
            response, content = http.request(url, 'POST', params,
            headers={"Content-Type": "application/json", 'Authorization' : 'Basic ' + auth})
            if response.status != 201:
               msg = content
               msg = HttpResponse(json.dumps({
                      'status': 'error',
                      'msg': 'Status=' + response.status + ' ' + msg,
                      'indexport' : indexport
                      }), status=response.status)
            else:
                msg = 'Status=200 Port: ' + indexport + ' created & assigned for data input to index ' + indexname + '. Save this port number for your records.'
        reply = 'SUCCESS: Index: ' + indexname + ' created and secured with role: ' + rolename + ' mapped to security group: ' + groupname + '.Click <a href=\"/dj/en-us/SplunkAppPrivateIndex/home/\">here</a> to return home.'
        if indexport:
            reply = reply + msg
        return HttpResponse(reply)
        #return HttpResponse('SUCCESS: Index: ' + indexname + ' created and secured with role: ' + rolename + ' mapped to security group: ' + groupname + '.Click <a href=\"/dj/en-us/SplunkAppPrivateIndex/home/\">here</a> to return home.'+msg)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        msg = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print msg # for Loggregator
        sys.stdout.flush()
        logger.warn(msg)
        return HttpResponse(json.dumps({
               'status': 'error',
               'msg': msg
               }))
    finally:
        pass
    pass

@csrf_exempt
@login_required
def port_create(request, internal=False):
    import json
    service = request.service
    indexname = "reserved_index123"
    indexes = service.indexes
    index = None
    msg = ''
    indexport = ''
    name = ''
    try:
        if request.POST.get('index_name') and request.POST['index_name']:
           indexname = request.POST['index_name']
        indexport = ''
        unique = False
        retry = 0
        while not unique:
            if retry > 3:
               break
            retry = retry + 1
            import random
            name = '63' + ''.join([random.choice(string.digits) for x in range(0, 3)]) # port
            indexport = name
            url = 'https://127.0.0.1:8089/services/data/inputs/tcp/raw?output_mode=json'
            response, content = http.request(url,
            headers={"Content-Type": "application/json", 'Authorization' : 'Basic ' + auth})
            if response.status != 200:
               logger.error("tcp input port for index:"+index +"could not be opened - skipping")
               break
            if name in content:
               logger.error("tcp input port:"+name+" for index:"+index +"already exists - skipping")
               continue;
            unique = True
        if unique:
            params = urllib.urlencode({'name':name, 'index':indexname, 'source':role, 'sourcetype':'tcp', 'queue': 'indexQueue'})
            url = 'https://127.0.0.1:8089/services/data/inputs/tcp/raw?output_mode=json'
            response, content = http.request(url, 'POST', params,
            headers={"Content-Type": "application/json", 'Authorization' : 'Basic ' + auth})
            if response.status != 201:
               msg = content
               msg = json.dumps({
                      'status': 'error',
                      'msg': 'Status=' + response.status + ' ' + msg,
                      'indexport' : indexport
                      })
               if not internal:
                  return HttpResponse(msg)
            else:
                msg = 'Status=200 Port: ' + indexport + ' created & assigned for data input to index ' + indexname + '.'
        else:
           msg = 'You have not specified an index in the query string.'
    except:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        msg = json.dumps({
               'status': 'error',
               'msg': 'Status=500 ' + repr(traceback.format_exception(exc_type, exc_value, exc_traceback)),
               'indexport' : indexport
               })
        if not internal:
          return HttpResponse(msg)
    finally:
        msg  = json.dumps({
               'status': 'success',
               'msg': 'Status=200 ' + msg,
               'port': indexport 
        })
        if not internal:
           return HttpResponse(msg)
        pass
