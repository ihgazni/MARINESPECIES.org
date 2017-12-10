import navegador5 as nv 
import navegador5.url_tool as nvurl
import navegador5.head as nvhead
import navegador5.body as nvbody
import navegador5.cookie 
import navegador5.cookie.cookie as nvcookie
import navegador5.cookie.rfc6265 as nvrfc6265
import navegador5.jq as nvjq
import navegador5.js_random as nvjr
import navegador5.file_toolset as nvft
import navegador5.shell_cmd as nvsh
import navegador5.html_tool as nvhtml
import navegador5.solicitud as nvsoli
import navegador5.content_parser 
import navegador5.content_parser.amf0_decode as nvamf0
import navegador5.content_parser.amf3_decode as nvamf3

from lxml import etree
import lxml.html
import collections
import copy
import re
import urllib
import os
import json
import sys
import time


from xdict.jprint import  pobj
from xdict.jprint import  print_j_str
from xdict import cmdline





#Taxonomic data
#http://www.marinespecies.org/rest/AphiaChildrenByAphiaID/1?marine_only=false&offset=2 
#-H "accept: application/json"

# /AphiaChildrenByAphiaID/{ID}Get the direct children (max. 50) for a given AphiaID

#get_json
def get_json(info_container):
    js = info_container['resp_body_bytes'].decode('utf-8')
    js = json.loads(js)
    return(js)

#mkdir
def mkdir(path,force=False):
    if(os.path.exists(path)):
        if(force):
            nvsh.pipe_shell_cmds({1:'rm -r '+path})
        else:
            pass
    else:
        os.makedirs(path)

#marinespecies_init
def marinespecies_init(base_url='http://www.marinespecies.org/'):
    info_container = nvsoli.new_info_container()
    info_container['base_url'] = base_url
    info_container['method'] = 'GET'
    req_head_str = '''Accept: application/json\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en;q=1.0, zh-CN;q=0.8'''
    info_container['req_head'] = nvhead.build_headers_dict_from_str(req_head_str,'\r\n')
    info_container['req_head']['Connection'] = 'close'
    #### init records_container
    records_container = nvsoli.new_records_container()
    return((info_container,records_container))

#AphiaChildrenByAphiaID_internal
def AphiaChildrenByAphiaID_internal(info_container,records_container,ID,marine_only=True,offset=1):
    if(marine_only):
        marine_only = 'true'
    else:
        marine_only = 'false'
    url_query_dict = {'marine_only':marine_only,'offset':str(offset)}
    url_dict = {
        'fragment': '', 
        'query_dict': url_query_dict, 
        'host': 'www.marinespecies.org', 
        'port': 80, 
        'params': '', 
        'scheme': 'http', 
        'path': ''.join(('rest/AphiaChildrenByAphiaID/',str(ID))), 
        'netloc': 'www.marinespecies.org'
    }
    url = nvurl.dict_to_url(url_dict).rstrip('#')
    info_container['url'] = url
    info_container = nvsoli.walkon(info_container,records_container=records_container)
    info_container = nvsoli.auto_redireced(info_container,records_container)
    return((info_container,records_container))

#AphiaChildrenByAphiaID
def AphiaChildrenByAphiaID(info_container,records_container,ID,marine_only=True):
    rslt = []
    curr_offset = 1
    info_container,records_container = AphiaChildrenByAphiaID_internal(info_container,records_container,ID,marine_only=marine_only,offset=curr_offset)
    cond = not(info_container['resp_body_bytes'] == b'')
    while(cond):
        js = get_json(info_container)
        rslt = rslt + js
        curr_offset = curr_offset + js.__len__()
        info_container,records_container = AphiaChildrenByAphiaID_internal(info_container,records_container,ID,marine_only=marine_only,offset=curr_offset)
        cond = not(info_container['resp_body_bytes'] == b'')
    #####offset list ready to add 
    return((info_container,records_container,rslt))

