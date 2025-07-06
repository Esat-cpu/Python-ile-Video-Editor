from tkinter import *
from os import listdir
from time import sleep
from threading import Thread
from edit import Edit
from plyer import notification as bildirim

win = Tk()
win.config(bg= "slategrey")
win.geometry("1000x720")
win.maxsize(1080, 800)
win.minsize(1000, 720)
win.title("Editor")



# Editleyen
edit = Edit()


# Dizindeki .mp3 ve .mp4 dosyalarını gösterir
def dizin():
    # dizin içindeki .mp3 ve .mp4 dosyalarını dizinici listesine kaydeder
    global dizinici
    while True:
        dizinici = [i+"\n" for i in listdir() if i.endswith(".mp4") or i.endswith(".mp3")]
        yazi = "Dizindeki ses ve videolar:\n\n"
        for i in dizinici: yazi+= i
        try: dizinyazi.destroy()
        except: pass
        dizinyazi = Label(win, text= yazi, width= 20)
        dizinyazi.grid(column=0, row= 0)
        sleep(3)


islem1 = Thread(target= dizin)
islem1.daemon = True
islem1.start()



# Arayüzde yazi gösteren fonksiyon
def mesaj(yer, yazi, buton:Button= ""):
    def f():
        a = Label(yer, text= yazi)
        a.place(anchor= CENTER, relx= .5, rely= .15)
        sleep(3.5)
        try: a.destroy()
        except: pass
        if buton:
            try: buton['state'] = "active"
            except: pass
        
    Thread(target= f, daemon= True).start()



# Kaydet tuşları için kontrol
kontrol = 1


# Canvas arayüzler

canvas = Canvas(width= 600, height= 380)
canvas.config(bg= "#add8e6")
canvas.place(anchor= CENTER, relx= 0.5, rely= 0.55)




# İki videoyu birleştirir
def birlestir():
    global canvas, fade1value, fade2value, Kaydet
    canvas.destroy()
    canvas = Canvas(width= 600, height= 380)
    canvas.config(bg= "#add8e6")
    canvas.place(anchor= CENTER, relx= 0.5, rely= 0.55)

    label1 = Label(canvas, text= "1. Video ismi:")
    label2 = Label(canvas, text= "2. Video ismi:")

    label1.place(anchor= CENTER, relx= 0.1, rely= 0.45)
    label2.place(anchor= CENTER, relx= 0.55, rely= 0.45)

    entry1 = Entry(canvas, width= 25)
    entry2 = Entry(canvas, width= 25)

    entry1.place(anchor= CENTER, relx= 0.3, rely= 0.45)
    entry2.place(anchor= CENTER, relx= 0.75, rely= 0.45)
    
    # Fade işlemleri
    fade1value = 0
    fade2value = 0
    def fade1func():
        global fade1value
        fade1value = 1 if fade1value == 0 else 0
        fade1['text'] = "1. videonun sonuna fade out ✔" if fade1['text'] == "1. videonun sonuna fade out ❌" else "1. videonun sonuna fade out ❌"
    def fade2func():
        global fade2value
        fade2value = 1 if fade2value == 0 else 0
        fade2['text'] = "2. videonun başına fade in ✔" if fade2['text'] == "2. videonun başına fade in ❌" else "2. videonun başına fade in ❌"
    fade1 = Button(canvas, text= "1. videonun sonuna fade out ❌", command= fade1func, width= 24)
    fade2 = Button(canvas, text= "2. videonun başına fade in ❌", command= fade2func, width= 24)
    
    fade1.place(anchor= CENTER, relx= 0.195, rely= 0.6)
    fade2.place(anchor= CENTER, relx= 0.195, rely= 0.7)

    # Kaydet tuşu
    def kaydet():
        Kaydet['state'] = "disabled"
        video1 = entry1.get()
        video2 = entry2.get()
        entry1.delete(0, END)
        entry2.delete(0, END)
        if video1: edit.clip0()
        try:
            edit.birlestir(video1, video2, fade1value, fade2value)
            mesaj(canvas, "Kaydedildi..", Kaydet)
        except NameError:
            mesaj(canvas, "Girilen video(lar) dizinde bulunamadı..", Kaydet)
        except:
            mesaj(canvas, "Bir hata oluştu..", Kaydet)
    Kaydet = Button(canvas, text= "Kaydet", width= 20, height=2, command= kaydet)
    Kaydet.place(anchor= CENTER, relx= 0.7, rely= 0.7)
    if not kontrol: Kaydet['state'] = "disabled"






