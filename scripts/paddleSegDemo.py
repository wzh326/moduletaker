#!/usr/bin/env python3
# coding:utf-8

import cv2
import numpy as np
import time
from Lib.PaddleSeg_Inference_Lib import Paddle_Seg
import rospy
from std_msgs.msg import Header
from cv_bridge import CvBridge , CvBridgeError
from Lib.PaddleSeg_Inference_Lib import Paddle_Seg
from sensor_msgs.msg import Image
# --------------------------配置区域--------------------------
infer_img_size = 300        # 自定义模型预测的输入图像尺寸
use_gpu = True              # 是否使用GPU
gpu_memory = 500            # GPU的显存
use_tensorrt = False         # 是否使用TensorRT
precision_mode = "fp16"     # TensorRT精度模式
# 模型文件路径
model_folder_dir = "/home/itcast/py3_test_ws/src/py3_demo/scripts/model/hardnet_test"
# 类别信息
label_list = ["sidewalk","other","blind_road"]
# -----------------------------------------------------------
        
if __name__ == '__main__':
    paddle_seg = Paddle_Seg(model_folder_dir=model_folder_dir, infer_img_size=infer_img_size, 
                            use_gpu=use_gpu, gpu_memory=gpu_memory, use_tensorrt=use_tensorrt, 
                            precision_mode=precision_mode,label_list=label_list)
    

    rospy.init_node('camera_node', anonymous=True) #定义节点
    image_pub=rospy.Publisher('/image_view/image_raw', Image, queue_size = 1) #定义话题
    while not rospy.is_shutdown():
        start = time.time()
        image = cv2.imread("/home/itcast/py3_test_ws/src/py3_demo/scripts/0.jpg",1)
        paddle_seg.init(image.shape[1],image.shape[0])
        image = cv2.resize(image,(640,480))
        # 预测
        result = paddle_seg.infer(image)
        # 绘制结果
        frame, _ = paddle_seg.post_process(image, result)
        image=(frame*255).astype(np.uint8)
        image = cv2.flip(image,1)   #水平镜像操作   
        ros_frame = Image()
        header = Header(stamp = rospy.Time.now())
        header.frame_id = "Camera"
        ros_frame.header=header
        ros_frame.width = 1920
        ros_frame.height = 1080
        ros_frame.encoding = "bgr8"
        ros_frame.data = np.array(image).tobytes()#图片格式转换
        image_pub.publish(ros_frame) #发布消息
        end = time.time()  
        print("cost time:", end-start ) # 看一下每一帧的执行时间，从而确定合适的rate
        rate = rospy.Rate(25) # 10hz 
        cv2.imshow("image", image)

        cv2.waitKey(1)



