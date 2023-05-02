# importing requried libraries
import warnings
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image
import cv2
import os
import time
#removing warnings form the runtime for better flow of ui
warnings.filterwarnings("ignore")

#defining some usefull objects:
mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # initializing mtcnn for face detection
resnet = InceptionResnetV1(pretrained='vggface2').eval() # initializing resnet for face img to embeding conversion


animation = "/-\|" # animation frames
frame_width, frame_height = 640, 480
frame_rate = 30

#defining usefull functions:
statements = ["click!",1,2,3]
def print_321():
  # Loop through the statements in reverse order, with a delay before each one
  for i in range(len(statements), 0, -1):
      print(statements[i-1])
  time.sleep(1)
#----------------------------------------------------------------------------------------------------------------------------------------------------
# to register a person in the database by clicking photos of the person in conversation mode:------------------------------------
def register():
  main_directory = "database"

  # Create the main directory if it doesn't exist
  if not os.path.exists(main_directory):
      os.makedirs(main_directory)

  # Prompt the user for a name
  name = input("Enter your name: ")

  # Set the directory for the user's photos
  directory = os.path.join(main_directory, name)

  # Create the user's directory if it doesn't exist
  if not os.path.exists(directory):
      os.makedirs(directory)

  # Set the number of photos to capture
  num_photos = 30

  # Set the time limit in seconds
  time_limit = 10

  # Set the camera device index (0 is usually the default camera)
  camera_index = 0

  # Initialize the camera
  print_321()
  cap = cv2.VideoCapture(camera_index)

  # Set the frame width and height
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

  # Set the frame rate
  cap.set(cv2.CAP_PROP_FPS, 30)

  # Calculate the time interval between photos
  time_interval = time_limit / num_photos

  # Capture and save the photos
  for i in range(num_photos):
      # Capture a frame
      ret, frame = cap.read()
      
      # Construct the filename
      filename = os.path.join(directory, f"photo_{i+1}.jpg")
      
      # Save the frame to a file
      cv2.imwrite(filename, frame)
      # Wait for the time interval before capturing the next photo
      cv2.waitKey(int(time_interval * 1000))
      
  # Release the camera
  cap.release()
  process()

# for indexing:-------------------------------------------------------------------------------------------------------------------------  
def collate_fn(x):
    return x[0]

#to_process the data and create data.pt file to store required embeddings:---------------------------------------------------------------
def process():
  print("processing the data........")
  dataset=datasets.ImageFolder('database') # photos folder path 
  idx_to_class = {i:c for c,i in dataset.class_to_idx.items()}
  loader = DataLoader(dataset, collate_fn=collate_fn)

  face_list = [] # list of cropped faces from photos folder
  name_list = [] # list of names corrospoing to cropped photos
  embedding_list = [] # list of embeding matrix after conversion from cropped faces to embedding matrix using resnet

  for img, idx in loader:
      face, prob = mtcnn(img, return_prob=True) 
      if face is not None and prob>0.90: # if face detected and porbability > 90%
          emb = resnet(face.unsqueeze(0)) # passing cropped face into resnet model to get embedding matrix
          embedding_list.append(emb.detach()) # resulten embedding matrix is stored in a list
          name_list.append(idx_to_class[idx]) # names are stored in a list

  data = [embedding_list, name_list]
  torch.save(data, 'data.pt')
  print("Almost done..........")

#for testing or to detecting the person and return respective name:----------------------------------------------------------------------
def detect():
    print("detecting.......")
    dir='test'
    data_dir='data.pt'
    if not os.path.exists(dir):
      os.makedirs(dir)
    # Capture a photo and save it to the given directory
    print_321()
    cap = cv2.VideoCapture(0)

    # Set the frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Set the frame rate
    cap.set(cv2.CAP_PROP_FPS, 30)
    ret, frame = cap.read()
    filename = os.path.join(dir, "photo.jpg")
    cv2.imwrite(filename, frame)

    # Match the captured photo with the dataset
    img_path = filename
    img = Image.open(img_path)
    face, prob = mtcnn(img, return_prob=True) # returns cropped face and probability
    emb = resnet(face.unsqueeze(0)).detach() # detach is to make required gradient false
    
    saved_data = torch.load(data_dir) # loading data.pt file
    embedding_list = saved_data[0] # getting embedding data
    name_list = saved_data[1] # getting list of names
    dist_list = [] # list of matched distances, minimum distance is used to identify the person
    
    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)
        
    idx_min = dist_list.index(min(dist_list))
    result = (name_list[idx_min], min(dist_list))

    print("This is : ", result[0])
 
    cap.release()
    return result  
register()
detect()
