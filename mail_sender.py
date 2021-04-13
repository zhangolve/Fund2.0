#coding=utf-8
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart


class MailSender(object):

	def __init__(self,my_sender,my_pass,sender_name,receiver_addr,subject,content, attachment):
		self.my_sender=my_sender
		self.my_pass=my_pass#口令，不是密码，通常为16位字符串
		self.sender_name=sender_name
		self.receiver_addr=receiver_addr
		self.subject=subject
		self.content=content
		self.attachment=attachment
		
	def send_it(self):
		msg = MIMEMultipart()
		msg.attach(MIMEText(self.content,'plain','utf-8',))
		msg['From']=formataddr([self.sender_name,self.my_sender])
		msg['to']='管理员'  
		msg['Subject']=self.subject
		if self.attachment: 
			with open(self.attachment, 'rb') as f:
				# set attachment mime and file name, the image type is png
				mime = MIMEBase('image', 'png', filename='img1.png')
				# add required header data:
				mime.add_header('Content-Disposition', 'attachment', filename='img1.png')
				mime.add_header('X-Attachment-Id', '0')
				mime.add_header('Content-ID', '<0>')
				# read attachment file content into the MIMEBase object
				mime.set_payload(f.read())
				# encode with base64
				encoders.encode_base64(mime)
				# add MIMEBase object to MIMEMultipart object
				msg.attach(mime)
		server=smtplib.SMTP_SSL("smtp.qq.com", 465)
		server.login(self.my_sender, self.my_pass)
		server.sendmail(self.my_sender,self.receiver_addr,msg.as_string())
		server.quit()
		print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'邮件发送成功')


		