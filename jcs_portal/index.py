# coding: utf-8
import xmlrpclib
from flask import Flask, render_template, redirect,jsonify,request,make_response,Response,send_file, send_from_directory
from xmlrpclib import ServerProxy
import random,time,os,sys

app = Flask(__name__)
CLOUD_PROXY = {
    'proto': 'http',
    'host': 'your-ip-address-here',
    'port': '8888',
}

user_name = "cloudfs"
local_download_path = "/home/cloudfs/tmp/download/"
local_upload_path_windows = ""
local_upload_path_linux = "/home/cloudfs/tmp/upload/"
cloud_dict={u'jcsproxy-aliyun-qingdao':['阿里云-青岛', [120.4058131861,36.0373135384],[56,64],"#FA6B04"],
    u'jcsproxy-aliyun-beijing':['阿里云-北京', [116.589392,40.863174],[19,73],"#FA6B04"],
    u'jcsproxy-aliyun-zhangjiakou':['阿里云-张家口', [114.8850547325,40.7697837132],[34,75],"#FA6B04"],
    u'jcsproxy-aliyun-hangzhou':['阿里云-杭州', [120.1530293773,30.1510512690],[65,52],"#FA6B04"],
    u'jcsproxy-aliyun-shanghai':['阿里云-上海', [121.22551,31.771022],[54,50],"#FA6B04"],
    u'jcsproxy-aliyun-shenzhen':['阿里云-深圳', [114.0776336847,22.4877890441],[14,21],"#FA6B04"],
    u'jcsproxy-aliyun-huhehaote':['阿里云-呼和浩特', [111.8034594563,40.5863721864],[10,10],"#FA6B04"],
    u'jcsproxy-baidu-beijing':['百度云-北京', [117.178105,40.217526],[29,70],"#4472C4"],
    u'jcsproxy-baidu-suzhou':['百度云-苏州', [120.5814138099,31.3034063568],[65,48], "#4472C4"],
    u'jcsproxy-baidu-guangzhou':['百度云-广州', [113.3084422684,23.1162839543],[20,20], "#4472C4"],
    u'jcsproxy-ksyun-beijing':['金山云-北京', [115.651129,39.679441],[30,80], "#7030A0"],
    u'jcsproxy-ksyun-shanghai':['金山云-上海', [121.22551,31.271022],[73,52], "#7030A0"],
    u'jcsproxy-aliyun-qingdao-low':['阿里云-青岛-low', [120.9058131861,36.0373135384],[60,64],"#FA6B04"],
    u'jcsproxy-aliyun-beijing-low':['阿里云-北京-low', [117.089392,40.863174],[23,73],"#FA6B04"],
    u'jcsproxy-aliyun-zhangjiakou-low':['阿里云-张家口-low', [115.3850547325,40.7697837132],[37,75],"#FA6B04"],
    u'jcsproxy-aliyun-hangzhou-low':['阿里云-杭州-low', [120.6530293773,30.1510512690],[68,52],"#FA6B04"],
    u'jcsproxy-aliyun-shanghai-low':['阿里云-上海-low', [121.72551,31.771022],[57,50],"#FA6B04"],
    u'jcsproxy-aliyun-shenzhen-low':['阿里云-深圳-low', [114.5776336847,22.4877890441],[17,21],"#FA6B04"],
    u'jcsproxy-aliyun-huhehaote-low':['阿里云-呼和浩特-low', [112.3034594563,40.5863721864],[10,10],"#FA6B04"],
    u'jcsproxy-baidu-beijing-low':['百度云-北京-low', [117.678105,40.217526],[32,70], "#4472C4"],
    u'jcsproxy-baidu-suzhou-low':['百度云-苏州-low', [121.0814138099,31.3034063568],[68,48], "#4472C4"],
    u'jcsproxy-baidu-guangzhou-low':['百度云-广州-low', [113.8084422684,23.1162839543],[25,20], "#4472C4"]}
