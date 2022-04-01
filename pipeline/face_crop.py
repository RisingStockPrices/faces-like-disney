import dlib
import cv2
import os
import numpy as np
import pandas as pd

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./detector/shape_predictor_68_face_landmarks.dat')

def detect_face(pth,outfile=None,debug=True,landmark_csv='/home/spock-the-wizard/3d-disney-face/data/landmark.csv',face_outdir='./data/cropped'):
    image = cv2.imread(pth)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(rgb, 1)

    if debug: 
        # Detect landmarks for each face
        for rect in rects:
            # Get the landmark points
            shape = predictor(rgb, rect)
            # Convert it to the NumPy Array
            shape_np = np.zeros((68, 2), dtype="int")
            for i in range(0, 68):
                shape_np[i] = (shape.part(i).x, shape.part(i).y)
            shape = shape_np

            # Display the landmarks
            for i, (x, y) in enumerate(shape):
            # Draw the circle to mark the keypoint 
                cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
            
        cv2.imwrite(outfile,image)
    else:
        # Detect landmarks for each face
        for idx,rect in enumerate(rects):
            # Get the landmark points
            shape = predictor(rgb, rect)
            # Convert it to the NumPy Array
            shape_np = np.zeros((68, 2), dtype="int")
            for i in range(0, 68):
                shape_np[i] = (shape.part(i).x, shape.part(i).y)
            shape = shape_np

            # idx = len(df)
            # get movie name 
            movie = pth.split('/')[-2]
            file = pth.split('/')[-1].split('.')[0].replace('스크린샷','screenshot')
            
            # import pdb;pdb.set_trace()
            face_file = os.path.join(face_outdir,'%s_%s_%s.png'%(movie,file,str(idx).zfill(4)))
            keypoints = shape

            # save cropped image as face_file
            center = rect.center()
            size = int(1.2*max(rect.width(),rect.height()))
            
            threshold = 150
            # import pdb;pdb.set_trace()
            if size<threshold:
                continue
            y_start = center.y-size#+pad_width[0]
            x_start = center.x-size#+pad_width[0]
            cropped = image[y_start:y_start+2*size,x_start:x_start+2*size]
            try:
                cropped = cv2.resize(cropped,(1024,1024))
            except:
                continue
            # import pdb;pdb.set_trace()
            cv2.imwrite(face_file,cropped)


            # df.loc[idx] = [face_file,pth,keypoints,rect]
            # df.to_csv(landmark_csv)


if __name__=="__main__":
    # root = './data/raw'
    movies = ['theincredibles']
    for movie in movies:
        root = './data/raw/%s'%movie
        outdir = './data/cropped.v2/%s'%movie
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        for file in os.listdir(root):
            print(file)
            
            # outfile = './data/cropped/%s_%s.png'%(movie,str(idx).zfill(5))
            detect_face(os.path.join(root,file),face_outdir=outdir,debug=False)
