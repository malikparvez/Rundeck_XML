from contextlib import nullcontext
import xml.etree.ElementTree as ET
import os


#input project name
project = input("Please enter the project name: ")
print(project)


#extractiong job list by id
extract = []
extract.append("rd jobs list -p "+ project +" |  grep -o '^[^ ]*' | sed 1,2d  > job_id.txt ")
print("Extracting job id's......")
os.system(extract[0])


#downloading xml file
id = open("job_id.txt", "r")
for i in id:
    st =[]
    st.append("rd jobs list -i " + i.strip('\n') + " -f "+i.strip('\n')+".xml -p " +project)
    print("downloading job: "+i.strip('\n'))
    os.system(st[0])
    

    # opening xml file
    tree = ET.parse(i.strip("\n")+".xml")

    # find desired element
    root = tree.find("job")
    toremove2 = root.find("nodefilters")
    toremove1 = root.find("dispatch")

    
    # remove if exists
    if toremove1 :
        print(toremove1.tag+" is already present")
        print("deleting "+toremove1.tag+"......") 
        root.remove(toremove1)

    if toremove2:
        print(toremove2.tag+" is already present")
        print("deleting "+toremove2.tag+"......")
        root.remove(toremove2)



    # Creating tag
    tag1 = ET.Element("dispatch")
    tag2 = ET.Element("excludePrecedence")
    tag3 = ET.Element("keepgoing")
    tag4 = ET.Element("rankOrder")
    tag5 = ET.Element("successOnEmptyNodeFilter")
    tag6 = ET.Element("threadcount")
    tag7 = ET.Element("nodefilters")
    tag8 = ET.Element("filter")

    # appending tag 
    root.append(tag1)
    tag1.append(tag2)
    tag1.append(tag3)
    tag1.append(tag4)
    tag1.append(tag5)
    tag1.append(tag6)
    root.append(tag7)
    tag7.append(tag8)


    # adding values to tag
    tag2.text = "true"
    tag3.text = "false"
    tag4.text = "ascending"
    tag5.text = "false"
    tag6.text = "1"
    tag8.text = ".*"


    # writing to file
    tree.write(i.strip("\n")+".xml")
    print("file successfully written")
    
    #uploading the xml file to rundeck
    try:
        os.system("rd jobs load -f " +i.strip("\n")+".xml -p " +project)
        print("Great "+ i.strip('\n')+ "uploded successfully")
    except:
        print("Upload failed for "+ i.strip('\n'))
        