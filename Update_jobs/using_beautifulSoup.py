import os
from bs4 import BeautifulSoup


#input project name
project = input("Please enter the project name: ")
print(project)

#extractiong job list by id
extract = []
extract.append("rd jobs list -p "+ project +" |  grep -o '^[^ ]*' | sed 1,2d  > job_id.txt ")
os.system(extract[0])

#downloading xml file
file1 = open("job_id.txt", "r")
for i in file1:
    st =[]
    st.append("rd jobs list -i " + i.strip('\n') + " -f "+i.strip('\n')+".xml -p " +project)
    print(st)
    os.system(st[0])
    
    #opening xml files
    with open(i.strip("\n")+".xml", "r") as f:
     content = f.read()
    y = BeautifulSoup(content, features="html.parser")
    print(id)
    #Creating new tags
    new_tag = y.new_tag("dispatch")
    new_tag1 = y.new_tag("excludePrecedence")
    new_tag2 = y.new_tag("keepgoing")
    new_tag3 = y.new_tag("rankOrder")
    new_tag4 = y.new_tag("successOnEmptyNodeFilter")
    new_tag5 = y.new_tag("threadcount")
    new_tag6 = y.new_tag("nodefilters")
    new_tag7 = y.new_tag("filter")
    
    # Adding values to tag
    new_tag1.string = "true"
    new_tag2.string = "false"
    new_tag3.string = "ascending"
    new_tag4.string = "false"
    new_tag5.string = "1"
    new_tag7.string = ".*"
    
    #Appending in respective position
    y.job.insert(2,new_tag)
    y.dispatch.append(new_tag1)
    y.dispatch.append(new_tag2)
    y.dispatch.append(new_tag3)
    y.dispatch.append(new_tag4)
    y.dispatch.append(new_tag5)
    y.job.append(new_tag6)
    y.nodefilters.append(new_tag7)
    f = open(i.strip("\n")+".xml", "w")
    f.write(y.prettify())


    #uploading the xml file to rundeck
    upload = []
    upload.append("rd jobs load -f " +i.strip("\n")+".xml -p " +project)
    os.system(upload[0])
