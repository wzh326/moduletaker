# paddle-inference-deploy-Lib
deploy Lib target for paddleDetetction and paddleSeg by paddle inference


## Install

- `PaddlePaddle`(>=2.2.0)

Install the PaddlePaddle 2.1 version, please refer to [Quick Installation](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/linux-pip.html) for the specific installation method. 

- `Paddleseg`

```
pip install paddleseg
```


'''
方案一
1.先按照 https://blog.csdn.net/qq_45779334/article/details/119641789?utm_source=app&app_version=5.0.1&code=app_1562916241&uLinkId=usr1mkqgl919blen
高总的这个博客安装cv_bridge以及python3环境，建议anaconda方法，可以避免一些不必要的问题
2.创建功能包运行demo
可能出现找不到yaml的问题。
看文件夹中的图片，并且将model文件夹下的yaml等文件copy移到lib下
注：由于测试的时候没有相机，用图片测试的，请将       self.paddle_seg.init(1920,1080)  改为    paddle_seg.init(camera_width,camera_height)。并且修改读取图片部分。



方案二
pip3 install rospkg
pip3 install catkin-tools

在代码中加入inport rospy
直接运行python3 XXX.py
注：在发布topic的时候出现了问题，可能是tostring（）的问题，也可能是cv_bridge不兼容的问题。不知道其他人会不会有。