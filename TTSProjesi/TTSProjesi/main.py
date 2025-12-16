import asyncio
import edge_tts


SECILEN_SES = "tr-TR-EmelNeural" 


CIKTI_DOSYASI = "seslendirme.mp3"


def metni_oku(dosya_yolu):
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Hata: metin.txt dosyası bulunamadı!")
        return None

async def seslendir_ve_kaydet(metin, ses, cikti):
    print(f"Seslendirme işlemi başlıyor... Kullanılan ses: {ses}")
    
    
    communicate = edge_tts.Communicate(metin, ses)
    
    
    await communicate.save(cikti)
    
    print(f"İşlem tamamlandı! Dosya '{cikti}' adıyla kaydedildi.")


if __name__ == "__main__":
    
    uzun_metin = metni_oku("metin.txt")

    if uzun_metin:
        
        asyncio.run(seslendir_ve_kaydet(uzun_metin, SECILEN_SES, CIKTI_DOSYASI))