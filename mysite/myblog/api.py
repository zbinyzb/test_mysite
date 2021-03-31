#导入装饰器
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password,make_password

from myblog.models import Classes,Userinfo,SiteInfo
from myblog.tojson import Classes_data,Userinfo_data
import json

@api_view(['GET','POST'])
def api_test(request):

    #1.使用rest_framework序列化
    # classes = Classes.objects.all()
    # classes_data = Classes_data(classes,many=True)
    # userlist = Userinfo.objects.all()
    # userlist_data = Userinfo_data(userlist,many=True)

    # data = {
    #     "classes":classes_data.data,
    #     "userlist":userlist_data.data
    # }
    # return Response({'data':data})


    #2.使用python语法自定义
    classes = Classes.objects.all()
    
    data = {
        'classes':[]
    }
    for c in classes:
        #每个元素也是字典
        data_item = {
            'id':c.id,
            'text':c.text,
            'userlist':[]
        }
        #通过related_name实现一个classes获取与其相关的外键信息
        userlist = c.userinfo_classes.all()
        for user in userlist:
            #用户的信息
            user_data = {
                'id':user.id,
                'nickName':user.nickName,
                'headImg':str(user.headImg)
            }
            #通过append()把数据推入列表
            data_item['userlist'].append(user_data)
        data['classes'].append(data_item)
    #UnicodeDecodeError：数据格式不一样    
    #return Response({'data':data})
    #return Response(data)
    # data = json.dumps(data)
    return Response(data)

#添加rest_framework中的api视图装饰器
@api_view(['GET'])
def getMenuList(request):
    allClasses = Classes.objects.all()
    siteinfo = SiteInfo.objects.get(id=1)
    siteinfo_data = {
        'sitename':siteinfo.title,
        'logo':'http://127.0.0.1:9000/upload/'+str(siteinfo.logo)
    }
    #整理数据为json
    menu_data = []
    for c in allClasses:
        #设计单条数据的结构、
        data_item = {
            'id':c.id,
            'text':c.text
        }
        menu_data.append(data_item)
    data = {
        'menu_data':menu_data,
        'siteinfo':siteinfo_data
    }
    return Response(data)

@api_view(['GET','DELETE'])
def getUserList(request):
    if request.method == 'DELETE':
        #获取id
        user_id = request.POST['id']
        print(user_id)
        #删除id
        deleteUser = Userinfo.objects.get(id=user_id)
        deleteUser.delete()
        return Response('ok')
    menuId = request.GET['id']
    print(menuId)
    #筛选课程
    menu = Classes.objects.get(id=menuId)
    print(menu)
    #筛选用户
    userlist = Userinfo.objects.filter(belong=menu)
    print(userlist)

    #开始整理数据列表
    data=[]
    for user in userlist:
        data_item= {
            'id':user.id,
            #转下格式
            'headImg':str(user.headImg),
            'nickName':user.nickName
        }
        data.append(data_item)
    return Response(data)

@api_view(['POST'])
def toLogin(request):
    print(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    print(username,password)
    #查询用户数据库
    user = User.objects.filter(username=username)
    if len(user)>0:
        #authenticate验证模块
        # auth_user = authenticate(username=username,password=password)
        # print(auth_user)
        # if auth_user:
        #     return Response('登录成功')
        # else:
        #     return Response('账号密码错误')
        
        #加密验证
        user_pwd = user[0].password     #user_pwd表示已存在数据库中的表中的索引数据
        auth_pwd = check_password(password,user_pwd)
        print(auth_pwd)
        if auth_pwd:
            token = Token.objects.update_or_create(user=user[0])
            token = Token.objects.get(user=user[0])
            print(token.key)

            #获取用户信息
            userinfo = Userinfo.objects.get(belong_user=user[0])
            data = {
                'token':token.key,
                'userinfo':{
                    'id':userinfo.id,
                    'nickName':userinfo.nickName,
                    #图片信息字符串化
                    'headImg':str(userinfo.headImg)
                }
            }
            return Response(data)
        else:
            return Response('pwderror')
    else:
        return Response('none')
    return Response('ok')

@api_view(['GET','POST'])
def toRegister(request):
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    print(username,password,password2)
    #用户是否存在
    user = User.objects.filter(username=username)
    if user:
        return Response('same')
    else:
        #make_password(密码,另外一个需要加密的)
        newPwd = make_password(password,username)
        print(newPwd)
        newUser = User(username=username,password=newPwd)
        newUser.save()
    return Response('ok')

@api_view(['POST','PUT'])
def uploadLogo(request):
    #获取的本质上仍是POST过来的东西，只是方法使用PUT来区分请求
    if request.method == 'PUT':
        sitename = request.POST['sitename']
        print(sitename)
        old_info = SiteInfo.objects.get(id=1)
        old_info.title = sitename
        new_info = SiteInfo.objects.get(id=2)
        old_info.logo = new_info.logo
        old_info.save()
        return Response('ok')
    img = request.FILES['logo']
    print(img)
    test_siteLogo = SiteInfo.objects.get(id=2)
    test_siteLogo.logo = img
    test_siteLogo.save()
    data = {
        'img':str(test_siteLogo.logo)
    }
    return Response(data)