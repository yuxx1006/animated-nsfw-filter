# NSWF Filter （鉴黄模型）概况

- 鉴黄模型是基于Inception V3的架构，并通过confusion matrix测量可达到93% 识图准确率。
- 模型简介：https://sh-tsang.medium.com/review-inception-v3-1st-runner-up-image-classification-in-ilsvrc-2015-17915421f77c
- 模型可将图片分为以下5个类别：
  - drawings - safe for work drawings (动漫画像)
  - hentai - pornographic drawings (动漫黄图)
  - neutral - safe for work images （安全图）
  - porn - pornographic images （黄图）
  - sexy - sexual images, not pornography (过于暴露图片)
- 模型input为：图片的地址 url， output为以上5中分类的百分比%
- 服务中还添加了smartcrop功能，找出图片压缩后，最想展现的区域


# 技术细节：
- 模型使用Flask框架，并基于Gevent WSGI server实现多进程任务
- 使用pymongo实现数据库的链接
- 使用tensorflow 中的tf.lite.Interpreter来load 训练好的模型 （可见label_image function）
- 使用smartcrop来实现1:1 和16:9 的图片展示区域


## requirements:
python == 3.7
tensorflow >= 2.2.0

## setup
- docker build --tag nsfw:1.0 .
- docker run --name nsfw -p 5000:5000 -d nsfw:1.0

- DEV:
  Feel free to use the base Flask api by running main.py
  Image data stores in mongo (localhost = "127.0.0.1:27017") - can run locally.
- PROD:
  Need to parse env variable (MONGO) to connect mongodb (host for aliyun)
