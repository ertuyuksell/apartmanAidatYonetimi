import tkinter as tk
from tkinter import messagebox


class Kisi:
    def __init__(self, ad, yas):
        self._ad = ad
        self._yas = yas

    def ad_al(self):
        return self._ad

    def ad_belirle(self, ad):
        self._ad = ad

    def yas_al(self):
        return self._yas

    def yas_belirle(self, yas):
        self._yas = yas

    def bilgi(self):
        return f"Ad: {self._ad}, yas: {self._yas}"


class Sakin(Kisi):
    def __init__(self, ad, yas, daire_numarasi, borc_miktari=0):
        super().__init__(ad, yas)
        self._daire_numarasi = daire_numarasi
        self._borc_miktari = borc_miktari
        self._odeme_gecmisi = []

    def daire_numarasi_al(self):
        return self._daire_numarasi

    def daire_numarasi_belirle(self, daire_numarasi):
        self._daire_numarasi = daire_numarasi

    def borc_ekle(self, miktar):
        self._borc_miktari += miktar

    def borc_ode(self, miktar):
        if miktar > self._borc_miktari:
            messagebox.showwarning("Uyarı", "Ödeme miktarı borç miktarından fazla olamaz.")
            return
        else:
            self._borc_miktari -= miktar
            self._odeme_gecmisi.append(miktar)

    def borc_miktari_al(self):
        return self._borc_miktari

    def odeme_gecmisi_al(self):
        return self._odeme_gecmisi

    def bilgi(self):
        return (f"Ad: {self._ad}, yas: {self._yas}, Daire Numarasi: {self._daire_numarasi}, "
                f"Borc Miktari: {self._borc_miktari}")


class Yonnetici(Kisi):
    def __init__(self, ad, yas, ofis_numarasi):
        super().__init__(ad, yas)
        self._ofis_numarasi = ofis_numarasi
        self._sakinler = []

    def ofis_numarasi_al(self):
        return self._ofis_numarasi

    def ofis_numarasi_belirle(self, ofis_numarasi):
        self._ofis_numarasi = ofis_numarasi

    def sakin_ekle(self, sakin):
        if isinstance(sakin, Sakin):
            self._sakinler.append(sakin)
        else:
            print("Sadece sakinler eklenebilir.")

    def sakinler_al(self):
        return self._sakinler

    def odemeleri_kontrol_et(self):
        for sakin in self._sakinler:
            print(sakin.bilgi())

    def bilgi(self):
        return f"Ad: {self._ad}, yas: {self._yas}, Ofis Numarasi: {self._ofis_numarasi}"


def form_olustur():
    yonetici = Yonnetici("Jane Smith", 40, "Ofis 1")

    def sakin_ekle():
        ad = entry_ad.get()
        yas = int(entry_yas.get())
        daire_numarasi = entry_daire_numarasi.get()
        borc_miktari = float(entry_borc_miktari.get())

        yeni_sakin = Sakin(ad, yas, daire_numarasi, borc_miktari)
        yonetici.sakin_ekle(yeni_sakin)
        messagebox.showinfo("Başarılı", f"{ad} isimli sakin başarıyla eklendi.")
        entry_ad.delete(0, tk.END)
        entry_yas.delete(0, tk.END)
        entry_daire_numarasi.delete(0, tk.END)
        entry_borc_miktari.delete(0, tk.END)

    def odeme_yap():
        secilen_sakin_index = listbox_sakinler.curselection()
        if not secilen_sakin_index:
            messagebox.showerror("Hata", "Lütfen bir sakin seçin.")
            return

        miktar = float(entry_odeme_miktari.get())
        secilen_sakin = yonetici.sakinler_al()[secilen_sakin_index[0]]

        if miktar > secilen_sakin.borc_miktari_al():
            messagebox.showwarning("Uyarı", "Ödeme miktarı borç miktarından fazla olamaz.")
            return

        secilen_sakin.borc_ode(miktar)
        messagebox.showinfo("Başarılı", f"{secilen_sakin.ad_al()} tarafından {miktar} ödeme yapıldı.")
        entry_odeme_miktari.delete(0, tk.END)
        odemeleri_kontrol_et()

    def odemeleri_kontrol_et():
        listbox_sakinler.delete(0, tk.END)
        for sakin in yonetici.sakinler_al():
            listbox_sakinler.insert(tk.END, sakin.bilgi())

    root = tk.Tk()
    root.title("Yönetici Formu")

    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    tk.Label(frame, text="Sakinin Adı:").grid(row=0, column=0)
    entry_ad = tk.Entry(frame)
    entry_ad.grid(row=0, column=1)

    tk.Label(frame, text="Sakinin Yaşı:").grid(row=1, column=0)
    entry_yas = tk.Entry(frame)
    entry_yas.grid(row=1, column=1)

    tk.Label(frame, text="Daire Numarası:").grid(row=2, column=0)
    entry_daire_numarasi = tk.Entry(frame)
    entry_daire_numarasi.grid(row=2, column=1)

    tk.Label(frame, text="Borç Miktarı:").grid(row=3, column=0)
    entry_borc_miktari = tk.Entry(frame)
    entry_borc_miktari.grid(row=3, column=1)

    tk.Button(frame, text="Sakin Ekle", command=sakin_ekle).grid(row=4, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Ödeme Miktarı:").grid(row=5, column=0)
    entry_odeme_miktari = tk.Entry(frame)
    entry_odeme_miktari.grid(row=5, column=1)

    tk.Button(frame, text="Ödeme Yap", command=odeme_yap).grid(row=6, column=0, columnspan=2, pady=10)

    listbox_sakinler = tk.Listbox(frame, width=100)
    listbox_sakinler.grid(row=7, column=0, columnspan=2, pady=10)

    tk.Button(frame, text="Ödemeleri Kontrol Et", command=odemeleri_kontrol_et).grid(row=8, column=0, columnspan=2,
                                                                                     pady=10)

    root.mainloop()


if __name__ == "__main__":
    form_olustur()