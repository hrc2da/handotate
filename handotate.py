import cv2
import os
import glob
import argparse
from copy import copy
import time
import csv
import yaml


def process_label(key_pressed,labels):
    ord_keys = [(ord(k),k) for k in labels.keys()]
    for k in ord_keys:
        if key_pressed == k[0]:
            return labels[k[1]]
    return None


if __name__=='__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", nargs='?', default='empty')
    parser.add_argument("--out", nargs='?', default='empty')
    parser.add_argument("--labels", nargs='?', default='empty')
    args = parser.parse_args()
    if args.dir == 'empty':
        path = 'vid'
    else:
        path = args.dir
    if args.out == 'empty':
        out_path = 'out'
    else:
        out_path = args.out
    if args.labels == 'empty':
        label_file = 'labels.yaml'
    else:
        label_file = args.labels
    labels = {}
    with open(label_file, 'r') as yamlfile:
        labels = yaml.load(yamlfile, Loader=yaml.FullLoader)
    framecounter = 0
    cv2.namedWindow('Handotate--press q to quit')
    for vidfile in glob.glob(os.path.join(path, '*.m4v')):

        print(vidfile)
        filename = os.path.join(out_path,os.path.splitext(os.path.basename(vidfile))[0]+'.csv')
        with open(filename, 'w+') as csvfile:
            filewriter = csv.writer(csvfile)
            cap = cv2.VideoCapture(vidfile)
            frame_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if (cap.isOpened()== False): 
                print("Error opening video stream or file")
            exit_f = False
            label = None
            while(cap.isOpened() and exit_f == False):
                # Capture frame-by-frame
                ret, frame_original = cap.read()
                frame = copy(frame_original)

                if ret == True:
                    # Display the resulting frame
                    cv2.imshow('Frame',frame)
                    frame_labels = []
                    for category in labels.keys():
                        frame = copy(frame_original)
                        
                        cv2.putText(frame,"Frame {}/{}: Select Label for {}:".format(framecounter,frame_length,category),(50,50),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale = 1, color = (255,255,255), lineType=2, thickness=4)
                        cv2.putText(frame,"{}".format(labels[category]),(50,100),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale = 1, color = (255,255,255), lineType=2, thickness=4)

                        if label != None:
                            cv2.putText(frame,"Last Selected Label: {}".format(label),(50,700),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale = 1, color = (255,255,255), lineType=2, thickness=4)
                            cv2.imshow('Frame',frame)
                        cv2.imshow('Frame',frame)
                        input_k = cv2.waitKey(0) & 0xFF
                        if input_k == ord('q'):
                            cap.release()
                            cv2.destroyAllWindows()
                            exit_f = True
                            break
                        label = process_label(input_k,labels[category])
                        if label == None:
                            continue
                        frame_labels.append(label)
                    
                    filewriter.writerow(frame_labels)
                    framecounter += 1
        
                        
                
                
                # Break the loop
                else: 
                    break
            
        # When everything done, release the video capture object
        cap.release()
        
        # Closes all the frames
        cv2.destroyAllWindows()