#init_level
def init_level(rslt,parent_path = '../Biota/Animalia/Mollusca/Gastropoda/'):
    next_unhandled_arr = []
    for i in range(0,rslt.__len__()):
        ####
        each = rslt[i]
        ####
        #parent_path = '../Biota/'
        dir_name = each['scientificname']
        path = parent_path + dir_name
        if(dir_name in parent_path):
            pass
        else:
            mkdir(path)
            fn = path + '/info.json' 
            nvft.write_to_file(fn=fn,content=json.dumps(each),op='w')
            ####
            ele = {}
            ele['path'] = path
            ele['url'] = each['url']
            ele['ID'] = each['AphiaID']
            ele['rest_url'] = creat_rest_url(ele['ID'])
            ####
            next_unhandled_arr.append(ele)
            fn = path + '/path.json' 
            nvft.write_to_file(fn=fn,content=json.dumps(ele),op='w')
    return(next_unhandled_arr)


####
#creat_rest_url
def creat_rest_url(ID,offset=1,marine_only=True):
    if(marine_only):
        marine_only = 'true'
    else:
        marine_only = 'false'
    url_query_dict = {'marine_only':marine_only,'offset':str(offset)}
    url_dict = {
        'fragment': '',
        'query_dict': url_query_dict,
        'host': 'www.marinespecies.org',
        'port': 80,
        'params': '',
        'scheme': 'http',
        'path': ''.join(('rest/AphiaChildrenByAphiaID/',str(ID))),
        'netloc': 'www.marinespecies.org'
    }
    url = nvurl.dict_to_url(url_dict).rstrip('#')
    return(url)




####parent_path = '../Biota/',ID=1
####info_container,records_container = marinespecies_init()
####info_container,records_container,rslt = AphiaChildrenByAphiaID(info_container,records_container,1,marine_only=True)
####next_unhandled = {}
####for each in rslt:
####    parent_path = '../Biota/'
####    dir_name = each['scientificname']
####    path = parent_path + dir_name
####    if(dir_name in parent_path):
####        pass
####    else:
####        mkdir(path)
####        fn = path + '/info.json'
####        nvft.write_to_file(fn=fn,content=json.dumps(each),op='w')
####        next_unhandled[path] = each['AphiaID']
####        fn = path + '/path.json'
####        nvft.write_to_file(fn=fn,content=json.dumps({path:each['AphiaID']}),op='w')
####

####parent_path = '../Biota/Animalia/Mollusca/Gastropoda/',ID=101
####info_container,records_container = marinespecies_init()
####info_container,records_container,rslt = AphiaChildrenByAphiaID(info_container,records_container,101,marine_only=True)

####




###################################


def crawl_continue(unhandled,next_unhandled,unhandled_start,children_start,info_container,records_container):
    #children_start = 0
    while(unhandled.__len__()>0):
        for i in range(unhandled_start,unhandled.__len__()):
            ele = unhandled[i]
            print(ele)
            parent_path = ele['path']
            ID = ele['ID']
            leaf = 0
            cond = 1
            while(cond):
                try:
                    info_container,records_container,children = AphiaChildrenByAphiaID(info_container,records_container,ID,marine_only=True)
                    if((children == [])&(info_container['resp'].getcode() == 204)):
                        print('Leaf: ' + info_container['url'])
                        leaf = 1
                        cond = 0
                #except AttributeError as Error:
                except:
                    if(info_container['resp_head'] == []):
                        print('No resp: ' + info_container['url'])
                        cond = 1
                        info_container,records_container = marinespecies_init()
                    else:
                        print('Fail: ' + info_container['url'])
                        cond = 1
                        time.sleep(60)
                else:
                    print('Success: ' + info_container['url'])
                    cond = 0
            for j in range(children_start,children.__len__()):
                child = children[j]
                dir_name = child['scientificname']
                if(dir_name in parent_path):
                    pass
                else:
                    ####################
                    if(child['status']=="unaccepted"):
                        #handle,exzample "404961"
                        print('Unaccepted: ' + info_container['url'])
                    else:
                        pass
                    ####################                    
                    path = parent_path + '/' +  dir_name
                    mkdir(path)
                    fn = path + '/info.json'
                    nvft.write_to_file(fn = fn,content=json.dumps(child),op='w')
                    fn = path + '/path.json'
                    nvft.write_to_file(fn=fn,content=json.dumps({path:child['AphiaID']}),op='w')
                    if(child['AphiaID'] == 0):
                        pass
                    else:
                        ele = {}
                        ele['ID'] = child['AphiaID']
                        ele['path'] = path
                        ele['url'] = child['url']
                        ele['rest_url'] = creat_rest_url(ele['ID'])
                        next_unhandled.append(ele)
                    ################
                    fn = '../CONTINUE/children_seq.record'
                    nvft.write_to_file(fn=fn,content=json.dumps({"children":j}),op='w')
                    ################
            ############
            children_start = 0            
            ############
            fn = '../CONTINUE/next_unhandled.json'
            nvft.write_to_file(fn=fn,content=json.dumps(next_unhandled),op='w')
            fn = '../CONTINUE/unhandled.json'
            nvft.write_to_file(fn=fn,content=json.dumps(unhandled),op='w')
            fn = '../CONTINUE/seq.record'
            nvft.write_to_file(fn=fn,content=json.dumps({"unhandled":i}),op='w')
            fn = '../CONTINUE/leaf.record'
            if(leaf == 1):
                nvft.write_to_file(fn=fn,content=os.path.basename(parent_path)+'\n',op='a+')
            else:
                pass
            ########
        #### 
        unhandled = next_unhandled
        next_unhandled = []
        unhandled_start = 0
        ####