# Bir videonun sesini girilen ses ile değiştirir
def sesekleme():
    global canvas, fade1value, fade2value, Kaydet
    canvas.destroy()
    canvas = Canvas(width= 600, height= 380)
    canvas.config(bg= "#add8e6")
    canvas.place(anchor= CENTER, relx= 0.5, rely= 0.55)

    label1 = Label(canvas, text= "Video ismi:")
    label2 = Label(canvas, text= "Ses ismi:")

    label1.place(anchor= CENTER, relx= 0.1, rely= 0.45)
    label2.place(anchor= CENTER, relx= 0.55, rely= 0.45)

    entry1 = Entry(canvas, width= 25)
    entry2 = Entry(canvas, width= 25)

    entry1.place(anchor= CENTER, relx= 0.3, rely= 0.45)
    entry2.place(anchor= CENTER, relx= 0.75, rely= 0.45)

    fade1value = 0
    fade2value = 0
    def fade1func():
        global fade1value
        fade1value = 1 if fade1value == 0 else 0
        fade1['text'] = "Sesin başına fade in ✔" if fade1['text'] == "Sesin başına fade in ❌" else "Sesin başına fade in ❌"
    def fade2func():
        global fade2value
        fade2value = 1 if fade2value == 0 else 0
        fade2['text'] = "Sesin sonuna fade out ✔" if fade2['text'] == "Sesin sonuna fade out ❌" else "Sesin sonuna fade out ❌"
    fade1 = Button(canvas, text= "Sesin başına fade in ❌", command= fade1func, width= 21)
    fade2 = Button(canvas, text= "Sesin sonuna fade out ❌", command= fade2func, width= 21)
    
    fade1.place(anchor= CENTER, relx= 0.195, rely= 0.6)
    fade2.place(anchor= CENTER, relx= 0.195, rely= 0.7)

    # Kaydet tuşu
    def kaydet():
        Kaydet['state'] = "disabled"
        video = entry1.get()
        ses = entry2.get()
        entry1.delete(0, END)
        entry2.delete(0, END)
        if video: edit.clip0()
        try:
            edit.sesekleme(video, ses, fade1value, fade2value)
            mesaj(canvas, "Kaydedildi..", Kaydet)
        except NameError:
            mesaj(canvas, "Girilen ses veya video dosyası dizinde bulunamadı..", Kaydet)
        except:
            mesaj(canvas, "Bir hata oluştu..", Kaydet)
    Kaydet = Button(canvas, text= "Kaydet", width= 20, height=2, command= kaydet)
    Kaydet.place(anchor= CENTER, relx= 0.7, rely= 0.7)
    if not kontrol: Kaydet['state'] = "disabled"






