import json
import re



def removeObjectAttribute(frame):
    frame1 = {key:value for key, value in frame.items() if key != "objects"}
    frame1 = {key:value for key, value in frame1.items() if key != "objects_changed"}
    return frame1

def remove_memo_personIdx(frames):
    for frame in frames:
        if frame["persons"]:    
            for idx, person in enumerate(frame["persons"]):
                person2 = {key:value for key, value in person.items() if key!="memo"}
                person2 = {key : value for key, value in person2.items() if key != "person_index"} 
                frame["persons"][idx] = person2
        frame["skeleton"] = frame["persons"]
        del frame["persons"]
    return frames



def attributeChange(dict):
    for data in dict["data"]:
        if data["skeleton"]:
            for skeleton in data["skeleton"]:
                skeleton["pose"] = skeleton["keypoints"]
                skeleton["score"] = skeleton["keypoints_score"]

                del skeleton["keypoints"]
                del skeleton["keypoints_score"]
    return dict

def data_converter(path):
    with open(path, "rb") as f:
        jsonDict = json.load(f)

    frames = list()
    for frame in jsonDict["frames"]:
        frame = removeObjectAttribute(frame)
        frames.append(frame)

    frames = remove_memo_personIdx(frames)
    new_dict = {"data": frames}
    new_dict = attributeChange(new_dict)
    rm = re.sub("[-=_.#/>:$}]","",path)
    labels = re.sub("[0-9]","", rm).split("x")
    label_index = re.sub("[a-zA-Z]","", rm)[3]
    
    label = labels[0]

    new_dict["label"] = label
    new_dict["label_index"] = label_index
    
    
    return new_dict