#"AphiaID": 0

#######







###########

def get_etree_root(info_container):
    html_text = info_container['resp_body_bytes'].decode('utf-8')
    root = etree.HTML(html_text)
    return(root)


def itertext(ele):
    it = ele.itertext()
    texts = list(it)    
    text = ''
    for i in range(0,texts.__len__()):
        text = text + texts[i]
    return(text)
    

def direct_child_taxa(base_url='http://www.marinespecies.org/'):
    rslt = {}
    root = get_etree_root(info_container)
    eles_dct= root.xpath('//tr/td[@valign="top"]/a')
    for i in range(1,eles_dct.__len__()):
        key = itertext(eles_dct[i])
        if(key):
            href = eles_dct[i].get('href')
            cond = 'taxdetail' in href
            if(cond):
                rslt[key] = base_url + href
    return(rslt)
    

###################################################################


####parent_path = '../Biota/Animalia/Mollusca/Gastropoda/Heterobranchia/Opisthobranchia', ID = 382226
####
info_container,records_container = marinespecies_init()

try:
    ID = int(sys.argv[1])
except:
    ID = 382226
else:
    pass


try:
    parent_path = sys.argv[2]
except:
    parent_path = '../Biota/Animalia/Mollusca/Gastropoda/Heterobranchia/Opisthobranchia/'
else:
    pass


try:
    marine_only = sys.argv[2]
except:
    marine_only = True
else:
    pass


info_container,records_container,rslt = AphiaChildrenByAphiaID(info_container,records_container,ID,marine_only=marine_only)

try:
    content = nvft.read_file_content(fn = '../CONTINUE/seq.record',op='r')
except:
    unhandled_start = 0
else:
    unhandled_start = json.loads(content)['unhandled']

try:
    content = nvft.read_file_content(fn = '../CONTINUE/unhandled.json',op='r')
except:
    unhandled  = init_level(rslt,parent_path = parent_path)
    fn = '../CONTINUE/unhandled.json'
    nvft.write_to_file(fn=fn,content=json.dumps(unhandled),op='w')
else:
    unhandled = json.loads(content)

try:
    content = nvft.read_file_content(fn = '../CONTINUE/next_unhandled.json',op='r')
except:
    next_unhandled = []
else:
    next_unhandled = json.loads(content)

try:
    content = nvft.read_file_content(fn = '../CONTINUE/children_seq.record',op='r')
except:
    children_start = 0
else:
    children_start = json.loads(content)['children']

try:
    content = nvft.read_file_content(fn = '../CONTINUE/leaf.record',op='r')
except:
    nvft.write_to_file(fn=fn,content='',op='w')
else:
    pass



crawl_continue(unhandled,next_unhandled,unhandled_start,children_start,info_container,records_container)