def gen_url(proxy):
    return "%s://%s:%s" % (proxy['proto'], proxy['host'], proxy['port'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cloud')
def cloudindex():
    return render_template('index.html')
@app.route('/data/map')
def mapindex():
    return render_template('index.html')
@app.route('/data/list')
def dataindex():
    return render_template('index.html')
@app.route('/user/user')
def userindex():
    return render_template('index.html')
@app.route('/user/login')
def loginindex():
    return render_template('index.html')
@app.route('/user/register')    
def registerindex():
    return render_template('index.html')

@app.route('/__webpack_hmr')
def npm():
    return redirect('http://120.131.11.139:5001/__webpack_hmr')

@app.route('/api/cloud/get', methods=['POST'])
def get():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    dir=request.json['params']['dir']
    user_name=request.json['params']['user']
    result = proxy.list_dir(user_name,dir)
    print user_name
    print result
    for k,value in enumerate(result['result']):
        tmp=[False,False,False]
        tmp2=[]
        if value['isdir'] == False:
            for v in value['cloud_block_path_dict']:
                if 'aliyun' in v:
                    tmp[0]=True
                elif 'baidu' in v:
                    tmp[1]=True
                elif 'ksyun' in v:
                    tmp[2]=True
                tmp2.append(cloud_dict[v][0])
            result['result'][k]['cloud_block_area']=tmp
            result['result'][k]['cloud_block_name']=tmp2

    return jsonify(result)

@app.route('/api/cloud/create', methods=['POST'])
def create():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    dir=request.json['dir']
    user_name=request.json['user']
    result = proxy.create_dir(user_name,dir)
    return jsonify(result)

@app.route('/api/cloud/delete_file', methods=['POST'])
def delete_file():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    dir=request.json['dir']
    user_name=request.json['user']
    result = proxy.delete_file(user_name,dir)
    return jsonify(result)

@app.route('/api/cloud/delete_dir', methods=['POST'])
def delete_dir():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    dir=request.json['dir']
    user_name=request.json['user']
    result = proxy.delete_dir(user_name,dir,True)
    return jsonify(result)

@app.route('/api/cloud/download', methods=['POST'])
def download():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    dir=request.json['dir']
    user_name=request.json['user']
    result = proxy.get_file(user_name,dir,os.path.join(local_download_path+dir.split('/')[-1]))
    return send_from_directory(local_download_path, dir.split('/')[-1], as_attachment=True)

@app.route('/api/cloud/upload', methods=['POST'])
def upload():
    form=request.form.to_dict()
    dir=form['dir']
    f=request.files['file']
    f.save(os.path.join(local_upload_path_linux, f.filename))
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    if dir!='':
        dir+='/'
    dir+=f.filename
    user_name=form['user']
    result = proxy.put_file(user_name, dir,os.path.join(local_upload_path_linux, f.filename))
    return jsonify(result)

@app.route('/api/user/register', methods=['GET', 'POST'])
def register():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    name=request.json['params']['name']
    password=request.json['params']['password']
    result = proxy.create_user(name, password)
    return jsonify(result)
@app.route('/api/user/login', methods=['GET', 'POST'])
def login():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    name=request.json['params']['name']
    result = proxy.get_user(name)
    return jsonify(result)
@app.route('/api/user/edit', methods=['GET', 'POST'])
def edit():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    name=request.json['form']['name']
    password=request.json['form']['password']
    others={'phone':request.json['form']['phone'],'mail':request.json['form']['mail']}
    result = proxy.update_user(name,password,others)
    return jsonify(result)
@app.route('/api/user/stat', methods=['GET', 'POST'])
def stat():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    name=request.json['form']['name']
    result = {'save':proxy.user_used_storage(name),'traffic':proxy.user_used_traffic(name)}
    return jsonify(result)

@app.route('/api/cloud/search', methods=['GET', 'POST'])
def search():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    name=request.json['input']
    user_name=request.json['user']
    result = proxy.search_file(user_name,name)
    return jsonify(result)

@app.route('/api/data/map', methods=['POST'])

def map():
    cloud_dict={
    u'shaoly-aliyun-qingdao':['阿里云-青岛', [120.4058131861,36.0373135384],[56,64],"#FA6B04"],
    u'shaoly-aliyun-shanghai':['阿里云-上海', [121.22551,31.771022],[54,50],"#FA6B04"],
    u'ks3test-bj':['金山云-北京', [115.651129,39.679441],[30,80], "#7030A0"],
    u'jcsproxy-aliyun-qingdao':['阿里云-青岛', [120.4058131861,36.0373135384],[56,64],"#FA6B04"],
    u'jcsproxy-aliyun-beijing':['阿里云-北京', [116.589392,40.863174],[19,73],"#FA6B04"],
    u'jcsproxy-aliyun-zhangjiakou':['阿里云-张家口', [114.8850547325,40.7697837132],[34,75],"#FA6B04"],
    u'jcsproxy-aliyun-hangzhou':['阿里云-杭州', [120.1530293773,30.1510512690],[65,52],"#FA6B04"],
    u'jcsproxy-aliyun-shanghai':['阿里云-上海', [121.22551,31.771022],[54,50],"#FA6B04"],
    u'jcsproxy-aliyun-shenzhen':['阿里云-深圳', [114.0776336847,22.4877890441],[14,21],"#FA6B04"],
    u'jcsproxy-aliyun-huhehaote':['阿里云-呼和浩特', [111.8034594563,40.5863721864],[2,74],"#FA6B04"],
    u'jcsproxy-baidu-beijing':['百度云-北京', [117.178105,40.217526],[29,70],"#4472C4"],
    u'jcsproxy-baidu-suzhou':['百度云-苏州', [120.5814138099,31.3034063568],[65,48], "#4472C4"],
    u'jcsproxy-baidu-guangzhou':['百度云-广州', [113.3084422684,23.1162839543],[20,20], "#4472C4"],
    u'jcsproxy-ksyun-beijing':['金山云-北京', [115.651129,39.679441],[30,80], "#7030A0"],
    u'jcsproxy-ksyun-shanghai':['金山云-上海', [121.22551,31.271022],[73,52], "#7030A0"],
    u'jcsproxy-aliyun-qingdao-low':['阿里云-青岛-low', [120.9058131861,36.0373135384],[60,64],"#FA6B04"],
    u'jcsproxy-aliyun-beijing-low':['阿里云-北京-low', [117.089392,40.863174],[23,73],"#FA6B04"],
    u'jcsproxy-aliyun-zhangjiakou-low':['阿里云-张家口-low', [115.3850547325,40.7697837132],[37,75],"#FA6B04"],
    u'jcsproxy-aliyun-hangzhou-low':['阿里云-杭州-low', [120.6530293773,30.1510512690],[68,52],"#FA6B04"],
    u'jcsproxy-aliyun-shanghai-low':['阿里云-上海-low', [121.72551,31.771022],[57,50],"#FA6B04"],
    u'jcsproxy-aliyun-shenzhen-low':['阿里云-深圳-low', [114.5776336847,22.4877890441],[17,21],"#FA6B04"],
    u'jcsproxy-aliyun-huhehaote-low':['阿里云-呼和浩特-low', [112.3034594563,40.5863721864],[3,74],"#FA6B04"],
    u'jcsproxy-baidu-beijing-low':['百度云-北京-low', [117.678105,40.217526],[32,70], "#4472C4"],
    u'jcsproxy-baidu-suzhou-low':['百度云-苏州-low', [121.0814138099,31.3034063568],[68,48], "#4472C4"],
    u'jcsproxy-baidu-guangzhou-low':['百度云-广州-low', [113.8084422684,23.1162839543],[25,20], "#4472C4"]}
    tran_dict={'aliyun-beijing':u'jcsproxy-aliyun-beijing','aliyun-shanghai':u'jcsproxy-aliyun-shanghai','aliyun-shenzhen':u'jcsproxy-aliyun-shenzhen'}
    cloud_list = [u'jcsproxy-aliyun-qingdao', u'jcsproxy-aliyun-beijing', u'jcsproxy-aliyun-zhangjiakou',
                  u'jcsproxy-aliyun-hangzhou',
                  u'jcsproxy-aliyun-shanghai', u'jcsproxy-aliyun-shenzhen', u'jcsproxy-aliyun-huhehaote',
                  u'jcsproxy-baidu-beijing', u'jcsproxy-baidu-suzhou',
                  u'jcsproxy-baidu-guangzhou', u'jcsproxy-ksyun-beijing', u'jcsproxy-ksyun-shanghai',
                  u'jcsproxy-aliyun-qingdao-low', u'jcsproxy-aliyun-beijing-low',
                  u'jcsproxy-aliyun-zhangjiakou-low', u'jcsproxy-aliyun-hangzhou-low', u'jcsproxy-aliyun-shanghai-low',
                  u'jcsproxy-aliyun-shenzhen-low',
                  u'jcsproxy-aliyun-huhehaote-low', u'jcsproxy-baidu-beijing-low', u'jcsproxy-baidu-suzhou-low',
                  u'jcsproxy-baidu-guangzhou-low']
    cloud_block = [[30, 75,"北京地区"],[65, 50,"上海地区"],[20, 20,"广东地区"]]

    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    result1 = proxy.cloud_used_storage()
    print result1
    result2 = proxy.jcsproxy_multicloud_traffic()

    cloud_used_storage=[]
    for k in cloud_dict:
        if k in result1['result']['cloud_used_storage']:
            tmp=[cloud_dict[k][2][0],cloud_dict[k][2][1],cloud_dict[k][0],cloud_dict[k][3],result1['result']['cloud_used_storage'][k]]
        else:
            tmp=[cloud_dict[k][2][0],cloud_dict[k][2][1],cloud_dict[k][0],cloud_dict[k][3],0]
        cloud_used_storage.append(tmp)

    cloud_trans=[]

    for k in result2['result']['jcsproxy_area']:
        if 'get_file' in result2['result']['jcsproxy_area'][k]:
            for k2 in result2['result']['jcsproxy_area'][k]['get_file']:
                if k2==tran_dict[k]:
                    continue
                tmp=[cloud_dict[k2][0],cloud_dict[k2][2][0],cloud_dict[k2][2][1],cloud_dict[tran_dict[k]][0],cloud_dict[tran_dict[k]][2][0],cloud_dict[tran_dict[k]][2][1],result2['result']['jcsproxy_area'][k]['get_file'][k2],cloud_dict[tran_dict[k]][3]]
                cloud_trans.append(tmp)
        if 'put_file' in result2['result']['jcsproxy_area'][k]:
            for k2 in result2['result']['jcsproxy_area'][k]['put_file']:
                if k2==tran_dict[k]:
                    continue
                tmp=[cloud_dict[tran_dict[k]][0],cloud_dict[tran_dict[k]][2][0],cloud_dict[tran_dict[k]][2][1],cloud_dict[k2][0],cloud_dict[k2][2][0],cloud_dict[k2][2][1],result2['result']['jcsproxy_area'][k]['put_file'][k2],cloud_dict[k2][3]]
                cloud_trans.append(tmp)

    cloud_bar=[]
    tmp,tmp2=[],[]
    for k in cloud_list:
        tmp.append(cloud_dict[k][0])
        if k in result1['result']['cloud_used_storage']:
            tmp2.append(result1['result']['cloud_used_storage'][k])
        else:
            tmp2.append(0)
    cloud_bar.append(tmp)
    cloud_bar.append(tmp2)

    cloud_statistics = {}
    cloud_statistics['cloud_used_storage'] = cloud_used_storage
    cloud_statistics['file_used_storage'] = result1['result']['file_used_storage']
    cloud_statistics['redundant_used_storage'] = result1['result']['redundant_used_storage']
    cloud_statistics['cloud_block'] = cloud_block
    cloud_statistics['cloud_trans'] = cloud_trans
    cloud_statistics['cloud_bar'] = cloud_bar

    return jsonify(cloud_statistics) # 返回json 格式
@app.route('/api/user/map', methods=['GET', 'POST'])
def umap():
    proxy = ServerProxy(gen_url(CLOUD_PROXY))
    name=request.json['form']['name']
    cloud_dict={u'jcsproxy-aliyun-qingdao':['阿里云-青岛', [120.4058131861,36.0373135384],[56,64],"#FA6B04"],
    u'jcsproxy-aliyun-beijing':['阿里云-北京', [116.589392,40.863174],[19,73],"#FA6B04"],
    u'jcsproxy-aliyun-zhangjiakou':['阿里云-张家口', [114.8850547325,40.7697837132],[34,75],"#FA6B04"],
    u'jcsproxy-aliyun-hangzhou':['阿里云-杭州', [120.1530293773,30.1510512690],[65,52],"#FA6B04"],
    u'jcsproxy-aliyun-shanghai':['阿里云-上海', [121.22551,31.771022],[54,50],"#FA6B04"],
    u'jcsproxy-aliyun-shenzhen':['阿里云-深圳', [114.0776336847,22.4877890441],[14,21],"#FA6B04"],
    u'jcsproxy-aliyun-huhehaote':['阿里云-呼和浩特', [111.8034594563,40.5863721864],[10,10],"#FA6B04"],
    u'jcsproxy-baidu-beijing':['百度云-北京', [117.178105,40.217526],[29,70],"#4472C4"],
    u'jcsproxy-baidu-suzhou':['百度云-苏州', [120.5814138099,31.3034063568],[65,48], "#4472C4"],
    u'jcsproxy-baidu-guangzhou':['百度云-广州', [113.3084422684,23.1162839543],[20,20], "#4472C4"],
    u'jcsproxy-ksyun-beijing':['金山云-北京', [115.651129,39.679441],[30,80], "#7030A0"],
    u'jcsproxy-ksyun-shanghai':['金山云-上海', [121.22551,31.271022],[73,52], "#7030A0"],
    u'jcsproxy-aliyun-qingdao-low':['阿里云-青岛-low', [120.9058131861,36.0373135384],[60,64],"#FA6B04"],
    u'jcsproxy-aliyun-beijing-low':['阿里云-北京-low', [117.089392,40.863174],[23,73],"#FA6B04"],
    u'jcsproxy-aliyun-zhangjiakou-low':['阿里云-张家口-low', [115.3850547325,40.7697837132],[37,75],"#FA6B04"],
    u'jcsproxy-aliyun-hangzhou-low':['阿里云-杭州-low', [120.6530293773,30.1510512690],[68,52],"#FA6B04"],
    u'jcsproxy-aliyun-shanghai-low':['阿里云-上海-low', [121.72551,31.771022],[57,50],"#FA6B04"],
    u'jcsproxy-aliyun-shenzhen-low':['阿里云-深圳-low', [114.5776336847,22.4877890441],[17,21],"#FA6B04"],
    u'jcsproxy-aliyun-huhehaote-low':['阿里云-呼和浩特-low', [112.3034594563,40.5863721864],[17,50],"#FA6B04"],
    u'jcsproxy-baidu-beijing-low':['百度云-北京-low', [117.678105,40.217526],[32,70], "#4472C4"],
    u'jcsproxy-baidu-suzhou-low':['百度云-苏州-low', [121.0814138099,31.3034063568],[68,48], "#4472C4"],
    u'jcsproxy-baidu-guangzhou-low':['百度云-广州-low', [113.8084422684,23.1162839543],[25,20], "#4472C4"]}
    tran_dict={'aliyun-beijing':u'jcsproxy-aliyun-beijing','baidu-beijing':u'jcsproxy-baidu-beijing','ksyun-beijing':u'jcsproxy-ksyun-beijing'}
    cloud_block = [[30, 75,"北京地区"],[65, 50,"上海地区"],[20, 20,"广东地区"]]
    cloud_list = [u'jcsproxy-aliyun-qingdao', u'jcsproxy-aliyun-beijing', u'jcsproxy-aliyun-zhangjiakou',
                  u'jcsproxy-aliyun-hangzhou',
                  u'jcsproxy-aliyun-shanghai', u'jcsproxy-aliyun-shenzhen', u'jcsproxy-aliyun-huhehaote',
                  u'jcsproxy-baidu-beijing', u'jcsproxy-baidu-suzhou',
                  u'jcsproxy-baidu-guangzhou', u'jcsproxy-ksyun-beijing', u'jcsproxy-ksyun-shanghai',
                  u'jcsproxy-aliyun-qingdao-low', u'jcsproxy-aliyun-beijing-low',
                  u'jcsproxy-aliyun-zhangjiakou-low', u'jcsproxy-aliyun-hangzhou-low', u'jcsproxy-aliyun-shanghai-low',
                  u'jcsproxy-aliyun-shenzhen-low',
                  u'jcsproxy-aliyun-huhehaote-low', u'jcsproxy-baidu-beijing-low', u'jcsproxy-baidu-suzhou-low',
                  u'jcsproxy-baidu-guangzhou-low']
    result1=proxy.user_used_storage(name)
    result2=proxy.user_multicloud_traffic(name)
    cloud_used_storage=[]
    for k in cloud_dict:
        if k in result1['result']['cloud_used_storage']:
            tmp=[cloud_dict[k][2][0],cloud_dict[k][2][1],cloud_dict[k][0],cloud_dict[k][3],result1['result']['cloud_used_storage'][k]]
        else:
            tmp=[cloud_dict[k][2][0],cloud_dict[k][2][1],cloud_dict[k][0],cloud_dict[k][3],0]
        cloud_used_storage.append(tmp)

    cloud_trans=[]

    for k in result2['result']['jcsproxy_area']:
        if 'get_file' in result2['result']['jcsproxy_area'][k]:
            for k2 in result2['result']['jcsproxy_area'][k]['get_file']:
                if k2==tran_dict[k]:
                    continue
                tmp=[cloud_dict[k2][0],cloud_dict[k2][2][0],cloud_dict[k2][2][1],cloud_dict[tran_dict[k]][0],cloud_dict[tran_dict[k]][2][0],cloud_dict[tran_dict[k]][2][1],result2['result']['jcsproxy_area'][k]['get_file'][k2],cloud_dict[tran_dict[k]][3]]
                cloud_trans.append(tmp)
        if 'put_file' in result2['result']['jcsproxy_area'][k]:
            for k2 in result2['result']['jcsproxy_area'][k]['put_file']:
                if k2==tran_dict[k]:
                    continue
                tmp=[cloud_dict[tran_dict[k]][0],cloud_dict[tran_dict[k]][2][0],cloud_dict[tran_dict[k]][2][1],cloud_dict[k2][0],cloud_dict[k2][2][0],cloud_dict[k2][2][1],result2['result']['jcsproxy_area'][k]['put_file'][k2],cloud_dict[k2][3]]
                cloud_trans.append(tmp)

    cloud_bar=[]
    tmp,tmp2=[],[]
    for k in cloud_list:
        tmp.append(cloud_dict[k][0])
        if k in result1['result']['cloud_used_storage']:
            tmp2.append(result1['result']['cloud_used_storage'][k])
        else:
            tmp2.append(0)
    cloud_bar.append(tmp)
    cloud_bar.append(tmp2)

    cloud_statistics = {}
    cloud_statistics['cloud_used_storage'] = cloud_used_storage
    cloud_statistics['file_used_storage'] = result1['result']['file_used_storage']
    cloud_statistics['redundant_used_storage'] = result1['result']['redundant_used_storage']
    cloud_statistics['cloud_block'] = cloud_block
    cloud_statistics['cloud_trans'] = cloud_trans
    cloud_statistics['cloud_bar'] = cloud_bar
    return jsonify(cloud_statistics) # 返回json 格式
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(host='your-ip-address-here',port=5000,debug=True)
