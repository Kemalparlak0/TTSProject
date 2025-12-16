from flask import Flask, request, send_file
from flask_cors import CORS 
import asyncio
import edge_tts
import io
import logging

# Loglama ayarı
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

CORS(app) 


@app.route('/seslendir', methods=['POST'])
def seslendir_api():
    try:
        
        data = request.get_json()
        metin = data.get('metin')
        ses_kodu = data.get('ses_kodu', 'tr-TR-EmelNeural') # Varsayılan ses
        
        if not metin or len(metin.strip()) == 0:
            app.logger.warning("Boş metin isteği geldi.")
            return {"error": "Lütfen seslendirilecek bir metin girin."}, 400

        
        async def generate_tts(text, voice):
            app.logger.info(f"Seslendirme işlemi başladı. Ses: {voice}, Metin uzunluğu: {len(text)}")
            communicate = edge_tts.Communicate(text, voice)
            audio_bytes = b''
            async for chunk in communicate.stream():
                if chunk.audio:
                    audio_bytes += chunk.audio
            return audio_bytes

        
        audio_data = asyncio.run(generate_tts(metin, ses_kodu))
        
        if not audio_data:
            raise Exception("edge-tts ses verisi oluşturamadı.")

       
        app.logger.info("Ses verisi başarıyla oluşturuldu ve gönderiliyor.")
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='seslendirme.mp3'
        )

    except Exception as e:
        app.logger.error(f"Hata oluştu: {e}")
        return {"error": f"Sunucu hatası: {str(e)}"}, 500

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000)