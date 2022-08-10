from flask import Flask, render_template, redirect, request, make_response, send_from_directory, session
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from werkzeug.security import generate_password_hash,check_password_hash
import api, os, json, api_f, app_ocr
from time import ctime
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='.')
# 配置 SELECT_KEY
app.config['SECRET_KEY'] = '3c2d9d261a464e4e8814c5a39aa72f1c'
app.config['UPLOAD_FOLDER'] = 'upload/'

@app.route('/ocr',methods=['GET', 'POST'])
def ocr():
	if request.method == 'POST':
		file = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
		return 'file upload successfully'
	else:
		return render_template('/static/index.html')

@app.route('/')
def index():
	if 'username' in session:
		#判断已经登录了，直接前往首页
		return redirect('/static/index.html')
	else:
		#没有登录，继续向下判断cookie
		if 'username' in request.cookies:
			# 曾经记住过密码，取出值保存进session
			username = request.cookies.get('username')
			session['username'] = username
			return redirect('/static/index.html')
		else:
			# 之前没有登录过，去往登录页
			return redirect('/static/login.html')

@app.route("/download", methods=['GET'])
def download_file():
	username = session.get('username')
	if not username:
		# 下载登录验证是否具有权限，考虑是否加入更高级的防盗机制
		return redirect('/static/login.html')
	get_data = request.args.to_dict()
	file_path = get_data.get('fileName')
	response = make_response(send_from_directory('data/', file_path, as_attachment=True))
	response.headers["Content-Disposition"] = f"attachment; filename={file_path.encode().decode('latin-1')}"
	return response

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		if 'username' in session:
			# 已经登录了，直接去往首页
			return redirect('/static/index.html')
		else:
			# 没有登录，继续向下判断cookie
			if 'username' in request.cookies:
				# 曾经记住过密码，取值保存进session
				username = request.cookies.get('username')
				session['username'] = username
				return redirect('/static/index.html')
			else:
				# 之前没有登录过，去往登录页
				return redirect('/static/login.html')
	else:
		# 先处理登录，登录成功则保存进session，否则返回登录页
		username = request.values.get('username')
		password = request.values.get('password')
		try:
			with open('userdata/data1.json', 'r', encoding='utf-8') as fp:
				json_data = json.load(fp)
				if check_password_hash(json_data[f"{username}"]["password"], password) == True:
					# 声明重定向到首页的对象
					resp = redirect('/static/index.html')
					# 登录成功：先将数据保存进session
					session['username'] = username
					if 'isSaved' in request.values:
						# 具体实现方法是在前端实现
						# 需要记住密码，将信息保存进cookie
						resp.set_cookie('username', username, 60 * 60 * 24 * 30)
					return resp
				else:
					return redirect('/static/login.html')
		except:
			return redirect('/static/login.html')

@app.route('/enroll', methods=['POST'])
def enroll():
	username = request.values.get('username')
	password = request.values.get('password')
	# hash加盐，不可逆向
	password = generate_password_hash(password)
	with open("userdata/data1.json", 'r+') as file:
		json_data = json.load(file)
		if username in json_data.keys():
			return """
			<p>账号已存在或者正在审核中</p>
			<a href="/static/login.html">返回</a>"""
		elif f"{username}_1" in json_data.keys():
			return """
			<p>账号已存在或者正在审核中</p>
			<a href="/static/login.html">返回</a>"""
		else:
			krro = {"password" :f"{password}"}
			json_data[f"{username}_1"] = krro
			print(json_data)
			file.seek(0)
			file.write(json.dumps(json_data, ensure_ascii=False, indent=2))
			file.truncate()
			return """
			<p>已经提交管理员审核</p>
			<a href="/static/login.html">返回</a>"""

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	resp = redirect('/static/login.html')
	resp.delete_cookie('username')
	session.pop('username', None)
	return resp

@app.route('/api/get_js', methods=['POST'])
def get_js():
	# 怎么这玩意靠bug运行
	if request.method == 'get':
		return {'return': 0}
	else:
		name = request.values.get("name")
		code = eval(request.values.get("code"))
		if code == 1:
			api_res = api.get_in_js(name)
		elif code == 2:
			api_res = api_f.get_in_book(name)
		return json.dumps(api_res, ensure_ascii=False, indent=2)

@app.route('/api/get_text', methods=['GET'])
def get_text():
	username = session.get('username')
	if not username:
		return redirect('/static/login.html')
	name = request.args.get("name")
	code = eval(request.args.get("code"))
	if os.path.exists(f"data/{name}.txt") != True:
		if request.method == 'get': # match后面跟要匹配的对象
			return {'return': 0}
		else: # _捕获其他未涵盖情况
			if code == 1:
				api.get_txt(name)
			elif code == 2:
				buid = request.args.get("buid")
				api_f.get_in_text(buid, name)
			now = ctime()
			open('static/download.log', 'a+', encoding='utf-8').write(f"[{now}] - SUC {name} download\n")
			return "下载完成"
	else:
		return "任务已存在或者下载完毕"

@app.errorhandler(500)
def internal_error(error):
	return "500 error"

@app.errorhandler(404)
def not_found(error):
    return"404 error",404

if __name__ == '__main__':
	CORS(app, supports_credentials=True)
	# app.run(debug=debug, processes=20)
	app.run(debug=True, threaded=True)
