import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
# MKYLisans Tarafından oluşturulmuş kodtur Emeğe Saygı Lütfen
class YklemeEkrani_MKYLisans:
    def __init__(self, parent):
        self.parent = parent
        self.yukleme_penceresi = tk.Toplevel(parent)
        self.yukleme_penceresi.title("Yükleniyor")
        self.yukleme_penceresi.geometry("500x500")
        self.yukleme_penceresi.resizable(False, False)

        self.yukleme_etiketi = ttk.Label(self.yukleme_penceresi, text="Yükleniyor...")
        self.yukleme_etiketi.pack(pady=20)

        self.resim_etiketi = ttk.Label(self.yukleme_penceresi)
        self.resim_etiketi.pack()

        self.parent.after(2000, self.kapat)  # Örnek olarak 2000 milisaniye (2 saniye) sonra pencereyi kapat

    def kapat(self):
        self.yukleme_penceresi.destroy()

class ResimBoyutlandirici_MKYLisans:
    def __init__(self, root):
        self.root = root
        self.root.title("MKYLisans Resim Boyutlandırıcı")

        self.resim = None
        self.etiket = tk.Label(root)
        self.etiket.pack()

        self.buton = tk.Button(root, text="Resim Seç", command=self.resim_sec)
        self.buton.pack()

        self.boyut_options = ["1024x768", "2545x600", "1900x1028"]
        self.boyut_menusu = tk.StringVar()
        self.boyut_menusu.set(self.boyut_options[0])

        boyut_menu = tk.OptionMenu(root, self.boyut_menusu, *self.boyut_options)
        boyut_menu.pack()

        self.genislik_entry = tk.Entry(root, width=100)
        self.genislik_entry.pack()

        self.yukseklik_entry = tk.Entry(root, width=100)
        self.yukseklik_entry.pack()

        self.kaydet_buton = tk.Button(root, text="Kaydet", state="disabled", command=self.resmi_kaydet)
        self.kaydet_buton.pack()

    def resim_sec(self):
        dosya_yolu = filedialog.askopenfilename(filetypes=[("Resim Dosyaları", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if dosya_yolu:
            self.yukleme_ekrani_MKYLisans = YklemeEkrani_MKYLisans(self.root)  # Yükleme ekranını burada oluştur
            self.root.update()  # Ekranı güncelle
            self.resim = cv2.imread(dosya_yolu)
            self.boyutlandir_resim()
            self.kaydet_buton.config(state="normal")
            self.yukleme_ekrani_MKYLisans.kapat()  # Yükleme ekranını kapat

    def boyutlandir_resim(self):
        genislik = self.genislik_entry.get()
        yukseklik = self.yukseklik_entry.get()

        if not genislik:
            genislik = 0
        else:
            genislik = int(genislik)

        if not yukseklik:
            yukseklik = 0
        else:
            yukseklik = int(yukseklik)

        if self.resim is not None and genislik > 0 and yukseklik > 0:
            orijinal_genislik, orijinal_yukseklik, _ = self.resim.shape
            olcek_faktoru = min(genislik / orijinal_genislik, yukseklik / orijinal_yukseklik)

            yeni_genislik = int(orijinal_genislik * olcek_faktoru)
            yeni_yukseklik = int(orijinal_yukseklik * olcek_faktoru)

            self.resim = cv2.resize(self.resim, (yeni_genislik, yeni_yukseklik))
            self.goruntule(self.resim)

    def goruntule(self, resim):
        tk_resim = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)))
        self.etiket.config(image=tk_resim)
        self.etiket.image = tk_resim

    def resmi_kaydet(self):
        if self.resim is not None:
            boyut_secimi = self.boyut_menusu.get()
            self.kaydet_resmi(boyut_secimi)

    def kaydet_resmi(self, boyut_secimi):
        if self.resim is not None:
            kaydet_yolu = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                           filetypes=[("JPEG Dosyaları", "*.jpg"),
                                                                      ("PNG Dosyaları", "*.png"),
                                                                      ("GIF Dosyaları", "*.gif"),
                                                                      ("BMP Dosyaları", "*.bmp")])
            if kaydet_yolu:
                orijinal_genislik, orijinal_yukseklik, _ = self.resim.shape
                boyutlar = boyut_secimi.split("x")
                hedef_genislik = int(boyutlar[0])
                hedef_yukseklik = int(boyutlar[1])

                olcek_faktoru = min(hedef_genislik / orijinal_genislik, hedef_yukseklik / orijinal_yukseklik)
                yeni_genislik = int(orijinal_genislik * olcek_faktoru)
                yeni_yukseklik = int(orijinal_yukseklik * olcek_faktoru)

                kaydet_resim = cv2.resize(self.resim,
                                          (int(boyut_secimi.split("x")[0]), int(boyut_secimi.split("x")[1])))
                cv2.imwrite(kaydet_yolu, kaydet_resim)

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = ResimBoyutlandirici_MKYLisans(root)

    boyutlandirma_butonu = tk.Button(root, text="Boyutlandır", command=uygulama.boyutlandir_resim)
    boyutlandirma_butonu.pack()

    root.mainloop()
