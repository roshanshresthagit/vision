import sys
import threading 
import cv2
import numpy as np
from ctypes import *

sys.path.append("./MvImport")
from .MvImport.MvCameraControl_class import *

class CAMERA:
    g_bExit = False
    current_image = None
    def __init__(self):
        # initialize SDK
        MvCamera.MV_CC_Initialize()
        self.cam = MvCamera()
        
    def image_captured_callback(self):
        """captured image callback
        
        """
        
    def enum_devices(self):
        self.g_bExit = False
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = (MV_GIGE_DEVICE | MV_USB_DEVICE | MV_GENTL_CAMERALINK_DEVICE
                    | MV_GENTL_CXP_DEVICE | MV_GENTL_XOF_DEVICE)
        
        # ch:枚举设备 | en:Enum device
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, self.deviceList)
        if ret != 0:
            print ("enum devices fail! ret[0x%x]" % ret)
            sys.exit()

        if self.deviceList.nDeviceNum == 0:
            print ("find no device!")
            sys.exit()

        print ("Find %d devices!" % self.deviceList.nDeviceNum)

        for i in range(0, self.deviceList.nDeviceNum):
            mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE or mvcc_dev_info.nTLayerType == MV_GENTL_GIGE_DEVICE:
                print ("\ngige device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    if per == 0:
                        break
                    strModeName = strModeName + chr(per)
                print ("device model name: %s" % strModeName)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                print ("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                print ("\nu3v device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                    if per == 0:
                        break
                    strModeName = strModeName + chr(per)
                print ("device model name: %s" % strModeName)

                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                print ("user serial number: %s" % strSerialNumber)
                
    def open_device(self, nConnectionNum):
        # ch:选择设备并创建句柄 | en:Select device and create handle
        stdeviceList = cast(self.deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents

        ret = self.cam.MV_CC_CreateHandle(stdeviceList)
        if ret != 0:
            print ("create handle fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:打开设备 | en:Open device
        ret = self.cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print ("open device fail! ret[0x%x]" % ret)
            sys.exit()
        
        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if stdeviceList.nTLayerType == MV_GIGE_DEVICE or stdeviceList.nTLayerType == MV_GENTL_GIGE_DEVICE:
            nPacketSize = self.cam.MV_CC_GetOptimalPacketSize()
            if int(nPacketSize) > 0:
                ret = self.cam.MV_CC_SetIntValue("GevSCPSPacketSize",nPacketSize)
                if ret != 0:
                    print ("Warning: Set Packet Size fail! ret[0x%x]" % ret)
            else:
                print ("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

        stBool = c_bool(False)
        ret =self.cam.MV_CC_GetBoolValue("AcquisitionFrameRateEnable", stBool)
        if ret != 0:
            print ("get AcquisitionFrameRateEnable fail! ret[0x%x]" % ret)

        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = self.cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print ("set trigger mode fail! ret[0x%x]" % ret)
            sys.exit()
    
    def start_grabbing(self):
        # ch:开始取流 | en:Start grab image
        ret = self.cam.MV_CC_StartGrabbing()
        if ret != 0:
            print ("start grabbing fail! ret[0x%x]" % ret)
            # sys.exit()

        try:
            self.hThreadHandle = threading.Thread(target=self.work_thread, args=()) # pass displayWidget id as argument to show the image
            self.hThreadHandle.start()
        except:
            print ("error: unable to start thread")
            
        # print ("press a key to stop grabbing.")
        # msvcrt.getch()

        # self.g_bExit = True
        # self.hThreadHandle.join()
        # self.close_device()

    def stop_grabbing(self):
        # ch:停止取流 | en:Stop grab image
        ret = self.cam.MV_CC_StopGrabbing()
        if ret != 0:
            print ("stop grabbing fail! ret[0x%x]" % ret)
            sys.exit()
            
    def close_device(self):
        # ch:关闭设备 | Close device
        self.g_bExit = True
        self.hThreadHandle.join()
        self.stop_grabbing()
        ret = self.cam.MV_CC_CloseDevice()
        if ret != 0:
            print ("close deivce fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:销毁句柄 | Destroy handle
        ret = self.cam.MV_CC_DestroyHandle()
        if ret != 0:
            print ("destroy handle fail! ret[0x%x]" % ret)
            sys.exit()
            
    # 彩色图像转为python数组
    def Color_numpy(self, data, nWidth, nHeight):
        data_ = np.frombuffer(data, count=int(nWidth * nHeight * 3), dtype=np.uint8, offset=0)
        data_r = data_[0:nWidth * nHeight * 3:3]
        data_g = data_[1:nWidth * nHeight * 3:3]
        data_b = data_[2:nWidth * nHeight * 3:3]

        data_r_arr = data_r.reshape(nHeight, nWidth)
        data_g_arr = data_g.reshape(nHeight, nWidth)
        data_b_arr = data_b.reshape(nHeight, nWidth)
        numArray = np.zeros([nHeight, nWidth, 3], "uint8")

        numArray[:, :, 0] = data_r_arr
        numArray[:, :, 1] = data_g_arr
        numArray[:, :, 2] = data_b_arr
        return numArray

    # 为线程定义一个函数
    def work_thread(self):
        stOutFrame = MV_FRAME_OUT()  
        memset(byref(stOutFrame), 0, sizeof(stOutFrame))
        while True:
            ret = self.cam.MV_CC_GetImageBuffer(stOutFrame, 1000)
            if None != stOutFrame.pBufAddr and 0 == ret:
                # print ("get one frame: Width[%d], Height[%d], nFrameNum[%d]"  % (stOutFrame.stFrameInfo.nWidth, stOutFrame.stFrameInfo.nHeight, stOutFrame.stFrameInfo.nFrameNum))
                nRet = self.cam.MV_CC_FreeImageBuffer(stOutFrame)
            else:
                print ("no data[0x%x]" % ret)
            self.st_frame_info = stOutFrame.stFrameInfo
            
            nRGBSize = stOutFrame.stFrameInfo.nWidth * stOutFrame.stFrameInfo.nHeight * 3
            stConvertParam = MV_CC_PIXEL_CONVERT_PARAM_EX()
            memset(byref(stConvertParam), 0, sizeof(stConvertParam))
            stConvertParam.nWidth = stOutFrame.stFrameInfo.nWidth
            stConvertParam.nHeight = stOutFrame.stFrameInfo.nHeight
            stConvertParam.pSrcData = stOutFrame.pBufAddr
            stConvertParam.nSrcDataLen = stOutFrame.stFrameInfo.nFrameLen
            stConvertParam.enSrcPixelType = stOutFrame.stFrameInfo.enPixelType  
            stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
            stConvertParam.pDstBuffer = (c_ubyte * nRGBSize)()
            stConvertParam.nDstBufferSize = nRGBSize
            ret = self.cam.MV_CC_ConvertPixelTypeEx(stConvertParam)
            if ret != 0:
                print ("convert pixel fail! ret[0x%x]" % ret)
                return
            
            img_buff = (c_ubyte * stConvertParam.nDstLen)()
            cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, stConvertParam.nDstLen)
            numArray = self.Color_numpy(img_buff, stOutFrame.stFrameInfo.nWidth, stOutFrame.stFrameInfo.nHeight)
            self.current_image = numArray.copy()
            
            # try:
            #     numArray = self.image_captured_callback(numArray)
            # except Exception as e:
            #         print('[-] Process Error')
            #         print(traceback.format_exc())
            
            # # preparing for the conversion
            # nHeight, nWidth, _channels = numArray.shape
            # numArray_pointer = numArray.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
            # self.st_frame_info.nWidth,self.st_frame_info.nHeight = nWidth, nHeight 
            # self.st_frame_info.nFrameLen = nWidth * nHeight
            
            
            # stDisplayParam = MV_DISPLAY_FRAME_INFO()
            # memset(byref(stDisplayParam), 0, sizeof(stDisplayParam))
            # stDisplayParam.hWnd = str('http://localhost:5173/')
            # stDisplayParam.nWidth = self.st_frame_info.nWidth
            # stDisplayParam.nHeight = self.st_frame_info.nHeight
            # stDisplayParam.enPixelType = PixelType_Gvsp_RGB8_Packed #  self.st_frame_info.enPixelType
            # stDisplayParam.pData = numArray_pointer # .tobytes(order='C') # self.buf_save_image # 
            # stDisplayParam.nDataLen = self.st_frame_info.nFrameLen
            # self.cam.MV_CC_DisplayOneFrame(stDisplayParam)
            
            # Display the image using OpenCV
            # cv2.imshow("Captured Image", numArray)
        
            # Wait for a key press to proceed (you can use a short wait for real-time processing)
            # if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the display window
            #     cv2.destroyAllWindows()
            if self.g_bExit == True:
            #     cv2.destroyAllWindows()
                break
            
    def get_capture_image(self):
        if not self.g_bExit:
            return self.current_image if self.current_image is not None else None
    
    def get_current_image(self):
        if not self.g_bExit:
            i = cv2.imread(r"C:\Users\shres\Downloads\files\images\fick.jpg")
            # i = cv2.imread(r"C:\Users\shres\Downloads\INDERAL-TABLETS-10mg-PACK-OF-50-TABLETS.webp")
            # i = cv2.imread(r"C:\Users\shres\Downloads\jeremy-bishop-b_Iz9tkrw6A-unsplash.jpg")
            # i = cv2.imread(r"C:\Users\shres\Downloads\cig_image\roshan\NG_1739163613.420269.jpg")
        
            self.current_image = np.array(i)
            return self.current_image if self.current_image is not None else None
    
 
        
                
        
            
# if __name__ == '__main__':
#     camera = CAMERA()