import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import asyncio
import edge_tts
import threading


def seslendirme_islemi(metin, ses_kodu, kayit_yeri):
    async def amele_kod():
        communicate = edge_tts.Communicate(metin, ses_kodu)
        await communicate.save(kayit_yeri)

    try:
        
        asyncio.run(amele_kod())
        
        messagebox.showinfo("Başarılı", f"Dosya başarıyla kaydedildi:\n{kayit_yeri}")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu:\n{str(e)}")
    finally:
        
        btn_cevir.config(state="normal", text="MP3'e Dönüştür ve Kaydet")


def baslat():
    metin = txt_alan.get("1.0", tk.END).strip()
    
    if len(metin) < 1:
        messagebox.showwarning("Uyarı", "Lütfen seslendirilecek bir metin girin!")
        return

    
    dosya_yolu = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 Dosyası", "*.mp3")],
        title="MP3 Olarak Kaydet"
    )

    if not dosya_yolu:
        return 

    
    secim = cinsiyet_var.get()
    if secim == "Erkek":
        ses = "tr-TR-AhmetNeural"
    else:
        ses = "tr-TR-EmelNeural"

    
    btn_cevir.config(state="disabled", text="İşleniyor, lütfen bekleyin...")
    
    
    t = threading.Thread(target=seslendirme_islemi, args=(metin, ses, dosya_yolu))
    t.start()


pencere = tk.Tk()
pencere.title("Metin Seslendirme Aracı (TTS)")
pencere.geometry("500x500")


lbl_baslik = tk.Label(pencere, text="Metni Aşağıya Yapıştırın", font=("Arial", 12, "bold"))
lbl_baslik.pack(pady=10)


txt_alan = scrolledtext.ScrolledText(pencere, width=50, height=15, font=("Arial", 10))
txt_alan.pack(padx=10, pady=5)


cinsiyet_var = tk.StringVar(value="Kadın") # Varsayılan
frame_ayar = tk.Frame(pencere)
frame_ayar.pack(pady=10)

rb_kadin = tk.Radiobutton(frame_ayar, text="Kadın Sesi (Emel)", variable=cinsiyet_var, value="Kadın", font=("Arial", 10))
rb_kadin.pack(side="left", padx=20)

rb_erkek = tk.Radiobutton(frame_ayar, text="Erkek Sesi (Ahmet)", variable=cinsiyet_var, value="Erkek", font=("Arial", 10))
rb_erkek.pack(side="left", padx=20)


btn_cevir = tk.Button(pencere, text="MP3'e Dönüştür ve Kaydet", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=baslat, height=2)
btn_cevir.pack(fill="x", padx=20, pady=10)


pencere.mainloop()