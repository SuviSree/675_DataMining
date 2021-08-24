from geopy.geocoders import Nominatim
import folium
import csv



def CreateCluster(LAT_LON_Dict,e,m,filename):
    import numpy as np
    import matplotlib.pyplot as plt
    XX=[list(x) for x in LAT_LON_Dict];
    X=np.array(XX) 
    plt.plot(X[:,1],X[:,0],"o",color='k')
    from sklearn.cluster import DBSCAN
    db = DBSCAN(eps=e, min_samples=m).fit(X)
    cluster_labels = db.labels_
    Cluster_Dict={}
    for label in cluster_labels:
        Cluster_Dict[label]=[];
    for i in range(len(X)):
        Cluster_Dict[cluster_labels[i]]+=[list(X[i])]
    for cluster in Cluster_Dict:
        if cluster==-1:
            continue;
        cluster_cords=np.array(Cluster_Dict[cluster]);
        plt.plot(cluster_cords[:,1],cluster_cords[:,0],'o')
    #plt.ylim((-90,90))
    #plt.xlim((-180,180))
    #plt.ylim((-90,90))
    #plt.xlim((70,100))
    plt.savefig(filename)
	
def CreateCluster2(LAT_LON_Dict):
    import numpy as np
    import matplotlib.pyplot as plt
    XX=[list(x) for x in LAT_LON_Dict];
    X=np.array(XX) 
    #plt.plot(X[:,1],X[:,0],"o",color='k')
    from sklearn.cluster import DBSCAN
    C=[];
    for i in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
        db = DBSCAN(eps=i, min_samples=10).fit(X)
        cluster_labels = len(np.unique(db.labels_))
        C.append([i,cluster_labels]);
    C=np.array(C)
    plt.plot(C[:,0],C[:,1],"-o")
    plt.savefig("Hathras-eps-selection.png")
        
#################################################
geolocator = Nominatim(user_agent="Vishal")
################################################

#-----------------------------------------------------#
#Comment one filename to generate other filename case's map and corresponding Cluster Image 
filename="Farmer-TweetsLat_Lon_Sent.csv"
#filename="Hathras-TweetsLat_Lon_Sent.csv"
#-----------------------------------------------------#
rows = []
with open(filename, 'r',encoding="utf-8") as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(eval(row[0]))
myrows=rows
LAT_LON_Dict={}
for c in myrows:
    location = (c[20],c[21])
    if location not in LAT_LON_Dict:
        LAT_LON_Dict[location]=[[c[22],c[24],c[25]]]
    else:
        LAT_LON_Dict[location]+=[[c[22],c[24],c[25]]]
    #print(location)
    #region.append(c.find('region/name').text)

## for india map
location = geolocator.geocode("jabalpur")
ind_coord = geolocator.geocode("India")
mapit = folium.Map( location=[location.latitude, location.longitude], zoom_start=5 )
temp_LAT_LON_Dict={}
#To know number of number of tweets in large cirsle, increase circle size
for coord in LAT_LON_Dict:
    sent=sum([x[1]for x in LAT_LON_Dict[coord]])/len(LAT_LON_Dict[coord])
    if (ind_coord.latitude,ind_coord.longitude)==coord:
        continue;
    if LAT_LON_Dict[coord][0][0].split(",")[-1].replace(" ","")!="India":
        continue;
    temp_LAT_LON_Dict[coord]=None;
    if sent>0 and sent<=0.25:
        folium.Circle( location=[ coord[0], coord[1] ], color='darkred', radius=len(LAT_LON_Dict[coord])*10,fill_color='darkred' ).add_to( mapit )
    elif sent>0.25 and sent<=0.5:
        folium.Circle( location=[ coord[0], coord[1] ], color='red', radius=len(LAT_LON_Dict[coord])*10,fill_color='red' ).add_to( mapit )
    elif sent>0.5 and sent<=0.75:
        folium.Circle( location=[ coord[0], coord[1] ], color='green', radius=len(LAT_LON_Dict[coord])*10,fill_color='green' ).add_to( mapit )
    elif sent>0.75 and sent<=1:
        folium.Circle( location=[ coord[0], coord[1] ], color='darkgreen', radius=len(LAT_LON_Dict[coord])*10,fill_color='darkgreen', ).add_to( mapit )
#Create Cluster
CreateCluster(temp_LAT_LON_Dict,.4,10,filename.replace(".csv","")+".png")

#mapit.save( 'indiamap_farmer.html')
#mapit.save( 'Hathras.html')
mapit.save( 'Farmer.html')

    

    