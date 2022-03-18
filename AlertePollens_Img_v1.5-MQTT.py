# Web Scraping img + reconnaissance couleur
# CUPRESSACÃ‰ES 2022
# https://www.pollens.fr/uploads/historic/2022/cypres.png
# CARTE DE VIGILANCE DES POLLENS
# https://www.pollens.fr/generated/vigilance_map.png

# pip install pillow
# pip install paho-mqtt

# -------------------------------------------------------------------------------------------
# Télégarchement images sur le WEB

from IPython.display import clear_output
import time
from datetime import datetime
import requests
import math

cpt = 0

# debugMode
debugMode = 1;


while True:  
    
    # Map gÃ©nÃ©rale CARTE DE VIGILANCE DES POLLENS 
    imgURL_Vigil = "https://www.pollens.fr/generated/vigilance_map.png"
    response = requests.get(imgURL_Vigil)
    file = open("vigilance_map.png", "wb")
    file.write(response.content)
    file.close()
    
    
    # Map cyprÃ¨s CUPRESSACÃ‰ES 
    imgURL_Cypres = "https://www.pollens.fr/uploads/historic/2022/cypres.png"
    response = requests.get(imgURL_Cypres)
    file = open("cypres.png", "wb")
    file.write(response.content)
    file.close()
    
    # -------------------------------------------------------------------------------------------
    # Divers fonctions
    
    def ExtractAlerteNiveau (R , G , B):
        # RGB Rouge Vert Bleu
        if R <= 60 and G >= 128 and B <= 60:
            Couleur = "Vert"
            Niveau = "FAIBLE"
            CouleurRGB = [0, 128, 0]
        elif  R >=200 and G >= 200 and B <= 60:
            Couleur = "Jaune"   
            Niveau = "MOYEN"
            CouleurRGB = [255, 255, 0]
        elif R >=200 and G <= 60 and B <= 60:
            Couleur = "Rouge"
            Niveau = "ELEVE"
            CouleurRGB = [255, 0, 0]
        else:
            Couleur = "?"   
            Niveau = "NUL"
            CouleurRGB = [R, G, B]
            
        return Couleur, Niveau, CouleurRGB
    
    def DrawCross(img, x, y , height):
          from PIL import ImageDraw
          draw = ImageDraw.Draw(img)
          draw.line([x, y-height, x, y+height],(0,0,0))
          draw.line([x-height, y, x+height, y],(0,0,0))  
          
          
    # -------------------------------------------------------------------------------------------
    # Map gÃ©nÃ©rale CARTE DE VIGILANCE DES POLLENS
    # Traitement d'image pour reconnaissance par couleur
    
    from PIL import Image
    
    # Ouverture image
    img = Image.open("vigilance_map.png").convert('RGB')
    size = (470,470)
    img.thumbnail(size)
    # img.show()
    if debugMode :
        print(img.format, img.size, img.mode)
    # PNG (401, 422) RGBA
    
    # Lecture de la couleur du pixel
    # ReadPix_X = 300
    # ReadPix_Y = 330
    ReadPix_X = 300
    ReadPix_Y = 330
    ColorPixelRGB = img.getpixel((ReadPix_X,ReadPix_Y))
    # Couleur utilisÃ©e sur le site
    # vert = (0, 128, 0, 255)
    # jaune (255, 255, 0, 255)
    # rouge = (255, 0, 0, 255)
    AlerteNiveau = ExtractAlerteNiveau(ColorPixelRGB[0],ColorPixelRGB[1],ColorPixelRGB[2])
    Vigil_Gard_CouleurAlerte = AlerteNiveau[0]
    Vigil_Gard_NiveauAlerte = AlerteNiveau[1]
    Vigil_Gard_CouleurAlerteRGB = str(AlerteNiveau[2])
    if debugMode :
        print("CouleurAlerte:", Vigil_Gard_CouleurAlerte ,"; NiveauAlerte:" , Vigil_Gard_NiveauAlerte, "; RGB:" , Vigil_Gard_CouleurAlerteRGB)
        
        DrawCross(img,ReadPix_X,ReadPix_Y,10)
        #draw.circle((50,50,50), (255,255,255))
        #draw.line([50, 50, 100, 100],(255,255,255))
        
        img.show()
        time.sleep(5)
        
    # -------------------------------------------------------------------------------------------
    # Map cyprÃ¨s CUPRESSACÃ‰ES 
    # Traitement d'image pour reconnaissance par couleur
    
    from PIL import Image
    
    # Ouverture image
    img = Image.open("cypres.png").convert('RGB')
    size = (470,470)
    img.thumbnail(size)
    # img.show()
    if debugMode :
        print(img.format, img.size, img.mode)
    # PNG (401, 422) RGBA
    
    
    # Lecture de la couleur du pixel
    # 1000 1100
    # ReadPix_X = 300
    # ReadPix_Y = 330
    ReadPix_X = 300
    ReadPix_Y = 330
    ColorPixelRGB = img.getpixel((ReadPix_X,ReadPix_Y))
    # Couleur utilisÃ©e sur le site
    # vert = (0, 128, 0, 255)
    # jaune (255, 255, 0, 255)
    # rouge = (255, 0, 0, 255)
    AlerteNiveau = ExtractAlerteNiveau(ColorPixelRGB[0],ColorPixelRGB[1],ColorPixelRGB[2])
    Cypres_Gard_CouleurAlerte = AlerteNiveau[0]
    Cypres_Gard_NiveauAlerte = AlerteNiveau[1]
    Cypres_Gard_CouleurAlerteRGB = str(AlerteNiveau[2])
    if debugMode :
        print("CouleurAlerte:", Cypres_Gard_CouleurAlerte ,"; NiveauAlerte:" , Cypres_Gard_NiveauAlerte, "; RGB:" , Cypres_Gard_CouleurAlerteRGB)
              
        DrawCross(img,ReadPix_X,ReadPix_Y,10)
        #draw.circle((50,50,50), (255,255,255))
        #draw.line([50, 50, 100, 100],(255,255,255))

        img.show()
        time.sleep(2)
    
    # -------------------------------------------------------------------------------------------
    # Diffusion des donnÃ©es via MQTT et le broker local sur serveur Unraid
    
    import paho.mqtt.client as paho
    broker="192.168.1.42"
    port=1883
    
    def on_publish(client,userdata,result):             #create function for callback
        print("Data published ", result)
        pass
    
    client1= paho.Client("control1")                           #create client object
    client1.username_pw_set("admin", password="147258")  # if password_file /mosquitto/config/passwd
    client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker,port)                                 #establish connection
    
    # AlertePollens_VigilPollensGardCouleur (eviter _)
    ret= client1.publish("AP/VPC",Vigil_Gard_CouleurAlerte)                   #publish
    # AlertePollens_VigilPollensGardNiveau (eviter _)
    ret= client1.publish("AP/VPN",Vigil_Gard_NiveauAlerte, qos=1, retain=True)                   #publish
    ret= client1.publish("AP/VPCrgb",Vigil_Gard_CouleurAlerteRGB) 
    
    #AlertePollens/Cyprés sGard_Couleur
    ret= client1.publish("AP/CGC",Cypres_Gard_CouleurAlerte)                   #publish
    #AlertePollens/CyprÃ¨sGardNiveau
    ret= client1.publish("AP/CGN",Cypres_Gard_NiveauAlerte, qos=1, retain=True)                   #publish
    ret= client1.publish("AP/CGCrgb",Cypres_Gard_CouleurAlerteRGB) 
    

    print("VigilPollensGard" , Vigil_Gard_CouleurAlerte, Vigil_Gard_NiveauAlerte, Vigil_Gard_CouleurAlerteRGB)
    print("CypresGard" , Cypres_Gard_CouleurAlerte, Cypres_Gard_NiveauAlerte, Cypres_Gard_CouleurAlerteRGB)
    
    # print(cpt , time.time() )
    
    datetimeNow = str(datetime.now())
    ret= client1.publish("AP/datetime", datetimeNow, qos=1, retain=True )
    
    # Signal générator test
    mathCpt = math.sin(cpt)
    print("cpt :" , mathCpt ) 
    ret= client1.publish("AP/math", mathCpt , qos=1, retain=True ) 
    cpt = cpt + 1
    
    print(datetimeNow)
    sleepTime = 10
    print("Sleep time :" , sleepTime ,"s") 
    print()
    time.sleep(sleepTime)
    # Clear print Jupyter
    clear_output(wait=True)
    
   
