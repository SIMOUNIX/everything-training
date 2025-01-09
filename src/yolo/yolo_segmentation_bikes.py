from ultralytics import YOLO, SAM

# load a pretrained model
yolo_model = YOLO("yolo11x-seg.pt")
# sam_model = SAM("sam2.1_b.pt")


# use the model to segment bikes in an image
results_yolo = yolo_model("locked_bicycle.jpg", classes=[1])
# results_sam = sam_model("locked_bicycle.jpg")

# display the results
for result in results_yolo:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    # result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk
