#!/usr/bin/env python
# coding: utf-8

# In[1]:


def download1(sts, t1, timeinmin):
    from obspy.clients.fdsn import Client
    client = Client("GFZ")
    try:
        print("SJ-FRGS")
        st = client.get_waveforms("SJ", "FRGS", "*", "*", t1-60*timeinmin, t1, attach_response=True)
        sts["FRGS"] = st
        st.write('./downloads_mseeds/FRGS/SJ.FRGS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\FRGS.png')
    except Exception as e:
        print(e)
    try:
        print("SJ-BEO")
        st = client.get_waveforms("SJ", "BEO", "*", "*", t1-60*timeinmin, t1, attach_response=True)
        sts["BEO"] = st
        st.write('./downloads_mseeds/BEO/SJ.BEO.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\BEO.png')
    except Exception as e:
        print(e)
    client = Client("ORFEUS")
    try:
        print("SL-GORS")
        st = client.get_waveforms("SL", "GORS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["GORS"] = st
        st.write('./downloads_mseeds/GORS/SL.GORS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\GORS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-GBAS")
        st = client.get_waveforms("SL", "GBAS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["GBAS"] = st
        st.write('./downloads_mseeds/GBAS/SL.GBAS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\GBAS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-GBRS")
        st = client.get_waveforms("SL", "GBRS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["GBRS"] = st
        st.write('./downloads_mseeds/GBRS/SL.GBRS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\GBRS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-GCIS")
        st = client.get_waveforms("SL", "GCIS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["GCIS"] = st
        st.write('./downloads_mseeds/GCIS/SL.GCIS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\GCIS.png') 
    except Exception as e:
        print(e)
    try:
        print("CR-ZAG")
        st = client.get_waveforms("CR", "ZAG", "*", "*", t1-60*timeinmin, t1, attach_response=True)
        sts["ZAG"] = st
        st.write('./downloads_mseeds/ZAG/CR.ZAG.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\ZAG.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-GROS")
        st = client.get_waveforms("SL", "GROS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["GROS"] = st
        st.write('./downloads_mseeds/GROS/SL.GROS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\GROS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-BOJS")
        st = client.get_waveforms("SL", "BOJS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["BOJS"] = st
        st.write('./downloads_mseeds/BOJS/SL.BOJS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\BOJS.png') 
    except Exception as e:
        print(e)
    try:
        print("HU-MPLH")
        st = client.get_waveforms("HU", "MPLH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["MPLH"] = st
        st.write('./downloads_mseeds/MPLH/HU.MPLH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\MPLH.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-MORH")
        st = client.get_waveforms("HU", "MORH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["MORH"] = st
        st.write('./downloads_mseeds/MORH/HU.MORH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\MORH.png') 
    except Exception as e:
        print(e)
    return sts
def download2(sts, t1, timeinmin):
    from obspy.clients.fdsn import Client
    client = Client("GFZ")
    try:
        print("HU-PSZ")
        st = client.get_waveforms("HU", "PSZ", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["PSZ"] = st
        st.write('./downloads_mseeds/PSZ/HU.PSZ.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\PSZ.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-SOP")
        st = client.get_waveforms("HU", "SOP", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["SOP"] = st
        st.write('./downloads_mseeds/SOP/HU.SOP.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\SOP.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-TRPA")
        st = client.get_waveforms("HU", "TRPA", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["TRPA"] = st
        st.write('./downloads_mseeds/TRPA/HU.TRPA.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\TRPA.png') 
    except Exception as e:
        print(e)
    try:
        print("HU-TIH")
        st = client.get_waveforms("HU", "TIH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["TIH"] = st
        st.write('./downloads_mseeds/TIH/HU.TIH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\TIH.png') 
    except Exception as e:
        print(e)
    client = Client("ORFEUS")
    try:
        print("SL-JAVS")
        st = client.get_waveforms("SL", "JAVS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["JAVS"] = st
        st.write('./downloads_mseeds/JAVS/SL.JAVS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\JAVS.png')
    except Exception as e:
        print(e)

    try:
        print("SL-KNDS")
        st = client.get_waveforms("SL", "KNDS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["KNDS"] = st
        st.write('./downloads_mseeds/KNDS/SL.KNDS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\KNDS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-KOGS")
        st = client.get_waveforms("SL", "KOGS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["KOGS"] = st
        st.write('./downloads_mseeds/KOGS/SL.KOGS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\KOGS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-LJU")
        st = client.get_waveforms("SL", "LJU", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["LJU"] = st
        st.write('./downloads_mseeds/LJU/SL.LJU.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\LJU.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-MOZS")
        st = client.get_waveforms("SL", "MOZS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["MOZS"] = st
        st.write('./downloads_mseeds/MOZS/SL.MOZS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\MOZS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-PDKS")
        st = client.get_waveforms("SL", "PDKS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["PDKS"] = st
        st.write('./downloads_mseeds/PDKS/SL.PDKS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\PDKS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-ROBS")
        st = client.get_waveforms("SL", "ROBS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["ROBS"] = st
        st.write('./downloads_mseeds/ROBS/SL.ROBS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\ROBS.png') 
    except Exception as e:
        print(e)
    return sts
def download3(sts, t1, timeinmin):
    from obspy.clients.fdsn import Client
    client = Client("ORFEUS")
    try:
        print("SL-SKDS")
        st = client.get_waveforms("SL", "SKDS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["SKDS"] = st
        st.write('./downloads_mseeds/SKDS/SL.SKDS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\SKDS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-VISS")
        st = client.get_waveforms("SL", "VISS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["VISS"] = st
        st.write('./downloads_mseeds/VISS/SL.VISS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\VISS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-VOJS")
        st = client.get_waveforms("SL", "VOJS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["VOJS"] = st
        st.write('./downloads_mseeds/VOJS/SL.VOJS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\VOJS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-VNDS")
        st = client.get_waveforms("SL", "VNDS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["VNDS"] = st
        st.write('./downloads_mseeds/VNDS/SL.VNDS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\VNDS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-ZAVS")
        st = client.get_waveforms("SL", "ZAVS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["ZAVS"] = st
        st.write('./downloads_mseeds/ZAVS/SL.ZAVS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\ZAVS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-PERS")
        st = client.get_waveforms("SL", "PERS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["PERS"] = st
        st.write('./downloads_mseeds/PERS/SL.PERS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\PERS.png')
    except Exception as e:
        print(e)

    client = Client("INGV")

    try:
        print("MN-BLY")
        st = client.get_waveforms("MN", "BLY", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["BLY"] = st
        st.write('./downloads_mseeds/BLY/MN.BLY.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\BLY.png') 
    except Exception as e:
        print(e)

    client = Client("GFZ")

    try:
        print("HU-ABAH")
        st = client.get_waveforms("HU", "ABAH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["ABAH"] = st
        st.write('./downloads_mseeds/ABAH/HU.ABAH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\ABAH.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-AMBH")
        st = client.get_waveforms("HU", "AMBH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["AMBH"] = st
        st.write('./downloads_mseeds/AMBH/HU.AMBH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\AMBH.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-BEHE")
        st = client.get_waveforms("HU", "BEHE", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["BEHE"] = st
        st.write('./downloads_mseeds/BEHE/HU.BEHE.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\BEHE.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-BSZH")
        st = client.get_waveforms("HU", "BSZH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["BSZH"] = st
        st.write('./downloads_mseeds/BSZH/HU.BSZH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\BSZH.png') 
    except Exception as e:
        print(e)
    return sts
def download4(sts, t1, timeinmin):
    from obspy.clients.fdsn import Client
    client = Client("ORFEUS")
    try:
        print("SL-CADS")
        st = client.get_waveforms("SL", "CADS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["CADS"] = st
        st.write('./downloads_mseeds/CADS/SL.CADS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\CADS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-CEY")
        st = client.get_waveforms("SL", "CEY", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["CEY"] = st
        st.write('./downloads_mseeds/CEY/SL.CEY.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\CEY.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-CRES")
        st = client.get_waveforms("SL", "CRES", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["CRES"] = st
        st.write('./downloads_mseeds/CRES/SL.CRES.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\CRES.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-CRNS")
        st = client.get_waveforms("SL", "CRNS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["CRNS"] = st
        st.write('./downloads_mseeds/CRNS/SL.CRNS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\CRNS.png') 
    except Exception as e:
        print(e)  

    try:
        print("SL-DOBS")
        st = client.get_waveforms("SL", "DOBS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["DOBS"] = st
        st.write('./downloads_mseeds/DOBS/SL.DOBS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\DOBS.png') 
    except Exception as e:
        print(e)

    try:
        print("SL-GOLS")
        st = client.get_waveforms("SL", "GOLS", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["GOLS"] = st
        st.write('./downloads_mseeds/GOLS/SL.GOLS.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\GOLS.png') 
    except Exception as e:
        print(e)
    client = Client("GFZ")
    try:
        print("HU-BUD")
        st = client.get_waveforms("HU", "BUD", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["BUD"] = st
        st.write('./downloads_mseeds/BUD/HU.BUD.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\BUD.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-CSKK")
        st = client.get_waveforms("HU", "CSKK", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["CSKK"] = st
        st.write('./downloads_mseeds/CSKK/HU.CSKK.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\CSKK.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-EGYH")
        st = client.get_waveforms("HU", "EGYH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["EGYH"] = st
        st.write('./downloads_mseeds/EGYH/HU.EGYH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\EGYH.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-KOVH")
        st = client.get_waveforms("HU", "KOVH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["KOVH"] = st
        st.write('./downloads_mseeds/KOVH/HU.KOVH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\KOVH.png') 
    except Exception as e:
        print(e)

    try:
        print("HU-LTVH")
        st = client.get_waveforms("HU", "LTVH", "*", "HH*", t1-60*timeinmin, t1, attach_response=True)
        sts["LTVH"] = st
        st.write('./downloads_mseeds/LTVH/HU.LTVH.00.00__20210104T065030000Z__20210104T065530000Z.mseed', format='MSEED'); #st.plot(outfile='.\pics\LTVH.png') 
    except Exception as e:
        print(e)
    return sts


# In[ ]:
#from obspy import UTCDateTime
#from datetime import datetime, timedelta
#download1({}, UTCDateTime((datetime.utcnow() - timedelta(seconds=45)).strftime('%Y-%m-%dT%H:%M:%S.%f')), 15)
#download2({}, UTCDateTime((datetime.utcnow() - timedelta(seconds=45)).strftime('%Y-%m-%dT%H:%M:%S.%f')), 15)
#download3({}, UTCDateTime((datetime.utcnow() - timedelta(seconds=45)).strftime('%Y-%m-%dT%H:%M:%S.%f')), 15)
#download4({}, UTCDateTime((datetime.utcnow() - timedelta(seconds=45)).strftime('%Y-%m-%dT%H:%M:%S.%f')), 15)

