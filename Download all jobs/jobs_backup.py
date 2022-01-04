import os

projects = open("project_inventory.txt", "r")
for project in projects.readlines():
    extract = []
    extract.append("rd jobs list -p "+ project.strip('\n') +" |  grep -o '^[^ ]*' | sed 1,2d  > job_id.txt ")
    print("Extracting job id's......")
    os.system(extract[0])
    os.system("mkdir " +project.strip('\n'))

    id = open("job_id.txt", "r")
    for i in id:
        print(project)

        # downloading jobs by id
        st =[]
        st.append("rd jobs list -i " + i.strip('\n') + " -f ./"+project.strip('\n')+"/"+i.strip('\n')+".xml -p " +project.strip('\n'))
        print("downloading job: "+i.strip('\n'))
        os.system(st[0])