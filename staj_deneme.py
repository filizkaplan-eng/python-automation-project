# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 22:36:53 2020

@author: Lenovo
"""


import pyodbc
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import sqlalchemy as sa
import urllib.parse
import sys
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)



CONNECTION_STRING = r'Driver={SQL Server};Server=DESKTOP-DUGGE5O\SQLEXPRESS;Database=sap_projem;Trusted_Connection=yes;'
engine = sa.create_engine('mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(CONNECTION_STRING))
conn=engine.connect()
metadata=sa.MetaData()
emp = sa.Table('yonetim_sureci', metadata, autoload=True, autoload_with=engine)
emp1=sa.Table('yonetici',metadata, autoload=True, autoload_with=engine)
emp2=sa.Table('kullanici',metadata, autoload=True, autoload_with=engine)
results = conn.execute(sa.select([emp])).fetchall()




db = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-DUGGE5O\SQLEXPRESS;'
    'Database=sap_projem;'
    'Trusted_Connection=true;'
)
cursor=db.cursor()
df=pd.read_sql('''select * from yonetim_sureci''',db)
dfk=pd.read_sql('''select * from kullanici ''',db)
dfy=pd.read_sql('''select * from yonetici''',db)
dataf=pd.DataFrame(df)
df['proje_adi']=df['proje_adi'].astype('str')
df['butce_verim']=df['butce_verim'].astype('int')
df['sure_verim']=df['sure_verim'].astype('int')
df['proje_id']=df['proje_id'].astype('str')

class pandasModel(QAbstractTableModel):
    #veritabanındaki verileri tabloya aktarma
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data #dışarıdan alınan tablo yani data _data değşkenine atanır

    def rowCount(self, parent=None): #Bu satırda parenttan bahsettik yani ebeveyn. 
        #Program alt pencerelerden oluşmaya başladığında, hangi pencerenin hangi 
        #pencereye ait alt pencere olduğunu ayırt etmek için bu yapı kullanılır. 
        #Biz bu pencerenin bir alt pencere olmadığını, bizim penceremizin bir ana
        #pencere olduğunu parent=None ifadesiyle belirttik.
        return self._data.shape[0]#satır sayısı

    def columnCount(self, parnet=None):
        return self._data.shape[1]#sütun sayıaı

    def data(self, index, role=Qt.DisplayRole):
        # Qt.DisplayRole=  Metin şeklinde işlenecek anahtar veriler.
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):#Qabstracttablemodel in alt fonksiyonu
        #HeaderData () fonksiyonu görüntüler tablonun başlığı(orientation), adı(role) ve adresi(col) . 
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # Qt.Horizontal = Yönlendirme(Orientation), örneğin QScrollBar ile kullanılır.
            # qt.horizontal sütun başlıkları için kullanılır.
            # Qt.DisplayRole=  Metin şeklinde işlenecek anahtar veriler.
            return self._data.columns[col]
        return None

df_k=pd.read_sql('''select * from yonetim_sureci where kullanici=1''',db)
df_y=pd.read_sql('''select * from yonetim_sureci where yonetici=13''',db)

class Pencere2(QMainWindow):
    #kayıt penceresi
    def __init__(self):
        super().__init__()
        self.set_ui()
        
        
    def set_ui(self):
        main_window=self.KytPencere()
        self.setStyleSheet(open("stil_dnm.qss","r").read())
        self.setWindowTitle("Kayıt Penceresi")
        self.setCentralWidget(main_window)
        self.setMaximumSize(QSize(700,700))
        self.setMinimumSize(QSize(500,500))
        
        
    def KytPencere(self):
        #kayıt pencere
        wid1=QWidget()
        
        vbox=QVBoxLayout()
        
        img2=QLabel()
        img2.setPixmap(QPixmap("kyt.png"))
        img2.setAlignment(Qt.AlignHCenter)
        self.secim=""
        statü=QLabel("Nasıl kaydolmak istediğinizi seçiniz")
        self.cb=QComboBox()
        self.cb.addItem("Seçiniz")
        self.cb.addItem("Yönetici")
        self.cb.addItem("Kullanıcı")
        self.cb.currentIndexChanged.connect(self.tikla)
        posta=QLabel("E-Posta Adresi")
        self.kyt_posta=QLineEdit()
        kyt=QLabel("Yönetici/Kullanıcı Adı")
        passw=QLabel("Şifre")
        self.kyt_name=QLineEdit()
        self.kyt_psw=QLineEdit()
        kyt_btn= QPushButton("Kayıt Ol")
        kyt_btn.clicked.connect(self.kayit_ol)
        self.yazialani=QLabel()
        
        vbox.addStretch()
        vbox.addWidget(img2)
        vbox.addStretch()
        vbox.addWidget(posta)
        vbox.addWidget(self.kyt_posta)
        vbox.addWidget(kyt)
        vbox.addWidget(self.kyt_name)
        vbox.addWidget(passw)
        vbox.addWidget(self.kyt_psw)
        vbox.addWidget(statü)
        vbox.addWidget(self.cb)
        vbox.addWidget(self.yazialani)
        vbox.addStretch()
        vbox.addWidget(kyt_btn)
        vbox.addStretch()
        vbox.addStretch()
        
        hbox=QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()
        
        wid1.setLayout(hbox)
        
        return wid1
    
    
    def tikla(self):
        self.secim=self.cb.currentText()
        print(self.secim)
    def kayit_ol(self):
        ad=self.kyt_name.text()
        sifre=self.kyt_psw.text()
        post=self.kyt_posta.text()
        if self.secim=="Yönetici":
            srg=sa.insert(emp1).values(yonetici_ad=ad,sifre=sifre,posta=post)
            conn.execute(srg)
            self.yazialani.setText("Yönetici kaydınız yapılmıştır.")
        elif self.secim=="Kullanıcı":
            srg=sa.insert(emp2).values(kullanici_ad=ad,sifre=sifre,posta=post)
            conn.execute(srg)
            self.yazialani.setText("Kullanıcı kaydınız yapılmıştır.")
        else:
            self.yazialani.setText(self.secim)



class Pencere3(QMainWindow):
    #yönetici girişi penceresi
    def __init__(self):
        super().__init__()
        self.setui()
        
        
    def setui(self):
        mainWindow=self.YntcPencere()
        self.setStyleSheet(open("stil_dnm.qss","r").read())
        self.setWindowTitle("Yönetici Girişi")
        self.setCentralWidget(mainWindow)
        self.setMaximumSize(QSize(700,700))
        self.setMinimumSize(QSize(500,500))
        self.mang_win=Terminal()
        
        
    def YntcPencere(self):
        wid=QWidget()
        
        vBox=QVBoxLayout()
        
        img1=QLabel()
        img1.setPixmap(QPixmap("yntc.png"))
        img1.setAlignment(Qt.AlignHCenter)
        
        mang=QLabel("Yönetici Adı")
        pswrd=QLabel("Şifre")
        self.mang_name=QLineEdit()
        self.mang_psw=QLineEdit()
        self.mang_psw.setEchoMode(QLineEdit.Password)
        mang_btn= QPushButton("Giriş")
        self.yazi_alan=QLabel()
        mang_btn.clicked.connect(self.grs_mang)
        
        vBox.addStretch()
        vBox.addWidget(img1)
        vBox.addStretch()
        vBox.addWidget(mang)
        vBox.addWidget(self.mang_name)
        vBox.addWidget(pswrd)
        vBox.addWidget(self.mang_psw)
        vBox.addWidget(self.yazi_alan)
        vBox.addStretch()
        vBox.addWidget(mang_btn)
        vBox.addStretch()
        vBox.addStretch()
        hBox=QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()
        wid.setLayout(hBox)
        
        return wid
    def grs_mang(self):
        self.adi=self.mang_name.text()
        self.sifre=self.mang_psw.text()
        
        a=cursor.execute("select yntc_id from yonetici where yonetici_ad=? and sifre=? ",(self.adi,self.sifre))
        
        dfmng=pd.DataFrame(a)
        dfid=dfmng.iloc[0,0]
        self.id_mng=int(dfid[0])
        
        cursor.execute("select * from yonetici where yonetici_ad=? and sifre=?",(self.adi,self.sifre))
        kontrol=cursor.fetchall()
        
        if len(kontrol)==0:
            self.yazi_alan.setText("Yönetici adı veya şifre hatalı lütfen tekrar deneyin.")
            
        else:
            self.hide()
            self.mang_win.show()
    
    
    
    


class Terminal(QDialog):
    def __init__(self, parent=None):
            super(Terminal, self).__init__(parent)
            self.resize(1300,700)
            self.figure = plt.figure(facecolor='black')
            self.initUI()
            
#This was creating a canvas which I was adding my widget to (bad idea)
    def initUI(self):
            
            layout = QVBoxLayout()
            self.xMplWidget1 = MatplotlibWidgett1()
            self.xMplWidget2 = MatplotlibWidgett2()
            
            
            
            
            
            dataf=pd.DataFrame(df_y)
            model = pandasModel(dataf)
            view = QTableView()
            view.setModel(model)
            view.resize(900,5000)
            
            #baş
            ana_grup=QGroupBox()
            ana_grup.setMaximumHeight(400)
            grup=QGroupBox()
            gr_layout=QVBoxLayout(grup)
            
            updt_btn=QPushButton("Guncelle")
            #updt_btn.clicked.connect(self.pro_up)
            updt_sec=QPushButton("Seciniz")
            #updt_sec.clicked.connect(self.up_sec)
            dlte_btn=QPushButton("Sil")
            #dlte_btn.clicked.connect(self.sil)
            insrt_btn=QPushButton("Ekle")
            #insrt_btn.clicked.connect(self.ekle)
            mang_updt=QPushButton("Guncelle")
            #mang_updt.clicked.connect(self.mang_up)
            
            lbl= QLabel("PROJE GUNCELLEME")
            lbl_0=QLabel("proje adi")
            lbl_1= QLabel("Güncellemek istediğiniz proje id'sini seciniz")
            lbl_2= QLabel("Tahmini Butçe")
            lbl_3= QLabel("Tamamlanan proje(Yuzde cinsinden)")
            lbl_4= QLabel("Harcanan Butçe")
            lbl_5= QLabel("Harcanan Sure(sure)")
            lbl_6= QLabel("Tahmini(Beklenen) Sure")
            
            lbl1= QLabel("PROJE SİLME")
            lbl1_1= QLabel("Silmek istediğiniz proje id'sini seciniz")
            
            lbl2= QLabel("PROJE EKLEME")
            lbl2_1= QLabel("Eklemek istediğiniz proje adı")
            lbl2_2= QLabel("Proje tahmini bütçe")
            lbl2_3= QLabel("Projenin tamamlanma yüzdesi")
            lbl2_4= QLabel("Projede harcanan bütçe")
            lbl2_5= QLabel("Projede harcanan süre")
            lbl2_6= QLabel("Projede beklenen süre")
            lbl2_7=QLabel("eklemek istediğiniz kullanıcının id'si")
            
            updt_pro=QLineEdit()#değiştirilecek proje id
            delt_pro=QLineEdit()#silinecek proje
            #self.delt_protx=delt_pro.text()
            
            updt_1=QLineEdit("Değistirilecek proje")
            updt_0=QLineEdit("Değistirilecek proje adı")
            updt_2=QLineEdit("Yeni tahmin butce")
            updt_3=QLineEdit("Yeni tamamlanan proje")
            updt_4=QLineEdit("Yeni harcanan bütce")
            updt_5=QLineEdit("Yeni harcanan sure")
            updt_6=QLineEdit("Yeni tahmin sure")
            
            insert_ad=QLineEdit() #eklenecek proje adı
            #self.insert_adtx=insert_ad.text()
            insert_tahBut=QLineEdit()#tahmin bütçe
            #self.insert_tahbuttx=insert_tahBut.text()
            insert_tamam=QLineEdit()#tamamlanan proje yüzde cinsinden
            #self.insert_tamamtx=insert_tamam.text()
            insert_harcBut=QLineEdit()#harcanan bütçe
            #self.insert_harcButtx=insert_harcBut.text()
            insert_sure=QLineEdit()#harcanan  süre
            #self.insert_suretx=insert_sure.text()
            insert_bekSure=QLineEdit()#beklenen süre
            #self.insert_beksuretx=insert_bekSure.text()
            insert_usr=QLineEdit()
            #self.insert_usrtx=insert_ad.text()
            
            
            mng=QLabel("BİLGİ GUNCELLEME")
            mng_1=QLabel("Yonetici adınız")
            mng_2=QLabel("posta")
            mng_3=QLabel("sifre")
            
            mng_ad=QLineEdit("yeni ad")
            mng_posta=QLineEdit("yeni posta")
            mng_sfr=QLineEdit("yeni sifre")
            
            gr_layout.addWidget(lbl)
            gr_layout.addWidget(lbl_1)
            gr_layout.addWidget(updt_1)
            gr_layout.addWidget(updt_sec)
            gr_layout.addWidget(lbl_0)
            gr_layout.addWidget(updt_0)
            gr_layout.addWidget(lbl_2)
            gr_layout.addWidget(updt_2)
            gr_layout.addWidget(lbl_3)
            gr_layout.addWidget(updt_3)
            gr_layout.addWidget(lbl_4)
            gr_layout.addWidget(updt_4)
            gr_layout.addWidget(lbl_5)
            gr_layout.addWidget(updt_5)
            gr_layout.addWidget(lbl_6)
            gr_layout.addWidget(updt_6)
            gr_layout.addWidget(updt_btn)
            gr_layout.addStretch()
            gr_layout.addWidget(lbl1)
            gr_layout.addWidget(lbl1_1)
            gr_layout.addWidget(delt_pro)
            gr_layout.addWidget(dlte_btn)
            gr_layout.addStretch()
            gr_layout.addWidget(lbl2)
            gr_layout.addWidget(lbl2_1)
            gr_layout.addWidget(insert_ad)
            gr_layout.addWidget(lbl2_2)
            gr_layout.addWidget(insert_tahBut)
            gr_layout.addWidget(lbl2_3)
            gr_layout.addWidget(insert_tamam)
            gr_layout.addWidget(lbl2_4)
            gr_layout.addWidget(insert_harcBut)
            gr_layout.addWidget(lbl2_5)
            gr_layout.addWidget(insert_sure)
            gr_layout.addWidget(lbl2_6)
            gr_layout.addWidget(insert_bekSure)
            gr_layout.addWidget(lbl2_7)
            gr_layout.addWidget(insert_usr)
            gr_layout.addWidget(insrt_btn)
            gr_layout.addWidget(mng)
            gr_layout.addWidget(mng_1)
            gr_layout.addWidget(mng_ad)
            gr_layout.addWidget(mng_2)
            gr_layout.addWidget(mng_posta)
            gr_layout.addWidget(mng_3)
            gr_layout.addWidget(mng_sfr)
            gr_layout.addWidget(mang_updt)
            gr_layout.addStretch()
            
            
            
            scrollarea = QScrollArea()
            scrollarea.setFixedWidth(450)
            scrollarea.setWidgetResizable(True)
            
            grup_wid=QWidget()
            scrollarea.setWidget(grup_wid)
            layout_sarea=QVBoxLayout(grup_wid)
            layout_sarea.addWidget(grup)
            
            
            
            
            widget=QWidget()
            widget.setMaximumHeight(500)
            ly= QVBoxLayout()
            ly.addWidget(view)
            widget.setLayout(ly)
            plt_grup=QGroupBox()
            plt_lay=QHBoxLayout(plt_grup)
            plt_lay.addWidget(self.xMplWidget1)
            plt_lay.addWidget(self.xMplWidget2)
            plt_grup.setLayout(plt_lay)
            
            lay_deneme=QHBoxLayout()
            lay_deneme.addWidget(plt_grup)
            #lay_deneme.addStretch()
            lay_deneme.addWidget(scrollarea)
            ana_grup.setLayout(lay_deneme)
            
            layout.addWidget(widget)
            layout.addWidget(ana_grup)
            self.setLayout(layout)
            
            
     def ekle(self):
        ekle_lst=[self.insert_ad.text(),self.insert_tahBut.text(),self.insert_tamam.text(),self.insert_harcBut.text(),self.insert_sure.text(),self.insert_bekSure.text(), self.insert_usr]
        dat=pd.DataFrame(ekle_lst)
        ekleme=sa.insert(emp)
        insert_adtx=dat.iloc[0,0]
        insert_tahbuttx=int(dat.iloc[1,0])
        insert_tamamtx=int(dat.iloc[2,0])
        insert_harcButtx=int(dat.iloc[3,0])
        insert_suretx=int(dat.iloc[4,0])
        insert_beksuretx=int(dat.iloc[5,0])
        insert_usrtx=float(dat.iloc[6,0])
        values_lst=[{'proje_adi':insert_adtx,'tahmin_butce':insert_tahbuttx ,'tamamlanan':insert_tamamtx ,'harcanan':insert_harcButtx,'sure':insert_suretx,'beklenen':insert_beksuretx,'yonetici':id_mng,'kullanici':insert_usrtx}]
        son=conn.execute(ekleme,values_lst)
        pass
    def sil(self):
        dlt=[self.delt_pro.text()]
        data=pd.DataFrame(dlt)
        delt_protx=float(data.iloc[0,0])
        silme=sa.delete(emp)
        silme=silme.where(emp.columns.proje_id==delt_protx)
        son=conn.execute(silme)
        pass
    def up_sec(self):
        pro_id=[self.updt_4.text()]
        dt=pd.DataFrame(pro_id)
        id_pro=float(dt.iloc[0,0])
        a=cursor.execute("select proje_adi,tahmin_butce,tamamlanan,harcanan,sure,beklenen from kullanici where yonetici=? and proje_id=? ",(self.id_mng,id_pro))
        yeni_text=pd.DataFrame(a)
        self.updt_0.setText(a.iloc[0,0])
        self.updt_2.setText(a.iloc[1,0])
        self.updt_3.setText(a.iloc[2,0])
        self.updt_4.setText(a.iloc[3,0])
        self.updt_5.setText(a.iloc[4,0])
        self.updt_6.setText(a.iloc[5,0])
    def pro_up(self):
        lst_up=[self.updt_1.text(), self.updt_2.text(),self.updt_3.text(),self.updt_4.text(),self.updt_5.text(),self.updt_6.text()]
        data=pd.DataFrame(lst_up)
        pro_id=float(data.iloc[0,0])
        pro_ad=self.updt_0.text()
        tah_bt=int(data.iloc[1,0])
        tamam=int(data.iloc[2,0])
        harc_bt=int(data.iloc[3,0])
        harc_sr=int(data.iloc[4,0])
        tah_sr=int(data.iloc[5,0])
        y_id=self.id_mng
        
        sorgu = sa.update(emp).values(proje_adi = pro_ad , tahmin_butce = tah_bt , tamamlanan = tamam , harcanan = harc_bt , sure = harc_sr , beklenen = tah_sr)
        sorgu=sorgu.where(emp.columns.proje_id==pro_id, emp.columns.yonetici==y_id)
        conn.execute(sorgu)  
        
    def mang_up(self):
        ad= self.adi
        sifre=self.sifre
        y_id=self.id_mng
        
        sorgu = sa.update(emp1).values(yonetici_ad = ad , sifre=us_sfr , posta = us_post )
        sorgu=sorgu.where(emp1.columns.yntc_id==y_id)
        conn.execute(sorgu) 


    


class MatplotlibWidget1(FigureCanvas):
    def __init__(self, parent=None, title='Title', dpi=100, hold=False):
        
        super(MatplotlibWidget1, self).__init__(Figure())       
        self.setParent(parent)
        self.figure = Figure(dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        
        ax=self.figure.add_subplot(111)
        colors=['orange','#3bdd00','#d90d2b','purple', '#209adf']

        labels = ax.get_xticklabels()
        plt.setp(labels, rotation = 45, horizontalalignment = 'right')                       #proje isimlerinin üst üste gelmesini engeller

        ax.bar(df_k.proje_id,df_k.sure_verim, color=colors)                                      #biz belirlemediğimiz sürece rengi otomatik kendisi verir. 
        ax.set_title("SURE VERIM")
        
        
class MatplotlibWidget2(FigureCanvas):
    def __init__(self, parent=None, title='Title', dpi=100, hold=False):
        
        super(MatplotlibWidget2, self).__init__(Figure())       
        self.setParent(parent)
        self.figure = Figure(dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        
        ax=self.figure.add_subplot(111)
    
        colors=['orange','green','#d90d2b','purple', 'black']

        labels = ax.get_xticklabels()
        plt.setp(labels, rotation = 45, horizontalalignment = 'right')#proje isimlerinin üst üste gelmesini engeller
        
        ax.bar(df_k.proje_id,df_k.butce_verim, color=colors) #biz belirlemediğimiz sürece rengi otomatik kendisi verir. 
        
        ax.set_title("BUTCE VERIM")
        
        
    

class MatplotlibWidgett1(FigureCanvas):
    def __init__(self, parent=None, title='Title', dpi=100, hold=False):
        
        super(MatplotlibWidgett1, self).__init__(Figure())       
        self.setParent(parent)
        self.figure = Figure(dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        
        ax=self.figure.add_subplot(111)
        colors=['orange','#3bdd00','#d90d2b','purple', '#209adf']

        labels = ax.get_xticklabels()
        plt.setp(labels, rotation = 45, horizontalalignment = 'right')                       #proje isimlerinin üst üste gelmesini engeller

        ax.bar(df_y.proje_id,df_y.sure_verim, color=colors)                                      #biz belirlemediğimiz sürece rengi otomatik kendisi verir. 
        ax.set_title("SURE VERIM")
        
        
class MatplotlibWidgett2(FigureCanvas):
    def __init__(self, parent=None, title='Title', dpi=100, hold=False):
        
        super(MatplotlibWidgett2, self).__init__(Figure())       
        self.setParent(parent)
        self.figure = Figure(dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        
        ax=self.figure.add_subplot(111)
    
        colors=['orange','green','#d90d2b','purple', 'black']

        labels = ax.get_xticklabels()
        plt.setp(labels, rotation = 45, horizontalalignment = 'right')#proje isimlerinin üst üste gelmesini engeller
        
        ax.bar(df_y.proje_id,df_y.butce_verim, color=colors) #biz belirlemediğimiz sürece rengi otomatik kendisi verir. 
        
        ax.set_title("BUTCE VERIM")
        
        
    




class Terminall(QDialog):
    def __init__(self, parent=None):
            super(Terminall, self).__init__(parent)
            self.resize(1300,700)
            #self.figure = plt.figure(facecolor='black')
            self.initUI()
            
#This was creating a canvas which I was adding my widget to (bad idea)
    def initUI(self):
            
            layout = QVBoxLayout()
            self.xMplWidget1 = MatplotlibWidget1()
            self.xMplWidget2 = MatplotlibWidget2()
            
            
            
            db = pyodbc.connect(
                    'Driver={SQL Server};'
                    'Server=DESKTOP-DUGGE5O\SQLEXPRESS;'
                    'Database=sap_projem;'
                    'Trusted_Connection=true;'
                )
                
            
            dataf=pd.DataFrame(df_k)
            model = pandasModel(dataf)
            view = QTableView()
            view.setModel(model)
            view.resize(900,5000)
            
            #baş
            ana_grup=QGroupBox()
            ana_grup.setMaximumHeight(400)
            grup=QGroupBox()
            gr_layout=QVBoxLayout(grup)
            
            updt_btn=QPushButton("Guncelle")
            updt_btn.clicked.connect(self.pro_up)
            updt_sec=QPushButton("Seciniz")
            updt_sec.clicked.connect(self.up_sec)
            usr_upt=QPushButton("Guncelle")
            usr_upt.clicked.connect(self.usr_up)
           
            lbl= QLabel("PROJE GUNCELLEME")
            lbl_0=QLabel("Proje adi")
            lbl_1= QLabel("Güncellemek istediğiniz proje id'sini seciniz")
            lbl_2= QLabel("Tahmini Butçe")
            lbl_3= QLabel("Tamamlanan proje(Yuzde cinsinden)")
            lbl_4= QLabel("Harcanan Butçe")
            lbl_5= QLabel("Harcanan Sure(sure)")
            lbl_6= QLabel("Tahmini(Beklenen) Sure")
            
            
            
            
            updt_pro=QLineEdit()#değiştirilecek proje id
            updt_1=QLineEdit("Değistirilecek proje")
            updt_0=QLineEdit("Değistirilecek proje adi")
            updt_2=QLineEdit("Yeni tahmin butce")
            updt_3=QLineEdit("Yeni tamamlanan proje")
            updt_4=QLineEdit("Yeni harcanan bütce")
            updt_5=QLineEdit("Yeni harcanan sure")
            updt_6=QLineEdit("Yeni tahmin sure")
            
            usr=QLabel("BİLGİ GUNCELLEME")
            usr_1=QLabel("Kullanici adınız")
            usr_2=QLabel("posta")
            usr_3=QLabel("sifre")
            
            usr_ad=QLineEdit("yeni ad")
            usr_posta=QLineEdit("yeni posta")
            usr_sfr=QLineEdit("yeni sifre")
            
            gr_layout.addWidget(lbl)
            gr_layout.addWidget(lbl_1)
            gr_layout.addWidget(updt_1)
            gr_layout.addWidget(updt_sec)
            gr_layout.addWidget(lbl_0)
            gr_layout.addWidget(updt_0)
            gr_layout.addWidget(lbl_2)
            gr_layout.addWidget(updt_2)
            gr_layout.addWidget(lbl_3)
            gr_layout.addWidget(updt_3)
            gr_layout.addWidget(lbl_4)
            gr_layout.addWidget(updt_4)
            gr_layout.addWidget(lbl_5)
            gr_layout.addWidget(updt_5)
            gr_layout.addWidget(lbl_6)
            gr_layout.addWidget(updt_6)
            gr_layout.addWidget(updt_btn)
            gr_layout.addWidget(usr)
            gr_layout.addWidget(usr_1)
            gr_layout.addWidget(usr_ad)
            gr_layout.addWidget(usr_2)
            gr_layout.addWidget(usr_posta)
            gr_layout.addWidget(usr_3)
            gr_layout.addWidget(usr_sfr)
            gr_layout.addWidget(usr_upt)
            gr_layout.addStretch()
            
            gr_layout.addStretch()
            
            
            
            scrollarea = QScrollArea()
            scrollarea.setFixedWidth(500)
            scrollarea.setWidgetResizable(True)
            
            grup_wid=QWidget()
            scrollarea.setWidget(grup_wid)
            layout_sarea=QVBoxLayout(grup_wid)
            layout_sarea.addWidget(grup)
            
            
            
            
            widget=QWidget()
            widget.setMaximumHeight(500)
            ly= QVBoxLayout()
            ly.addWidget(view)
            widget.setLayout(ly)
 ########################################           
            plt_grup=QGroupBox()
            plt_lay=QHBoxLayout()
            plt_lay.addWidget(self.xMplWidget1)
            plt_lay.addWidget(self.xMplWidget2)
            plt_grup.setLayout(plt_lay)
##################################################3            
            lay_deneme=QHBoxLayout()
            lay_deneme.addWidget(plt_grup)
            #lay_deneme.addStretch()
            lay_deneme.addWidget(scrollarea)
            ana_grup.setLayout(lay_deneme)
            
            layout.addWidget(widget)
            layout.addWidget(ana_grup)
            self.setLayout(layout)
            
    
    def up_sec(self):
        pro_id=[self.updt_4.text()]
        dt=pd.DataFrame(pro_id)
        id_pro=float(dt.iloc[0,0])
        a=cursor.execute("select proje_adi,tahmin_butce,tamamlanan,harcanan,sure,beklenen from kullanici where kullanici=? and proje_id=? ",(self.id_us,id_pro))
        yeni_text=pd.DataFrame(a)
        self.updt_0.setText(a.iloc[0,0])
        self.updt_2.setText(a.iloc[1,0])
        self.updt_3.setText(a.iloc[2,0])
        self.updt_4.setText(a.iloc[3,0])
        self.updt_5.setText(a.iloc[4,0])
        self.updt_6.setText(a.iloc[5,0])
    def pro_up(self):
        lst_up=[self.updt_1.text(), self.updt_2.text(),self.updt_3.text(),self.updt_4.text(),self.updt_5.text(),self.updt_6.text()]
        data=pd.DataFrame(lst_up)
        pro_id=float(data.iloc[0,0])
        pro_ad=self.updt_0.text()
        tah_bt=int(data.iloc[1,0])
        tamam=int(data.iloc[2,0])
        harc_bt=int(data.iloc[3,0])
        harc_sr=int(data.iloc[4,0])
        tah_sr=int(data.iloc[5,0])
        k_id=self.id_us
        
        sorgu = sa.update(emp).values(proje_adi = pro_ad , tahmin_butce = tah_bt , tamamlanan = tamam , harcanan = harc_bt , sure = harc_sr , beklenen = tah_sr)
        sorgu=sorgu.where(emp.columns.proje_id==pro_id, emp.columns.kullanici==k_id)
        conn.execute(sorgu)  
        
    def usr_up(self):
        
        ad=self.usr_ad.text()
        us_post= self.usr_posta.text()
        us_sfr= self.usr_sfr.text()
        k_id=self.id_us
        sorgu = sa.update(emp2).values(kullanici_ad = ad , sifre=us_sfr ,posta = us_post )
        sorgu=sorgu.where(emp2.columns.usr_id==k_id)
        conn.execute(sorgu) 
       







class Pencere1(QMainWindow):
    #kullanici girisi
    def __init__(self):
        super().__init__()
        self.setUii()
        
    def setUii(self):
        mainwindow=self.AnaPencere()
        self.setStyleSheet(open("stil_dnm.qss","r").read())
        self.setWindowTitle("Kullanıcı Girişi")
        self.setCentralWidget(mainwindow)
        self.setMaximumSize(QSize(700,700))
        self.setMinimumSize(QSize(500,500))
        self.secondWin=Pencere3()
        self.kyt_win=Pencere2()
        self.user_win=Terminall()
        self.show()
    def AnaPencere(self):
        widget=QWidget()
        v_box=QVBoxLayout()
        img=QLabel()
        img.setPixmap(QPixmap("grs.png"))
        img.setAlignment(Qt.AlignHCenter)
        user=QLabel("Kullanıcı Adı")
        psw=QLabel("Şifre")
        self.user_name=QLineEdit()
        self.user_psw=QLineEdit()
        self.user_psw.setEchoMode(QLineEdit.Password)
        ulgn_btn= QPushButton("Giriş")
        manager_btn=QPushButton("Yönetici girişi için tıklayın")
        record_btn= QPushButton("Kayıt Ol")
        self.yazi_alani=QLabel()
        
        ulgn_btn.clicked.connect(self.grs_user)
        manager_btn.clicked.connect(self.yontc)
        record_btn.clicked.connect(self.kyt)
        
        v_box.addStretch()
        v_box.addWidget(img)
        v_box.addStretch()
        v_box.addWidget(user)
        v_box.addWidget(self.user_name)
        v_box.addWidget(psw)
        v_box.addWidget(self.user_psw)
        v_box.addWidget(self.yazi_alani)
        v_box.addStretch()
        v_box.addWidget(ulgn_btn)
        v_box.addWidget(manager_btn)
        v_box.addWidget(record_btn)
        v_box.addStretch()
        v_box.addStretch()
        
        h_box=QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        
        widget.setLayout(h_box)
        return widget
    def grs_user(self):
        self.adi=self.user_name.text()
        self.sifre=self.user_psw.text()
        
        
        cursor.execute("select * from kullanici where kullanici_ad=? and sifre=?",(self.adi,self.sifre))
        kontrol=cursor.fetchall()
        
        if len(kontrol)==0:
            self.yazi_alani.setText("Kullanıcı adı veya şifre hatalı lütfen tekrar deneyin.")
            
        else:
            a=cursor.execute("select usr_id from kullanici where kullanici_ad=? and sifre=? ",(self.adi,self.sifre))
        
            dfusr=pd.DataFrame(a)
            dfid=dfusr.iloc[0,0]
            self.id_us=int(dfid[0])
            self.hide()
            self.user_win.show()
            
    def yontc(self):
        self.hide()
        self.secondWin.show()
    def kyt(self):
        self.hide()
        self.kyt_win.show()
if __name__=="__main__":
    
    app=QApplication(sys.argv)
    pencere=Pencere1()
    sys.exit(app.exec_())