import json
import re

file_path = "./sample3.json"
#sample.json 파일을 만들어서 json 구조를 확인하기 위함
def removeObjectAttribute(frame):
    frame1 = {key: value for key, value in frame.items() if key != "objects"}
    frame1 = {key: value for key, value in frame1.items() if key != "objects_changed"}

    return frame1


def remove_useless_in_persons(frames):
    for frame in frames:
        if frame["persons"]:
            for idx, person in enumerate(frame["persons"]):
                person2 = {key: value for key, value in person.items() if key != "memo"}
                person2 = {key: value for key, value in person2.items() if key != "person_index"}
                person2 = {key: value for key, value in person2.items() if key != "keypoints_movement"}
                person2 = {key: value for key, value in person2.items() if key != "keypoints_angle"}
                person2 = {key: value for key, value in person2.items() if key != "person_center"}

                frame["persons"][idx] = person2
        frame["skeleton"] = frame["persons"]
        del frame["persons"]
    return frames



def convertSkeleton(dict):
    for data in dict["data"]:
        if data["skeleton"]:
            for skeleton in data["skeleton"]:
               
                skeleton["pose"] = list()
               
                skeleton["score"] = list()

                for i in range(19):
                    if i in [9,10,11,12,13,14,15,16,17,18]:
                        # print(i)
                        split = list(map(float, skeleton["keypoints"][i].split(",")))
                    
                        skeleton["pose"].append(split[0])
                        skeleton["pose"].append(split[1])
                       
                        skeleton["score"].append(float(skeleton["keypoints_score"][i]))
                    elif i in [0,1,2,3,4,5,6,7]:
                        # print(i)
                        split = list(map(float, skeleton["keypoints"][i].split(",")))
                        skeleton["pose"].append(split[0])
                        skeleton["pose"].append(split[1])
                        
                      
                        skeleton["score"].append(float(skeleton["keypoints_score"][i]))
                    else:
                        pass

                del skeleton["keypoints"]
                del skeleton["keypoints_score"]
    return dict


def convert(path):
    with open(path, "rb") as f:
        jsonDict = json.load(f)

    frames = list()
    for frame in jsonDict["frames"]:
        frame = removeObjectAttribute(frame)
        frames.append(frame)

    frames = remove_useless_in_persons(frames)
    new_dict = {"data": frames}
    new_dict = convertSkeleton(new_dict)
    rm = re.sub("[-=_.#/>:$}]", "", path)
    labels = re.sub("[0-9]", "", rm).split("x")
    label_index = re.sub("[a-zA-Z]", "", rm)[3]

    label = labels[0]

    new_dict["label"] = label
    new_dict["label_index"] = label_index

    with open(file_path, 'w') as outfile :
        json.dump(new_dict, outfile, indent =4)
    return new_dict

def a(path):
    with open(path, "rb") as f:
        jsonDict = json.load(f)
    with open(file_path, 'w') as outfile :
        json.dump(jsonDict, outfile, indent =4)

framePreprocess("C:\JuYeong\Fighting002_x264.json")
#a("C:\JuYeong\---QUuC4vJs.json")