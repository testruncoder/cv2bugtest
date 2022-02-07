import streamlit as st  # Ver 1.3.0
import numpy as np
import cv2

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    RTCConfiguration,
)
import cvzone
import av



# Created on 02/05/2022 by testruncoder
# Test code to fix "No Module named 'cv2'" on strealit cloud

RTC_CONFIGURATION=RTCConfiguration(
    {'iceServers':[{'urls':['stun:stun.l.google.com:19302']}]}
)

# Ver0_5 (01/01/2022)
def streamlit_webrtc_stacked_videoFrames():
    class VideoStackedVideoFramesProcessor(VideoProcessorBase):
        # def __init__(self):
        #     self.detector=PoseDetector()

        def stacked_video_frames(self,img):
            imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            imgList=[img,img,imgGray,img,imgGray,img,imgGray,img,img]
            stackedImg=cvzone.stackImages(imgList,3,0.4)
            return stackedImg
        # ------------------------  END OF stacked_video_frames()  --------------------------------------------

        # def transform(self,frame):
        def recv(self,frame):
            img=frame.to_ndarray(format='bgr24')
            img=self.stacked_video_frames(img)
            return av.VideoFrame.from_ndarray(img,format='bgr24')  # Must use this line with 'VideoProcessorBase' and recv() - Ver0_4_1 (01/01/2022)

    # # Call streamer
    ctx=webrtc_streamer(key='stackedvideoframes',
                    # mode=WebRtcMode.SENDRECV,  # Not necessarily needed (?) - Ver0_4_1 (01/01/2022)
                                            # client_settings=WEBRTC_CLINET_SETTINGS,  # Deprecated - Disabled in Ver0_4 (2021/12/31)
                    rtc_configuration=RTC_CONFIGURATION,
                    media_stream_constraints={'video':True,'audio':False},

                    video_processor_factory=VideoStackedVideoFramesProcessor,  # Ver0_4_1 (01/01/2022)
                    # async_processing=True,  # What is this? - Ver0_4_1 (01/01/2022)
        )
# --------------------------------  END OF streamlit_webrtc_stacked_videoFrames()  -----------------------------------------------------


def main():
    st.subheader('Stacked Frames')
    streamlit_webrtc_stacked_videoFrames()

if __name__=='__main__':
    main()

