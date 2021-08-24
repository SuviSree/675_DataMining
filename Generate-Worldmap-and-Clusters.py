from geopy.geocoders import Nominatim
import folium
import csv



def CreateCluster(LAT_LON_Dict,e,m,filename):
    import numpy as np
    import matplotlib.pyplot as plt
    XX=[list(x) for x in LAT_LON_Dict];
    X=np.array(XX) 
    plt.figure(figsize=(60,30))
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
    #plt.xlim((-150,-50))
    plt.savefig(filename)
	
def FindingEps(LAT_LON_Dict):
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
    plt.savefig("US-eps-selection.png")
        
#################################################
geolocator = Nominatim(user_agent="Vishal")
################################################


filename="France-Vienna-TweetsLat_Lon_Sent.csv"
#filename="USElection-TweetsLat_Lon_Sent.csv"
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
location = geolocator.geocode("Niamey")
mapit = folium.Map( location=[location.latitude, location.longitude], zoom_start=5 )
for coord in LAT_LON_Dict:
    sent=sum([x[1]for x in LAT_LON_Dict[coord]])/len(LAT_LON_Dict[coord])
    if sent>0 and sent<=0.25:
        folium.Circle( location=[ coord[0], coord[1] ], color='darkred', radius=len(LAT_LON_Dict[coord])*10,fill_color='darkred' ).add_to( mapit )
    elif sent>0.25 and sent<=0.5:
        folium.Circle( location=[ coord[0], coord[1] ], color='red', radius=len(LAT_LON_Dict[coord])*10,fill_color='red' ).add_to( mapit )
    elif sent>0.5 and sent<=0.75:
        folium.Circle( location=[ coord[0], coord[1] ], color='green', radius=len(LAT_LON_Dict[coord])*10,fill_color='green' ).add_to( mapit )
    elif sent>0.75 and sent<=1:
        folium.Circle( location=[ coord[0], coord[1] ], color='darkgreen', radius=len(LAT_LON_Dict[coord])*10,fill_color='darkgreen', ).add_to( mapit )
CreateCluster(LAT_LON_Dict,.5,10,filename.replace(".csv","")+".png")

mapit.save( 'France.html')
#mapit.save( 'US.html')



    

    