# Belirtilen saniye aralığını kaydeder
def kirp():
    global canvas, Kaydet
    canvas = Canvas(width= 600, height= 380)
    canvas.config(bg= "#add8e6")
    canvas.place(anchor= CENTER, relx= 0.5, rely= 0.55)

    label1 = Label(canvas, text= "Video ismi:")
    label2 = Label(canvas, text= "Saniye aralığı:")

    label1.place(anchor= CENTER, relx= 0.1, rely= 0.45)
    label2.place(anchor= CENTER, relx= 0.55, rely= 0.45)

    entry1 = Entry(canvas, width= 25)
    entry2 = Entry(canvas, width= 25)

    entry1.place(anchor= CENTER, relx= 0.3, rely= 0.45)
    entry2.place(anchor= CENTER, relx= 0.75, rely= 0.45)

    # Kaydet tuşu
    def kaydet():
        Kaydet['state'] = "disabled"
        video = entry1.get()
        aralik = entry2.get().split()
        entry1.delete(0, END)
        entry2.delete(0, END)
        try:
            aralik1 = aralik[0]
            aralik2 = aralik[1]
            if video: edit.clip0()
            try:
                edit.kirp(videoadi= video, zaman1= aralik1, zaman2= aralik2)
                mesaj(canvas, "Kaydedildi..", Kaydet)
            except NameError:
                mesaj(canvas, "Dizinde öyle bir dosya yok..", Kaydet)
            except:
                mesaj(canvas, "Bir hata oluştu..", Kaydet)
        except: mesaj(canvas, "Saniye aralığı yanlış girildi.. Örnek: '10 20'", Kaydet)
    Kaydet = Button(canvas, text= "Kaydet", width= 20, height=2, command= kaydet)
    Kaydet.place(anchor= CENTER, relx= 0.7, rely= 0.7)
    if not kontrol: Kaydet['state'] = "disabled"
    


BUTON1 = Button(text= "Video Birleştir", width= 20, command= birlestir)
BUTON2 = Button(text= "Ses Ekleme", width= 20, command= sesekleme)
BUTON3 = Button(text= "Kırpma", width= 20, command= kirp)
BUTON1.place(anchor= CENTER, relx= 0.9, rely= 0.2)
BUTON2.place(anchor= CENTER, relx= 0.9, rely= 0.24)
BUTON3.place(anchor= CENTER, relx= 0.9, rely= 0.28)



# Video yazdiran yer
videoadilabel = Label(text= "Oluşturulacak videonun adı:")
videoadilabel.place(anchor= CENTER, relx= 0.275, rely= 0.85)
videoadientry = Entry(width= 42)
videoadientry.place(anchor= CENTER, relx= 0.5, rely= 0.85)

def videoismi():
    asdf = videoadientry.get()
    videoadientry.delete(0, END)
    return asdf
def Yazdir():
    global kontrol
    kontrol = 0
    Kaydet['state'] = "disabled"
    edit.yazdir(videoismi())
    Kaydet['state'] = "active"
    kontrol = 1
    if bildirimler == 1: bildirim.notify("Edit başarılı", "Video Oluşturuldu.")

videoyazdir = Button(text= "Video Oluştur", width= 20, command= lambda: Thread(target= lambda: Yazdir(), daemon= True).start())
videoyazdir.place(anchor= CENTER, relx= 0.725, rely= 0.85)
videoyazdir['state'] = "disabled"





# clip kontroller
def kontroller():
    yazim = 0
    while True:
        if edit.clipsorgu():
            if not yazim:
                yazim = Label(win, text= "Kayıtlı Klip", width= 11)
                yazim.place(anchor= CENTER, relx= 0.24, rely= 0.266)
                sil = Button(win, text= "❌", command= edit.clip0)
                sil.place(anchor= CENTER, relx= 0.3, rely= 0.266)
            videoyazdir['state'] = "active"
        else:
            try: yazim.destroy(); sil.destroy(); yazim = 0
            except: pass
            videoyazdir['state'] = "disabled"
        sleep(.01)
Thread(target= kontroller, daemon= True).start()




# Bildirim ayarlarını yapan butonun fonksiyonu
bildirimler = 1
def bildirimTusFunc():
    global bildirimler
    bildirTus['text'] = "Bildirimleri aç" if bildirTus['text'] == "Bildirimleri kapat" else "Bildirimleri kapat"
    bildirimler = 1 if bildirimler == 0 else 0
    

bildirTus = Button(text= "Bildirimleri kapat", width= 14, command= bildirimTusFunc)
bildirTus.place(anchor= CENTER, relx= 0.9, rely= 0.9)



# Kapatma fonksiyonu ve Kapat butonu
def Kapat():
    win.protocol("WM_DELETE_WINDOW")
    win.destroy()

kapat = Button(text= "Çıkış", width= 14, command= Kapat)
kapat.place(anchor= CENTER, relx= .9, rely= .95)


win.mainloop()
