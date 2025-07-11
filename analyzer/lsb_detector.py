from PIL import Image

def detect_lsb_steganography(file_path):
    """Analyzes the LSB of an image to detect potential steganography."""
    try:
        with Image.open(file_path).convert('RGB') as img:
            width, height = img.size
            pixels = img.load()

            lsb_bits = []
            # Sadece bir örneklem alanı (ilk 50x50 piksel) analiz ediliyor
            # Performansı artırmak için tüm resmi analiz etmekten kaçınıyoruz
            sample_size = min(width, height, 50)

            for x in range(sample_size):
                for y in range(sample_size):
                    r, g, b = pixels[x, y]
                    lsb_bits.append(r & 1)
                    lsb_bits.append(g & 1)
                    lsb_bits.append(b & 1)
            
            # Basit bir istatistiksel analiz: 0 ve 1'lerin dağılımı
            zeros = lsb_bits.count(0)
            ones = lsb_bits.count(1)
            total_bits = len(lsb_bits)

            # Eğer bitler çok düzenli veya çok düzensiz ise şüpheli olabilir.
            # Normal bir fotoğrafta dağılımın %50'ye yakın olması beklenir.
            # %40-%60 aralığı dışındaki dağılımları şüpheli kabul edelim.
            ratio = ones / total_bits if total_bits > 0 else 0.5

            if not (0.4 < ratio < 0.6):
                return {
                    "status": "Suspicious LSB distribution detected.",
                    "suspicion_level": "High",
                    "details": f"LSB analysis of a {sample_size}x{sample_size} sample shows an unusual distribution of 0s and 1s (Ones ratio: {ratio:.2%}). This might indicate the presence of hidden data."
                }
            else:
                return {
                    "status": "No obvious signs of LSB steganography found.",
                    "suspicion_level": "Low",
                    "details": f"LSB distribution appears normal (Ones ratio: {ratio:.2%})."
                }

    except Exception as e:
        return {
            "status": "Error during LSB analysis.",
            "suspicion_level": "Error",
            "details": str(e)
        }
