import os
import time
from csv import reader
import multiprocessing
from shutil import copy
from operator import itemgetter
from math import log10
from datetime import datetime, timedelta
import gmplot
import numpy as np
from slack import WebClient
from obspy import UTCDateTime
from ipynb.fs.full.funk import download1
from ipynb.fs.full.funk import download2
from ipynb.fs.full.funk import download3
from ipynb.fs.full.funk import download4
from EQTransformer.core.mseed_predictor import mseed_predictor
from geopy import distance
from scipy.optimize import least_squares

def residuals_fn(points):
    def fn(location):
        return np.array( [ (distance.distance(p, location).km - r)*(r*r) for (p, r) in points ] )
    return fn

def multilateration(points):
    ps = [x[0] for x in points]
    x0 = np.mean(np.array(ps),axis=0)
    return least_squares(residuals_fn(points), x0).x


client = WebClient(token="xoxb-1648714122736-1621786781861-Bq4TGn3qEWwml1nSfx8mnJNa")
response = client.conversations_open(users=["U01JCRMUM7U"])

while True:
    try:
        start_time = time.time()
        timeinmin = 15
        now = UTCDateTime((datetime.utcnow() - timedelta(seconds=45)).strftime('%Y-%m-%dT%H:%M:%S.%f'))
        #now = UTCDateTime("2021-01-15T12:02:00")
        print((datetime.utcnow() - timedelta(seconds=945)).strftime('%Y-%m-%dT%H:%M:%S.%f'))
        print((datetime.utcnow() - timedelta(seconds=45)).strftime('%Y-%m-%dT%H:%M:%S.%f'))
        nije_prvi = True
        for dirname, dirs, files in os.walk("C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi\\downloads_mseeds"):
            for i in files:
                if list(i.split("."))[-1] == "mseed":
                    file_path = os.path.join(dirname, i)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        pass

        manager = multiprocessing.Manager()
        sts = manager.dict()


        p1 = multiprocessing.Process(target = download1, args = (sts, now, timeinmin,))
        p1.start()
        p2 = multiprocessing.Process(target = download2, args = (sts, now, timeinmin,))
        p2.start()
        p3 = multiprocessing.Process(target = download3, args = (sts, now, timeinmin,))
        p3.start()
        p4 = multiprocessing.Process(target = download4, args = (sts, now, timeinmin,))
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()

        #print(len(sts))

        mseed_predictor(input_dir='downloads_mseeds', input_model='EqT_model.h5', stations_json='station_list.json', output_dir='detections', detection_threshold=0.2, P_threshold=0.03, S_threshold=0.03, number_of_plots=100, plot_mode='time_frequency', overlap=0.3, batch_size=500)
        folder = 'C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi\\analiza'

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass
                #####print('Failed to delete %s. Reason: %s' % (file_path, e))

        for dirname, dirs, files in os.walk("C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi\\detections"):
            if "X_prediction_results.csv" in files:
                lista = list(dirname.split('\\'))
                os.rename(dirname+"\\X_prediction_results.csv",dirname+"\\"+lista[-1]+".csv")
                #####print(str(dirname)+"\\"+lista[-1]+".csv")
                copy(str(dirname)+"\\"+lista[-1]+".csv", "C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi\\analiza")
            for i in files:
                if list(i.split("."))[-1] == "png":
                    lista = list(dirname.split('\\'))
                    os.rename(dirname+"\\"+i,dirname+"\\"+lista[-2]+"-"+i)
                    #####print(str(dirname)+"\\"+lista[-2]+"-"+i)
                    copy(str(dirname)+"\\"+lista[-2]+"-"+i, "C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi\\analiza")

        paz_wa = {'sensitivity': 2800, 'zeros': [0j], 'gain': 1,
                  'poles': [-6.2832 - 4.7124j, -6.2832 + 4.7124j]}

        lista = []
        for filename in os.listdir("C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi\\analiza"):
            if filename.endswith(".csv"):
                with open("C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi\\analiza\\"+filename, 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    for row in csv_reader:
                        if (row and row[4]!="station_lat" and row[4]!='' and row[5]!='' and row[7]!='' and row[8]!='' and row[11]!='' and row[15]!=''):
                            try:
                                dt = datetime(int(row[7][0:4]),int(row[7][5:7]),int(row[7][8:10]),int(row[7][11:13]),int(row[7][14:16]),int(row[7][17:19]),int(row[7][20:25]))
                            except Exception as e:
                                dt = datetime(int(row[7][0:4]),int(row[7][5:7]),int(row[7][8:10]),int(row[7][11:13]),int(row[7][14:16]),int(row[7][17:19]),0)
                            try:
                                de = datetime(int(row[8][0:4]),int(row[8][5:7]),int(row[8][8:10]),int(row[8][11:13]),int(row[8][14:16]),int(row[8][17:19]),int(row[8][20:25]))
                            except Exception as e:
                                de = datetime(int(row[8][0:4]),int(row[8][5:7]),int(row[8][8:10]),int(row[8][11:13]),int(row[8][14:16]),int(row[8][17:19]),0)
                            try:
                                dp = datetime(int(row[11][0:4]),int(row[11][5:7]),int(row[11][8:10]),int(row[11][11:13]),int(row[11][14:16]),int(row[11][17:19]),int(row[11][20:25]))
                            except Exception as e:
                                dp = datetime(int(row[11][0:4]),int(row[11][5:7]),int(row[11][8:10]),int(row[11][11:13]),int(row[11][14:16]),int(row[11][17:19]), 0)
                            try:
                                ds = datetime(int(row[15][0:4]),int(row[15][5:7]),int(row[15][8:10]),int(row[15][11:13]),int(row[15][14:16]),int(row[15][17:19]),int(row[15][20:25]))
                            except Exception as e:
                                ds = datetime(int(row[15][0:4]),int(row[15][5:7]),int(row[15][8:10]),int(row[15][11:13]),int(row[15][14:16]),int(row[15][17:19]),0)
                            d = (dt - datetime(1970,1,1,0,0,0,0)).total_seconds()
                            dee = (de - datetime(1970,1,1,0,0,0,0)).total_seconds()
                            dd = (ds - dp).total_seconds()
                            ddd = (de - datetime(1970,1,1,0,0,0,0)).total_seconds()
                            dist_to_eq = float(dd * 7)#6.98613133929)
                            ##print(row[2], dist_to_eq)
                            try:
                                stre = sts[row[2]]
                                st = stre.copy()
                                start = UTCDateTime(datetime.utcfromtimestamp(d).strftime('%Y-%m-%dT%H:%M:%S.%f'))
                                end = UTCDateTime(datetime.utcfromtimestamp(dee).strftime('%Y-%m-%dT%H:%M:%S.%f'))
                                st.trim(start, end + 10)
                                a0 = st[1].stats.response.get_paz().normalization_factor
                                if st[1].stats.response.get_paz().input_units != "M/S":
                                    a0 *= 1000000000
                                paz = {'sensitivity': st[1].stats.response.instrument_sensitivity.value, 'zeros': st[1].stats.response.get_paz().zeros, 'gain': a0,'poles': st[1].stats.response.get_paz().poles}

                                st.simulate(paz_remove=paz, paz_simulate=paz_wa)
                                try:
                                    tr_n = st.select(component="N")[0]
                                except Exception as e:
                                    pass
                                try:
                                    tr_n = st.select(component="1")[0]
                                except Exception as e:
                                    pass
                                ampl_n = max(abs(tr_n.data))
                                tr_n.plot()
                                try:
                                    tr_e = st.select(component="E")[0]
                                except Exception as e:
                                    pass
                                try:
                                    tr_e = st.select(component="2")[0]
                                except Exception as e:
                                    pass
                                tr_e.plot()
                                ampl_e = max(abs(tr_e.data))
                                ampl = max(ampl_n, ampl_e)
                                epi_dist = dist_to_eq
                                ##print(ampl)
                                mag1 = log10(ampl*1000) + 1.6627*log10(epi_dist)+0.0008*epi_dist-0.433
                                mag2 = log10(ampl*1000) + 1.110*log10(epi_dist/100)+0.00189*(epi_dist-100)+3
                                mag3 = ((log10(ampl*1000) + 1.110*log10(epi_dist/100)+0.00189*(epi_dist-100)+3)+0.062)/0.992
                                mag4 = 0.885*(log10(ampl*1000) + 1.110*log10(epi_dist/100)+0.00189*(epi_dist-100)+3)+0.257
                                ##print(mag1)
                                ##print(mag2)
                                ##print(mag3)
                                ##print(mag4)
                                ##print((mag1+mag2+mag3+mag4)/4)
                                lista.append([(row[0].split("\\"))[0], float(row[4]), float(row[5]), d, ddd, row[11], ((mag1+mag2+mag3+mag4)/4), row[1], row[15], dist_to_eq, dd])
                            except Exception as e:
                                pass

        lista = sorted(lista, key=itemgetter(3))
        #print(lista)
        eq = []
        mjesta = []
        if len(lista)>=1:
            for i in range(len(lista)):
                if i == 0:
                    tmp = []
                    tmp.append(lista[0])
                    mjesta.append(lista[0][0])
                    ##print("usao1", i, lista[i])
                elif (lista[i][3]-tmp[-1][3]<=45 and lista[i][0] not in mjesta):
                    tmp.append(lista[i])
                    mjesta.append(lista[i][0])
                    ##print("usao2", i, lista[i])
                else:
                    eq.append(tmp)
                    tmp = []
                    mjesta = []
                    tmp.append(lista[i])
                    ##print("usao3", i, lista[i])
                ####print(mjesta)
            if len(tmp)!=0:
                eq.append(tmp)
        #print(eq)
        mags = []
        eq_mags=[]
        for i in range(len(eq)):
            magni=dict()
            ukupno_mag = 0
            print(datetime.utcfromtimestamp(int(eq[i][0][3])+3600).strftime('%Y-%m-%d %H:%M:%S'))
            for j in range(len(eq[i])):
                ukupno_mag+=eq[i][j][6]
                magni[eq[i][j][0]]=eq[i][j][6]
            print(ukupno_mag/len(eq[i]))
            mags.append(ukupno_mag/len(eq[i]))
            eq_mags.append(magni)
            ukupno_mag = 0
            print(len(eq[i]))
        #print(eq)
        #print(eq_mags)

        folder = 'C:\\Users\\Lovro Milišić\\Desktop\\Seizmografi'
        for filename in os.listdir(folder):
            if ".html" in filename:
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    pass
                    #####print('Failed to delete %s. Reason: %s' % (file_path, e))
        bio = False
        apikey = "AIzaSyAMLMeFfhOkreGwx0A2t3TXsQ5vgXoVAA8"
        for i in range(len(eq)):
            datas = []
            #print(eq[i])
            gmap = gmplot.GoogleMapPlotter(45.9854944, 17.3130722, 8, apikey=apikey)
            for j in range(len(eq[i])):
                gmap.circle(eq[i][j][0], eq[i][j][1], eq[i][j][2], eq[i][j][-2]*1000, face_alpha = 0, edge_alpha = 1)
                a = str(datetime.utcfromtimestamp(int(eq[i][0][3])).strftime('%Y-%m-%d %H:%M:%S'))
                a = a.replace(" ", "-")
                a = a.replace(":", ".")
                if eq[i][j][7]!='HU':
                    datas.append(((eq[i][j][1], eq[i][j][2]),eq[i][j][-2]))
            if len(eq[i])>2:
                rj = multilateration(datas)
                gmap.marker(rj[0], rj[1], color='cornflowerblue')
            gmap.draw("map"+a+".html")
            b = "map"+a+".html"
            f = open(b, "r")
            contents = f.readlines()
            f.close()
            index = -1
            #print(str(eq_mags[i]))
            for j in range(len(contents)):
                if "</script>" in contents[j]:
                    index = j
            contents.insert(j-7, """try {
    if (FRGS.getVisible()){
        var x = document.getElementById("FRGS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("FRGS button");
    x.style.display = "none";
    var x = document.getElementById("FRGS ime");
    x.style.display = "none";
    }


    try {
    if (ZAG.getVisible()){
        var x = document.getElementById("ZAG button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("ZAG button");
    x.style.display = "none";
    var x = document.getElementById("ZAG ime");
    x.style.display = "none";
    }


    try {
    if (BEO.getVisible()){
        var x = document.getElementById("BEO button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("BEO button");
    x.style.display = "none";
    var x = document.getElementById("BEO ime");
    x.style.display = "none";
    }


    try {
    if (GROS.getVisible()){
        var x = document.getElementById("GROS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("GROS button");
    x.style.display = "none";
    var x = document.getElementById("GROS ime");
    x.style.display = "none";
    }


    try {
    if (BOJS.getVisible()){
        var x = document.getElementById("BOJS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("BOJS button");
    x.style.display = "none";
    var x = document.getElementById("BOJS ime");
    x.style.display = "none";
    }


    try {
    if (CADS.getVisible()){
        var x = document.getElementById("CADS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("CADS button");
    x.style.display = "none";
    var x = document.getElementById("CADS ime");
    x.style.display = "none";
    }


    try {
    if (CEY.getVisible()){
        var x = document.getElementById("CEY button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("CEY button");
    x.style.display = "none";
    var x = document.getElementById("CEY ime");
    x.style.display = "none";
    }


    try {
    if (CRES.getVisible()){
        var x = document.getElementById("CRES button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("CRES button");
    x.style.display = "none";
    var x = document.getElementById("CRES ime");
    x.style.display = "none";
    }


    try {
    if (CRNS.getVisible()){
        var x = document.getElementById("CRNS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("CRNS button");
    x.style.display = "none";
    var x = document.getElementById("CRNS ime");
    x.style.display = "none";
    }


    try {
    if (DOBS.getVisible()){
        var x = document.getElementById("DOBS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("DOBS button");
    x.style.display = "none";
    var x = document.getElementById("DOBS ime");
    x.style.display = "none";
    }


    try {
    if (GOLS.getVisible()){
        var x = document.getElementById("GOLS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("GOLS button");
    x.style.display = "none";
    var x = document.getElementById("GOLS ime");
    x.style.display = "none";
    }


    try {
    if (GORS.getVisible()){
        var x = document.getElementById("GORS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("GORS button");
    x.style.display = "none";
    var x = document.getElementById("GORS ime");
    x.style.display = "none";
    }


    try {
    if (GBAS.getVisible()){
        var x = document.getElementById("GBAS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("GBAS button");
    x.style.display = "none";
    var x = document.getElementById("GBAS ime");
    x.style.display = "none";
    }


    try {
    if (GBRS.getVisible()){
        var x = document.getElementById("GBRS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("GBRS button");
    x.style.display = "none";
    var x = document.getElementById("GBRS ime");
    x.style.display = "none";
    }


    try {
    if (GCIS.getVisible()){
        var x = document.getElementById("GCIS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("GCIS button");
    x.style.display = "none";
    var x = document.getElementById("GCIS ime");
    x.style.display = "none";
    }


    try {
    if (JAVS.getVisible()){
        var x = document.getElementById("JAVS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("JAVS button");
    x.style.display = "none";
    var x = document.getElementById("JAVS ime");
    x.style.display = "none";
    }


    try {
    if (KNDS.getVisible()){
        var x = document.getElementById("KNDS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("KNDS button");
    x.style.display = "none";
    var x = document.getElementById("KNDS ime");
    x.style.display = "none";
    }


    try {
    if (KOGS.getVisible()){
        var x = document.getElementById("KOGS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("KOGS button");
    x.style.display = "none";
    var x = document.getElementById("KOGS ime");
    x.style.display = "none";
    }


    try {
    if (LJU.getVisible()){
        var x = document.getElementById("LJU button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("LJU button");
    x.style.display = "none";
    var x = document.getElementById("LJU ime");
    x.style.display = "none";
    }


    try {
    if (MOZS.getVisible()){
        var x = document.getElementById("MOZS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("MOZS button");
    x.style.display = "none";
    var x = document.getElementById("MOZS ime");
    x.style.display = "none";
    }


    try {
    if (PDKS.getVisible()){
        var x = document.getElementById("PDKS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("PDKS button");
    x.style.display = "none";
    var x = document.getElementById("PDKS ime");
    x.style.display = "none";
    }


    try {
    if (ROBS.getVisible()){
        var x = document.getElementById("ROBS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("ROBS button");
    x.style.display = "none";
    var x = document.getElementById("ROBS ime");
    x.style.display = "none";
    }


    try {
    if (SKDS.getVisible()){
        var x = document.getElementById("SKDS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("SKDS button");
    x.style.display = "none";
    var x = document.getElementById("SKDS ime");
    x.style.display = "none";
    }


    try {
    if (VISS.getVisible()){
        var x = document.getElementById("VISS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("VISS button");
    x.style.display = "none";
    var x = document.getElementById("VISS ime");
    x.style.display = "none";
    }


    try {
    if (VOJS.getVisible()){
        var x = document.getElementById("VOJS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("VOJS button");
    x.style.display = "none";
    var x = document.getElementById("VOJS ime");
    x.style.display = "none";
    }


    try {
    if (VNDS.getVisible()){
        var x = document.getElementById("VNDS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("VNDS button");
    x.style.display = "none";
    var x = document.getElementById("VNDS ime");
    x.style.display = "none";
    }


    try {
    if (ZAVS.getVisible()){
        var x = document.getElementById("ZAVS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("ZAVS button");
    x.style.display = "none";
    var x = document.getElementById("ZAVS ime");
    x.style.display = "none";
    }


    try {
    if (PERS.getVisible()){
        var x = document.getElementById("PERS button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("PERS button");
    x.style.display = "none";
    var x = document.getElementById("PERS ime");
    x.style.display = "none";
    }


    try {
    if (BLY.getVisible()){
        var x = document.getElementById("BLY button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("BLY button");
    x.style.display = "none";
    var x = document.getElementById("BLY ime");
    x.style.display = "none";
    }


    try {
    if (ABAH.getVisible()){
        var x = document.getElementById("ABAH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("ABAH button");
    x.style.display = "none";
    var x = document.getElementById("ABAH ime");
    x.style.display = "none";
    }


    try {
    if (AMBH.getVisible()){
        var x = document.getElementById("AMBH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("AMBH button");
    x.style.display = "none";
    var x = document.getElementById("AMBH ime");
    x.style.display = "none";
    }


    try {
    if (BEHE.getVisible()){
        var x = document.getElementById("BEHE button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("BEHE button");
    x.style.display = "none";
    var x = document.getElementById("BEHE ime");
    x.style.display = "none";
    }


    try {
    if (BSZH.getVisible()){
        var x = document.getElementById("BSZH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("BSZH button");
    x.style.display = "none";
    var x = document.getElementById("BSZH ime");
    x.style.display = "none";
    }


    try {
    if (BUD.getVisible()){
        var x = document.getElementById("BUD button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("BUD button");
    x.style.display = "none";
    var x = document.getElementById("BUD ime");
    x.style.display = "none";
    }


    try {
    if (CSKK.getVisible()){
        var x = document.getElementById("CSKK button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("CSKK button");
    x.style.display = "none";
    var x = document.getElementById("CSKK ime");
    x.style.display = "none";
    }


    try {
    if (EGYH.getVisible()){
        var x = document.getElementById("EGYH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("EGYH button");
    x.style.display = "none";
    var x = document.getElementById("EGYH ime");
    x.style.display = "none";
    }


    try {
    if (KOVH.getVisible()){
        var x = document.getElementById("KOVH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("KOVH button");
    x.style.display = "none";
    var x = document.getElementById("KOVH ime");
    x.style.display = "none";
    }


    try {
    if (LTVH.getVisible()){
        var x = document.getElementById("LTVH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("LTVH button");
    x.style.display = "none";
    var x = document.getElementById("LTVH ime");
    x.style.display = "none";
    }


    try {
    if (MPLH.getVisible()){
        var x = document.getElementById("MPLH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("MPLH button");
    x.style.display = "none";
    var x = document.getElementById("MPLH ime");
    x.style.display = "none";
    }


    try {
    if (MORH.getVisible()){
        var x = document.getElementById("MORH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("MORH button");
    x.style.display = "none";
    var x = document.getElementById("MORH ime");
    x.style.display = "none";
    }


    try {
    if (PSZ.getVisible()){
        var x = document.getElementById("PSZ button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("PSZ button");
    x.style.display = "none";
    var x = document.getElementById("PSZ ime");
    x.style.display = "none";
    }


    try {
    if (SOP.getVisible()){
        var x = document.getElementById("SOP button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("SOP button");
    x.style.display = "none";
    var x = document.getElementById("SOP ime");
    x.style.display = "none";
    }


    try {
    if (TRPA.getVisible()){
        var x = document.getElementById("TRPA button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("TRPA button");
    x.style.display = "none";
    var x = document.getElementById("TRPA ime");
    x.style.display = "none";
    }


    try {
    if (TIH.getVisible()){
        var x = document.getElementById("TIH button");
        x.checked = true;
    }                          
    }
    catch(err) {
    var x = document.getElementById("TIH button");
    x.style.display = "none";
    var x = document.getElementById("TIH ime");
    x.style.display = "none";
    }
    }
    var mag = """+str(mags[i])+""";
    var br = """+str(len(eq[i]))+""";
    var eqmags = """+str(eq_mags[i])+""";
    function FRGSf() {
        if(FRGS.getVisible()){
        FRGS.setVisible(false);
        mag = ((mag*br)-eqmags["FRGS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        FRGS.setVisible(true);
        mag = ((mag*br)+eqmags["FRGS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function ZAGf() {
        if(ZAG.getVisible()){
        ZAG.setVisible(false);
        mag = ((mag*br)-eqmags["ZAG"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        ZAG.setVisible(true);
        mag = ((mag*br)+eqmags["ZAG"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function BEOf() {
        if(BEO.getVisible()){
        BEO.setVisible(false);
        mag = ((mag*br)-eqmags["BEO"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        BEO.setVisible(true);
        mag = ((mag*br)+eqmags["BEO"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function GROSf() {
        if(GROS.getVisible()){
        GROS.setVisible(false);
        mag = ((mag*br)-eqmags["GROS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        GROS.setVisible(true);
        mag = ((mag*br)+eqmags["GROS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function BOJSf() {
        if(BOJS.getVisible()){
        BOJS.setVisible(false);
        mag = ((mag*br)-eqmags["BOJS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        BOJS.setVisible(true);
        mag = ((mag*br)+eqmags["BOJS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function CADSf() {
        if(CADS.getVisible()){
        CADS.setVisible(false);
        mag = ((mag*br)-eqmags["CADS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        CADS.setVisible(true);
        mag = ((mag*br)+eqmags["CADS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function CEYf() {
        if(CEY.getVisible()){
        CEY.setVisible(false);
        mag = ((mag*br)-eqmags["CEY"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        CEY.setVisible(true);
        mag = ((mag*br)+eqmags["CEY"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function CRESf() {
        if(CRES.getVisible()){
        CRES.setVisible(false);
        mag = ((mag*br)-eqmags["CRES"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        CRES.setVisible(true);
        mag = ((mag*br)+eqmags["CRES"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function CRNSf() {
        if(CRNS.getVisible()){
        CRNS.setVisible(false);
        mag = ((mag*br)-eqmags["CRNS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        CRNS.setVisible(true);
        mag = ((mag*br)+eqmags["CRNS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function DOBSf() {
        if(DOBS.getVisible()){
        DOBS.setVisible(false);
        mag = ((mag*br)-eqmags["DOBS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        DOBS.setVisible(true);
        mag = ((mag*br)+eqmags["DOBS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function GOLSf() {
        if(GOLS.getVisible()){
        GOLS.setVisible(false);
        mag = ((mag*br)-eqmags["GOLS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        GOLS.setVisible(true);
        mag = ((mag*br)+eqmags["GOLS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function GORSf() {
        if(GORS.getVisible()){
        GORS.setVisible(false);
        mag = ((mag*br)-eqmags["GORS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        GORS.setVisible(true);
        mag = ((mag*br)+eqmags["GORS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function GBASf() {
        if(GBAS.getVisible()){
        GBAS.setVisible(false);
        mag = ((mag*br)-eqmags["GBAS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        GBAS.setVisible(true);
        mag = ((mag*br)+eqmags["GBAS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function GBRSf() {
        if(GBRS.getVisible()){
        GBRS.setVisible(false);
        mag = ((mag*br)-eqmags["GBRS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        GBRS.setVisible(true);
        mag = ((mag*br)+eqmags["GBRS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function GCISf() {
        if(GCIS.getVisible()){
        GCIS.setVisible(false);
        mag = ((mag*br)-eqmags["GCIS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        GCIS.setVisible(true);
        mag = ((mag*br)+eqmags["GCIS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function JAVSf() {
        if(JAVS.getVisible()){
        JAVS.setVisible(false);
        mag = ((mag*br)-eqmags["JAVS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        JAVS.setVisible(true);
        mag = ((mag*br)+eqmags["JAVS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function KNDSf() {
        if(KNDS.getVisible()){
        KNDS.setVisible(false);
        mag = ((mag*br)-eqmags["KNDS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        KNDS.setVisible(true);
        mag = ((mag*br)+eqmags["KNDS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function KOGSf() {
        if(KOGS.getVisible()){
        KOGS.setVisible(false);
        mag = ((mag*br)-eqmags["KOGS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        KOGS.setVisible(true);
        mag = ((mag*br)+eqmags["KOGS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function LJUf() {
        if(LJU.getVisible()){
        LJU.setVisible(false);
        mag = ((mag*br)-eqmags["LJU"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        LJU.setVisible(true);
        mag = ((mag*br)+eqmags["LJU"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function MOZSf() {
        if(MOZS.getVisible()){
        MOZS.setVisible(false);
        mag = ((mag*br)-eqmags["MOZS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        MOZS.setVisible(true);
        mag = ((mag*br)+eqmags["MOZS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function PDKSf() {
        if(PDKS.getVisible()){
        PDKS.setVisible(false);
        mag = ((mag*br)-eqmags["PDKS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        PDKS.setVisible(true);
        mag = ((mag*br)+eqmags["PDKS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function ROBSf() {
        if(ROBS.getVisible()){
        ROBS.setVisible(false);
        mag = ((mag*br)-eqmags["ROBS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        ROBS.setVisible(true);
        mag = ((mag*br)+eqmags["ROBS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function SKDSf() {
        if(SKDS.getVisible()){
        SKDS.setVisible(false);
        mag = ((mag*br)-eqmags["SKDS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        SKDS.setVisible(true);
        mag = ((mag*br)+eqmags["SKDS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function VISSf() {
        if(VISS.getVisible()){
        VISS.setVisible(false);
        mag = ((mag*br)-eqmags["VISS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        VISS.setVisible(true);
        mag = ((mag*br)+eqmags["VISS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function VOJSf() {
        if(VOJS.getVisible()){
        VOJS.setVisible(false);
        mag = ((mag*br)-eqmags["VOJS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        VOJS.setVisible(true);
        mag = ((mag*br)+eqmags["VOJS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function VNDSf() {
        if(VNDS.getVisible()){
        VNDS.setVisible(false);
        mag = ((mag*br)-eqmags["VNDS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        VNDS.setVisible(true);
        mag = ((mag*br)+eqmags["VNDS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function ZAVSf() {
        if(ZAVS.getVisible()){
        ZAVS.setVisible(false);
        mag = ((mag*br)-eqmags["ZAVS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        ZAVS.setVisible(true);
        mag = ((mag*br)+eqmags["ZAVS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function PERSf() {
        if(PERS.getVisible()){
        PERS.setVisible(false);
        mag = ((mag*br)-eqmags["PERS"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        PERS.setVisible(true);
        mag = ((mag*br)+eqmags["PERS"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function BLYf() {
        if(BLY.getVisible()){
        BLY.setVisible(false);
        mag = ((mag*br)-eqmags["BLY"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        BLY.setVisible(true);
        mag = ((mag*br)+eqmags["BLY"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function ABAHf() {
        if(ABAH.getVisible()){
        ABAH.setVisible(false);
        mag = ((mag*br)-eqmags["ABAH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        ABAH.setVisible(true);
        mag = ((mag*br)+eqmags["ABAH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function AMBHf() {
        if(AMBH.getVisible()){
        AMBH.setVisible(false);
        mag = ((mag*br)-eqmags["AMBH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        AMBH.setVisible(true);
        mag = ((mag*br)+eqmags["AMBH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function BEHEf() {
        if(BEHE.getVisible()){
        BEHE.setVisible(false);
        mag = ((mag*br)-eqmags["BEHE"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        BEHE.setVisible(true);
        mag = ((mag*br)+eqmags["BEHE"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function BSZHf() {
        if(BSZH.getVisible()){
        BSZH.setVisible(false);
        mag = ((mag*br)-eqmags["BSZH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        BSZH.setVisible(true);
        mag = ((mag*br)+eqmags["BSZH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function BUDf() {
        if(BUD.getVisible()){
        BUD.setVisible(false);
        mag = ((mag*br)-eqmags["BUD"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        BUD.setVisible(true);
        mag = ((mag*br)+eqmags["BUD"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function CSKKf() {
        if(CSKK.getVisible()){
        CSKK.setVisible(false);
        mag = ((mag*br)-eqmags["CSKK"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        CSKK.setVisible(true);
        mag = ((mag*br)+eqmags["CSKK"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function EGYHf() {
        if(EGYH.getVisible()){
        EGYH.setVisible(false);
        mag = ((mag*br)-eqmags["EGYH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        EGYH.setVisible(true);
        mag = ((mag*br)+eqmags["EGYH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function KOVHf() {
        if(KOVH.getVisible()){
        KOVH.setVisible(false);
        mag = ((mag*br)-eqmags["KOVH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        KOVH.setVisible(true);
        mag = ((mag*br)+eqmags["KOVH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function LTVHf() {
        if(LTVH.getVisible()){
        LTVH.setVisible(false);
        mag = ((mag*br)-eqmags["LTVH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        LTVH.setVisible(true);
        mag = ((mag*br)+eqmags["LTVH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function MPLHf() {
        if(MPLH.getVisible()){
        MPLH.setVisible(false);
        mag = ((mag*br)-eqmags["MPLH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        MPLH.setVisible(true);
        mag = ((mag*br)+eqmags["MPLH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function MORHf() {
        if(MORH.getVisible()){
        MORH.setVisible(false);
        mag = ((mag*br)-eqmags["MORH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        MORH.setVisible(true);
        mag = ((mag*br)+eqmags["MORH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function PSZf() {
        if(PSZ.getVisible()){
        PSZ.setVisible(false);
        mag = ((mag*br)-eqmags["PSZ"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        PSZ.setVisible(true);
        mag = ((mag*br)+eqmags["PSZ"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function SOPf() {
        if(SOP.getVisible()){
        SOP.setVisible(false);
        mag = ((mag*br)-eqmags["SOP"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        SOP.setVisible(true);
        mag = ((mag*br)+eqmags["SOP"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function TRPAf() {
        if(TRPA.getVisible()){
        TRPA.setVisible(false);
        mag = ((mag*br)-eqmags["TRPA"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        TRPA.setVisible(true);
        mag = ((mag*br)+eqmags["TRPA"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }
    }


    function TIHf() {
        if(TIH.getVisible()){
        TIH.setVisible(false);
        mag = ((mag*br)-eqmags["TIH"])/(br-1)
        document.querySelector('.content .value').innerHTML = mag;
        }
        else{
        TIH.setVisible(true);
        mag = ((mag*br)+eqmags["TIH"])/(br+1)
        document.querySelector('.content .value').innerHTML = mag;
        }

    """)
            for j in range(len(contents)):
                if "</head>" in contents[j]:
                    index = j
            contents.insert(j-4, """
    <div>
    <input name="FRGS" onclick="FRGSf()" type="checkbox" id="FRGS button">
    <label for="FRGS" id="FRGS ime">FRGS</label></div><div>
    <input name="ZAG" onclick="ZAGf()" type="checkbox" id="ZAG button">
    <label for="ZAG" id="ZAG ime">ZAG</label></div><div>
    <input name="BEO" onclick="BEOf()" type="checkbox" id="BEO button">
    <label for="BEO" id="BEO ime">BEO</label></div><div>
    <input name="GROS" onclick="GROSf()" type="checkbox" id="GROS button">
    <label for="GROS" id="GROS ime">GROS</label></div><div>
    <input name="BOJS" onclick="BOJSf()" type="checkbox" id="BOJS button">
    <label for="BOJS" id="BOJS ime">BOJS</label></div><div>
    <input name="CADS" onclick="CADSf()" type="checkbox" id="CADS button">
    <label for="CADS" id="CADS ime">CADS</label></div><div>
    <input name="CEY" onclick="CEYf()" type="checkbox" id="CEY button">
    <label for="CEY" id="CEY ime">CEY</label></div><div>
    <input name="CRES" onclick="CRESf()" type="checkbox" id="CRES button">
    <label for="CRES" id="CRES ime">CRES</label></div><div>
    <input name="CRNS" onclick="CRNSf()" type="checkbox" id="CRNS button">
    <label for="CRNS" id="CRNS ime">CRNS</label></div><div>
    <input name="DOBS" onclick="DOBSf()" type="checkbox" id="DOBS button">
    <label for="DOBS" id="DOBS ime">DOBS</label></div><div>
    <input name="GOLS" onclick="GOLSf()" type="checkbox" id="GOLS button">
    <label for="GOLS" id="GOLS ime">GOLS</label></div><div>
    <input name="GORS" onclick="GORSf()" type="checkbox" id="GORS button">
    <label for="GORS" id="GORS ime">GORS</label></div><div>
    <input name="GBAS" onclick="GBASf()" type="checkbox" id="GBAS button">
    <label for="GBAS" id="GBAS ime">GBAS</label></div><div>
    <input name="GBRS" onclick="GBRSf()" type="checkbox" id="GBRS button">
    <label for="GBRS" id="GBRS ime">GBRS</label></div><div>
    <input name="GCIS" onclick="GCISf()" type="checkbox" id="GCIS button">
    <label for="GCIS" id="GCIS ime">GCIS</label></div><div>
    <input name="JAVS" onclick="JAVSf()" type="checkbox" id="JAVS button">
    <label for="JAVS" id="JAVS ime">JAVS</label></div><div>
    <input name="KNDS" onclick="KNDSf()" type="checkbox" id="KNDS button">
    <label for="KNDS" id="KNDS ime">KNDS</label></div><div>
    <input name="KOGS" onclick="KOGSf()" type="checkbox" id="KOGS button">
    <label for="KOGS" id="KOGS ime">KOGS</label></div><div>
    <input name="LJU" onclick="LJUf()" type="checkbox" id="LJU button">
    <label for="LJU" id="LJU ime">LJU</label></div><div>
    <input name="MOZS" onclick="MOZSf()" type="checkbox" id="MOZS button">
    <label for="MOZS" id="MOZS ime">MOZS</label></div><div>
    <input name="PDKS" onclick="PDKSf()" type="checkbox" id="PDKS button">
    <label for="PDKS" id="PDKS ime">PDKS</label></div><div>
    <input name="ROBS" onclick="ROBSf()" type="checkbox" id="ROBS button">
    <label for="ROBS" id="ROBS ime">ROBS</label></div><div>
    <input name="SKDS" onclick="SKDSf()" type="checkbox" id="SKDS button">
    <label for="SKDS" id="SKDS ime">SKDS</label></div><div>
    <input name="VISS" onclick="VISSf()" type="checkbox" id="VISS button">
    <label for="VISS" id="VISS ime">VISS</label></div><div>
    <input name="VOJS" onclick="VOJSf()" type="checkbox" id="VOJS button">
    <label for="VOJS" id="VOJS ime">VOJS</label></div><div>
    <input name="VNDS" onclick="VNDSf()" type="checkbox" id="VNDS button">
    <label for="VNDS" id="VNDS ime">VNDS</label></div><div>
    <input name="ZAVS" onclick="ZAVSf()" type="checkbox" id="ZAVS button">
    <label for="ZAVS" id="ZAVS ime">ZAVS</label></div><div>
    <input name="PERS" onclick="PERSf()" type="checkbox" id="PERS button">
    <label for="PERS" id="PERS ime">PERS</label></div><div>
    <input name="BLY" onclick="BLYf()" type="checkbox" id="BLY button">
    <label for="BLY" id="BLY ime">BLY</label></div><div>
    <input name="ABAH" onclick="ABAHf()" type="checkbox" id="ABAH button">
    <label for="ABAH" id="ABAH ime">ABAH</label></div><div>
    <input name="AMBH" onclick="AMBHf()" type="checkbox" id="AMBH button">
    <label for="AMBH" id="AMBH ime">AMBH</label></div><div>
    <input name="BEHE" onclick="BEHEf()" type="checkbox" id="BEHE button">
    <label for="BEHE" id="BEHE ime">BEHE</label></div><div>
    <input name="BSZH" onclick="BSZHf()" type="checkbox" id="BSZH button">
    <label for="BSZH" id="BSZH ime">BSZH</label></div><div>
    <input name="BUD" onclick="BUDf()" type="checkbox" id="BUD button">
    <label for="BUD" id="BUD ime">BUD</label></div><div>
    <input name="CSKK" onclick="CSKKf()" type="checkbox" id="CSKK button">
    <label for="CSKK" id="CSKK ime">CSKK</label></div><div>
    <input name="EGYH" onclick="EGYHf()" type="checkbox" id="EGYH button">
    <label for="EGYH" id="EGYH ime">EGYH</label></div><div>
    <input name="KOVH" onclick="KOVHf()" type="checkbox" id="KOVH button">
    <label for="KOVH" id="KOVH ime">KOVH</label></div><div>
    <input name="LTVH" onclick="LTVHf()" type="checkbox" id="LTVH button">
    <label for="LTVH" id="LTVH ime">LTVH</label></div><div>
    <input name="MPLH" onclick="MPLHf()" type="checkbox" id="MPLH button">
    <label for="MPLH" id="MPLH ime">MPLH</label></div><div>
    <input name="MORH" onclick="MORHf()" type="checkbox" id="MORH button">
    <label for="MORH" id="MORH ime">MORH</label></div><div>
    <input name="PSZ" onclick="PSZf()" type="checkbox" id="PSZ button">
    <label for="PSZ" id="PSZ ime">PSZ</label></div><div>
    <input name="SOP" onclick="SOPf()" type="checkbox" id="SOP button">
    <label for="SOP" id="SOP ime">SOP</label></div><div>
    <input name="TRPA" onclick="TRPAf()" type="checkbox" id="TRPA button">
    <label for="TRPA" id="TRPA ime">TRPA</label></div><div>
    <input name="TIH" onclick="TIHf()" type="checkbox" id="TIH button">
    <label for="TIH" id="TIH ime">TIH</label></div>
    <div class="content">Magnituda: <span class='value'></span></div>
    <script type ="text/javascript">
        what();
        function what(){
            document.querySelector('.content .value').innerHTML = mag;
        };
    </script>
    """)
            f = open(b, "w")
            contents = "".join(contents)
            f.write(contents)
            f.close()
            #print(eq[i])
            if (len(eq)>=1 and round(mags[i], 2)>=3.50 and not bio):
                try:
                    response = client.chat_postMessage(channel="U01JCRMUM7U", text="================================")
                except:
                    pass
            if round(mags[i], 2)>=3.50:
                try:
                    ime = "map"+a+".html"
                    response = client.chat_postMessage(channel="U01JCRMUM7U", text='*POTRES*\nVRIJEME: '+datetime.utcfromtimestamp(int(eq[i][0][3])+3600).strftime('%d/%m/%Y %H:%M:%S')+'\nMAGNITUDA: '+str(round(mags[i], 2)))
                    response = client.files_upload(channels="U01JCRMUM7U", file=ime, title="POTRES.html")
                except:
                    pass
    except Exception as e:
        print(e)
    print("--- %s seconds ---" % (time.time() - start_time))
