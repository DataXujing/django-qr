from django import forms


class QrForm(forms.Form):
	# 后边这个是列表显示
	QrType = forms.ChoiceField(label='选择类型',initial='普通二维码',choices=[('普通二维码','普通二维码'),('Logo二维码','Logo二维码'),('背景二维码','背景二维码')])
	QrSource = forms.CharField(label='定义资源', max_length=100)
	QrImg = forms.FileField(label='上传图片',allow_empty_file=True)
 
