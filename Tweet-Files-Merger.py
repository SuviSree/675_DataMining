import os
import csv
path=os.getcwd()
print(path)
files=os.listdir(path)
#Add the case name in /Data/casename.csv
outfile=str(path)+str("\\DATA\\USElection-Tweets.csv");
OF=open(outfile,"w",encoding="utf-8",newline='');
csvWriter=csv.writer(OF)
Data=[];
for file in files:
    if ".csv" in file:
        f=open(file,"r",encoding="utf-8");
        csvReader=csv.reader(f);
        for row in csvReader:
            if len(row)!=1:
                d=row[0];
                for i in range(1,len(row)):
                    d=d+","+str(row[i])
            else:
                d=str(row[0])
                #d=d.replace("[","");
                #d=d.replace("]","");
                #d=d.replace("\"","\'");
                d=d.replace("\n","")
            filtered_row=eval(d);
            if len(filtered_row) !=20:
                print(row)
            Data.append(filtered_row)
        f.close()
        print("Reading from",file,"is DONE")
for row in Data:
    csvWriter.writerow([row])
OF.close()
            
        