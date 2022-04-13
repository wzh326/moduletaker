import cv2
import numpy as np
import time
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
model_folder_dir = "model/hardnet_test"
# 类别信息
label_list = ["sidewalk"]
# -----------------------------------------------------------
class Paddle_me:
    def __init__(self, model_folder_dir, infer_img_size, use_gpu, 
                 gpu_memory, use_tensorrt, precision_mode, label_list):

        self.paddle_seg = Paddle_Seg(model_folder_dir=model_folder_dir, infer_img_size=infer_img_size, 
                            use_gpu=use_gpu, gpu_memory=gpu_memory, use_tensorrt=use_tensorrt, 
                            precision_mode=precision_mode)
        self.cap = cv2.VideoCapture(0) # USB Camera
        self.camera_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.camera_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)    
        self.paddle_seg.init(camera_width,camera_height)
        self.image_pub=rospy.Publisher('/image_view/image_raw',Image,queue_size = 1)

    def imgshow(self):
        start = time.time()
        bridge = CvBridge()
        while True:
            start = time.time()
            _, image = cap.read()
        # 预测
            result = self.paddle_seg.infer(image)
        # 绘制结果
            image, _ = self.paddle_seg.post_process(image, result)
            image= cv2.resize(image,(640,480))
            #cv2.imshow("image", image)
            ros_frame = Image()
            header = Header(stamp = rospy.Time.now())
            header.frame_id = "Camera"
            ros_frame.header=header
            ros_frame.width = 640
            ros_frame.height = 480
            ros_frame.encoding = "bgr8"
            ros_frame.step = 1920
            ros_frame.data = np.array(image).tostring() #图片格式转换
            self.image_pub.publish(ros_frame) #发布消息
            rate = rospy.Rate(10)
        
        cap.release()
def main():
    # 初始化
    

    rospy.init_node('camera_node',anonymous=True)
    come=Paddle_me(model_folder_dir=model_folder_dir, use_model_img_size=use_model_img_size, 
                                    infer_img_size=infer_img_size, use_gpu=use_gpu, filter_mode=filter_mode, 
                                    gpu_memory=gpu_memory, use_tensorrt=use_tensorrt, precision=precision_mode)
    come.imgshow()

if __name__ == '__main__':
    main()


