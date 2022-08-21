import cv2
import time
import datetime

yol_liste = [600, 1000, 1400, 1800, 2200, 2600, 3000, 3400, 3800, 4200, 4600, 
             5000, 5400, 5800, 6200, 6600, 7000, 7400, 7800, 7805, 7810, 7815, 
             7820, 7825, 7830, 7835, 7840, 7845, 7850, 7855, 7860, 7865, 7870, 
             7875, 7880, 7885, 7890, 7895, 7900, 7905, 7910, 7915, 7920, 7925, 
             7930, 7935, 7940, 7945, 7950, 7955, 7960, 7965, 7970, 7975, 7980, 
             7985, 7990, 7995, 8200, 8600, 9000, 9400, 9800, 10200, 10600, 
             11000, 11400, 11800, 12200, 12600, 13000, 13005, 13010, 13015, 
             13020, 13025, 13030, 13035, 13040, 13045, 13050, 13055, 13060, 
             13065, 13070, 13075, 13080, 13085, 13090, 13095, 13400, 13800, 
             14200, 14600, 15000, 15400, 15800, 16200, 16600, 17000, 17400]

cap = cv2.VideoCapture(0)
yellowReflectorCounter=0
redReflectorCounter=0
reflectorCount=0

firstTime = datetime.datetime.now()
startTime = datetime.datetime.now()
nowTime = datetime.datetime.now()

def cycle():
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:   
        
        global redReflectorCounter 
        global reflectorCount
        global yellowReflectorCounter
        
        global firstTime
        global startTime
        global nowTime
        
        delayTime= delay(reflectorCount)
        print("delay time",delayTime)
        time.sleep(delayTime)
        
        if(reflectorCount==0):
            firstTime = datetime.datetime.now()
            
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        cx = int(width / 2)
        cy = int(height / 2)

        # Pick pixel value
        pixel_center = hsv_frame[cy, cx]
        hue_value = pixel_center[0]

        color = "Undefined"
        if 1< hue_value < 6:
            color = "RED"        
            redReflectorCounter=redReflectorCounter+1         
            reflectorCount=reflectorCount+1
            startTime=nowTime
            nowTime = datetime.datetime.now()


        elif 10 <= hue_value < 33:
            color = "SARI"
            yellowReflectorCounter=yellowReflectorCounter + 1
            reflectorCount=reflectorCount+1
            startTime=nowTime
            nowTime = datetime.datetime.now()
          

        elif 131 <= hue_value < 180:
            color = "RED"
            redReflectorCounter=redReflectorCounter+1
            reflectorCount=reflectorCount+1
            startTime=nowTime
            nowTime = datetime.datetime.now()
            
        else:
            color = "Siyah" 
            isReflekUp=False

                       
        pixel_center_bgr = frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1) #yazının arkasına beyaz font
        cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5) #aynı renk olsun diye bgrla yazı yazdırma
        cv2.putText(frame, str(hue_value), (cx - 200, 200), 0, 3, (255, 255,255), 5)

        cv2.putText(frame, "KSayac:"+str(redReflectorCounter), (cx - 200, 300), 0, 3, (255, 255, 255), 5)
        cv2.putText(frame, "SSayac:"+str(yellowReflectorCounter), (cx - 200, 400), 0, 3, (255, 255, 255), 5)

        cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3) #orta noktaya yuvarlak koydum belli olsun diye
        

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    return reflectorCount
    cap.release()
    cv2.destroyAllWindows()
    
        
def delay(reflectorCount):
    if reflectorCount==0:
        return 1 ##hata devam ederse ilk burayı 

    global yol_liste
    global firstTime
    global startTime
    global nowTime
    
    check()
    
    print("")
    print("")
    accelerationSeconds=(nowTime - startTime).seconds
    onsetSeconds=(nowTime - firstTime).seconds
    print("Starting code time: ",firstTime)
    print("Start Time: ", startTime)
    print("Now Time: ", nowTime)
    print("Between reflektor Seconds:" , onsetSeconds)
    
    if(reflectorCount==1):
        mesafe=(yol_liste[reflectorCount-1])/100
    elif(reflectorCount>1):
        mesafe=((yol_liste[reflectorCount-1])/100)-((yol_liste[reflectorCount-2])/100)
    #print("Mesafe: ",mesafe)
    print("Location(m): ",yol_liste[reflectorCount-1]/100)
    
    acceleration=mesafe/accelerationSeconds
    hız=((yol_liste[reflectorCount-1])/100)/onsetSeconds
    print("İvme: ", acceleration)
    print("Speed: ", hız)
    print("Reflektör sayısı: ",reflectorCount)
    ##burda sayılar matematiksel olarak hesaplanıp değiştirilecek
    if(hız<10):
        return 1
    elif (hız<20):
        return 1
    elif (hız<30):
        return 1
    elif (hız<40):
        return 1
    
def check():
    global reflectorCount
    global yellowReflectorCounter
    
    if (yellowReflectorCounter==1):
        reflectorCount=20
        
    if yellowReflectorCounter==40:
        reflectorCount=60
    
def home():
    global startTime
    startTime = datetime.datetime.now()
    reflectorCount = cycle()
    
#created by Necmettin Alver   
home()
