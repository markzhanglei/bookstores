from django.shortcuts import render, redirect
import re
from django.http import JsonResponse
# Create your views here.
from users.models import Passport, Address
from django.core.urlresolvers import reverse
from utils.decorators import login_required
from order.models import OrderInfo,OrderGoods


def register(request):
	return render(request, 'users/register.html')


def register_handle(request):
	'''进行用户注册处理'''
	# 接收数据
	username = request.POST.get('user_name')
	password = request.POST.get('pwd')
	email = request.POST.get('email')

	# 进行数据校验
	if not all([username, password, email]):
		# 有数据为空
		return render(request, 'users/register.html', {'errmsg': '参数不能为空'})

	# 判断邮箱是否合法
	if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
		return render(request, 'users/register.html', {'errmsg': '邮箱不合法'})

	# 进行业务处理:注册，向账户系统中添加账户
	passport = Passport.objects.add_one_passport(username=username, password=password, email=email)
	# 注册完，还是返回注册页。
	# 	return redirect(reverse('users:register'))
	return redirect(reverse('books:index'))


def login(request):
	return render(request, 'users/login.html')


def login_check(request):
	'''进行用户登录校验'''
	# 1.获取数据
	username = request.POST.get('username')
	password = request.POST.get('password')
	remember = request.POST.get('remember')
	# 2.数据校验
	if not all([username, password, remember]):
		# 有数据为空
		return JsonResponse({'res': 2})
	# 3.进行处理:根据用户名和密码查找账户信息
	passport = Passport.objects.get_one_passport(username=username, password=password)

	if passport:
		# 用户名密码正确
		# 获取session中的url_path
		# if request.session.has_key('url_path'):
		#     next_url = request.session.get('url_path')
		# else:
		#     next_url = reverse('books:index')
		next_url = request.session.get('url_path', reverse('books:index'))
		jres = JsonResponse({'res': 1, 'next_url': next_url})

		# 判断是否需要记住用户名
		if remember == 'true':
			# 记住用户名
			jres.set_cookie('username', username, max_age=7 * 24 * 3600)
		else:
			# 不要记住用户名
			jres.delete_cookie('username')
		# 记住用户的登录状态
		request.session['islogin'] = True
		request.session['username'] = username
		request.session['passport_id'] = passport.id
		return jres
	else:
		# 用户名或密码错误
		return JsonResponse({'res': 0})


def logout(request):
	'''用户退出登录'''
	# 清空用户的session信息
	request.session.flush()
	# 跳转到书籍首页
	return redirect(reverse('books:index'))


# 使用装饰器修饰用户中心.
@login_required
def user(request):
	'''用户中心-信息页'''
	passport_id = request.session.get('passport_id')
	# 获取用户的基本信息
	addr = Address.objects.get_default_address(passport_id=passport_id)

	books_li = []

	context = {
		'addr': addr,
		'page': 'user',
		'books_li': books_li
	}

	return render(request, 'users/user_center_info.html', context)


@login_required
def address(request):
	'''用户中心-地址页'''
	# 获取登录用户的id
	passport_id = request.session.get('passport_id')

	if request.method == 'GET':
		#显示地址页面
#查询用户的默认地址
		addr = Address.objects.get_default_address(passport_id=passport_id)
		return render(request,'users/user_center_site.html',{'addr':addr,'page':'address'})

	else:
		#添加收货地址
#1接受数据
		recipient_name = request.POST.get('username')
		recipient_addr = request.POST.get('addr')
		zip_code = request.POST.get('zip_code')
		recipient_phone = request.POST.get('phone')

		#进行校验
		if not all([recipient_name,recipient_addr,zip_code,recipient_phone]):
			return render(request,'users/user_center_site.html',{'errmsg':'参数不必为空!'})

		#3添加收获地址
		Address.objects.add_one_address(
			passport_id=recipient_name,
			recipient_addr=recipient_addr,
			zip_code=zip_code,
			recipient_phone = recipient_phone
		)

		#返回应答
		return redirect(reverse('users:address'))


@login_required
def order(request):
	#用户中心-订单页
#查询用户的订单信息
	passport_id = request.session.get('passport_id')

	#获取订单信息
	order_li = OrderInfo.objects.filter(passport_id=passport_id)

	#便利获取订单的商品信息
	for order in order_li:
# 根据订单id查询订单商品信息
		order_id = order.order_id
		order_books_li = OrderGoods.objects.filter(order_id=order_id)
# 计算商品的小计
# order_books ->OrderGoods实例对象
		for order_books in order_books_li:
			count = order_books.count
			price = order_books.price
			amount = count * price
			order_books.amount = amount
# 给order对象动态增加一个属性order_books_li,保存订单中商品的信息
		order.order_books_li = order_books_li

	context = {
		'order_li':order_li,
		'page':'order'

	}

	return render(request,'users/user_center_order.html',context)