# encoding:utf-8

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
access_key = 'JPoz3ujw_RDlfdndPK1QtftzngAkeH6eY50KLP5M'
secret_key = 'impOZtOOFArrCo4JVDvlJm50cx5KKULozvDTbjod'
# 初始化Auth状态
q = Auth(access_key, secret_key)
# 你要保存的空间bucket， 保存的文件名imagename
bucket_name = 'nineoffs-img'
key = '6.jpg'
# 指定缩略使用的队列名称，不设置代表不使用私有队列，使用公有队列。
pipeline = ''
# 设置图片缩略参数
fops = 'imageView2/1/w/200/h/200'
# 通过添加'|saveas'参数，指定处理后的文件保存的bucket和key，不指定默认保存在当前空间，bucket_saved为目标bucket，key_saved为目标key
saveas_key = urlsafe_base64_encode('bucket_saved:key_saved')
fops = fops+'|saveas/'+saveas_key
# 在上传策略中指定fobs和pipeline
policy={
  'persistentOps':fops,
  'persistentPipeline':pipeline
 }
token = q.upload_token(bucket_name, key, 3600, policy)
# 图片所在的本地路径
localfile = 'D:\\FlaskForDrops\\img\\6.jpg'
ret, info = put_file(token, key, localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)