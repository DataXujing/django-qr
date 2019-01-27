from django.shortcuts import render
from .forms import QrForm
import uuid

import qrcode
from PIL import Image
import imageio
from MyQR import myqr
import os
# import Image

def qr_normal(sources,path):
	img =qrcode.make(sources)
	img.save(path)



def qr_logo(sources,logo,path):
	qr = qrcode.QRCode(
	    version=1,  # 设置容错率为最高
	    error_correction=qrcode.ERROR_CORRECT_H, # 用于控制二维码的错误纠正程度
	    box_size=8, # 控制二维码中每个格子的像素数，默认为10
	    border=1, # 二维码四周留白，包含的格子数，默认为4
	    #image_factory=None,  保存在模块根目录的image文件夹下
	    #mask_pattern=None
	)

	qr.add_data(sources) # QRCode.add_data(data)函数添加数据
	qr.make(fit=True)  # QRCode.make(fit=True)函数生成图片

	img = qr.make_image()
	img = img.convert("RGBA") # 二维码设为彩色
	logo = Image.open(logo) # 传gif生成的二维码也是没有动态效果的

	w , h = img.size
	logo_w , logo_h = logo.size
	factor = 4   # 默认logo最大设为图片的四分之一
	s_w = int(w / factor)
	s_h = int(h / factor)
	if logo_w > s_w or logo_h > s_h:
	    logo_w = s_w
	    logo_h = s_h

	logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)
	l_w = int((w - logo_w) / 2)
	l_h = int((h - logo_h) / 2)
	logo = logo.convert("RGBA")
	img.paste(logo, (l_w, l_h), logo)
	# img.show()
	img.save(path, quality=100)

def qr_back(sources,img_path,save_name,save_dirs):
	myqr.run(
	words = sources,    # 二维吗目标信息（URL或文本信息）
	version = 1,            # 设置容错率为最高
	level = 'H',            # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
	picture = img_path,         # 背景图片（可以gif格式）
	colorized = True,       # 是否开启彩色
	contrast = 1.0,         # 图片对比度
	brightness = 1.0,       # 图片亮度
	save_name = save_name,       # 保存文件名，格式可以为： .jpg .png .bmp .gif
	save_dir = save_dirs  # 保存路径(当前目录)
	)



# Create your views here.


def index(request):

	uid = uuid.uuid1()

	# 功能实现
	if request.method == 'POST':
		form_index = QrForm(request.POST,request.FILES)
		if form_index.is_valid():
			qrtype = form_index.cleaned_data['QrType']
			qrsource = form_index.cleaned_data['QrSource']
			qrimg = form_index.cleaned_data['QrImg'].name

			if qrtype == '背景二维码':
				if os.path.splitext(qrimg)[1] != ".gif":
					# print(os.path.splitext(qrimg)[1])
					file_suffix_png = os.path.splitext(qrimg)[0] 
					with open('static/upload/'+str(uid)+qrimg,'wb') as f:
						file = form_index.cleaned_data['QrImg'].read()
						f.write(file)

					im = Image.open('static/upload/'+str(uid)+qrimg)
					rgb_im = im.convert('RGB')
					rgb_im.save('static/upload/'+str(uid)+file_suffix_png+".png")
					if os.path.splitext(qrimg)[1] != ".png":
						os.remove('static/upload/'+str(uid)+qrimg)
					else:
						pass
				else:
					# gif_read = imageio.mimread(qrimg)
					# imageio.mimsave('static/upload/'+str(uid)+qrimg,gif_read)
					with open('static/upload/'+str(uid)+qrimg,'wb') as f:
						file = form_index.cleaned_data['QrImg'].read()
						f.write(file)
			else:
				pass


			# print(qrtype)

			if qrtype == '普通二维码':
				qr_normal(qrsource,'static/upload/'+str(uid)+'.png')
				return render(request,'index.html',{'form':form_index,'state':'post','qr_pic':'upload/'+str(uid)+'.png'})

			elif qrtype == 'Logo二维码':
				with open('static/upload/'+str(uid)+qrimg,'wb') as f:
					file = form_index.cleaned_data['QrImg'].read()
					f.write(file)
				qr_logo(qrsource,'static/upload/'+str(uid)+qrimg,'static/upload/'+str(uid)+'.png')
				return render(request,'index.html',{'form':form_index,'state':'post','qr_pic':'upload/'+str(uid)+'.png'})

			else:
				try:
					file_suffix = os.path.splitext(qrimg)[1] 
					qr_back(qrsource,'static/upload/'+str(uid)+qrimg,str(uid)+file_suffix,'static/upload')
					return render(request,'index.html',{'form':form_index,'state':'post','qr_pic':'upload/'+str(uid)+file_suffix})
				except:
					qr_back(qrsource,'static/upload/'+str(uid)+file_suffix_png+".png",str(uid)+".png",'static/upload')
					return render(request,'index.html',{'form':form_index,'state':'post','qr_pic':'upload/'+str(uid)+".png"})




			# return render(request,'index.html',{'form':form_index,'state':'post','qr_pic':uid})
	else:
		form_index = QrForm()

		return render(request, 'index.html',{'form':form_index,'state':'get','qr_pic':None})


def qr_intro(request):

	return render(request, 'qr_intro.html')

def abouts(request):

	return render(request, 'about.html')
