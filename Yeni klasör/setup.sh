#!/bin/bash
# WhatsApp UserBot v4.0 - Quick Start Script
# Linux Bulut Sunucu için Otomatik Kurulum

echo "=================================="
echo "WhatsApp UserBot v4.0 Kurulum"
echo "=================================="
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Sistem güncellemesi
echo -e "${YELLOW}[1/8]${NC} Sistem güncelleniyor..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

# Python kurulumu
echo -e "${YELLOW}[2/8]${NC} Python yükleniyor..."
sudo apt-get install -y python3 python3-pip python3-venv git screen -qq

# Chrome ve ChromeDriver
echo -e "${YELLOW}[3/8]${NC} Chrome ve ChromeDriver yükleniyor..."
sudo apt-get install -y chromium-browser chromium-chromedriver -qq

# Çalışma dizini
echo -e "${YELLOW}[4/8]${NC} Çalışma dizini oluşturuluyor..."
mkdir -p ~/whatsapp-bot
cd ~/whatsapp-bot

# Virtual environment
echo -e "${YELLOW}[5/8]${NC} Python virtual environment oluşturuluyor..."
python3 -m venv venv
source venv/bin/activate

# Python paketleri
echo -e "${YELLOW}[6/8]${NC} Python paketleri yükleniyor..."
pip install --upgrade pip -qq
pip install selenium requests psutil -qq

# API anahtarı kontrolü
echo -e "${YELLOW}[7/8]${NC} API anahtarı ayarlanıyor..."
echo ""
echo -e "${GREEN}Google Gemini API anahtarınızı girin:${NC}"
echo "  (Ücretsiz API: https://makersuite.google.com/app/apikey)"
echo "  (Boş bırakırsanız AI özellikleri devre dışı olur)"
read -p "API Key: " GEMINI_KEY

if [ -n "$GEMINI_KEY" ]; then
    echo "export GEMINI_API_KEY='$GEMINI_KEY'" >> ~/.bashrc
    export GEMINI_API_KEY="$GEMINI_KEY"
    echo -e "${GREEN}✓ API anahtarı kaydedildi${NC}"
else
    echo -e "${YELLOW}⚠ API anahtarı atlandı (AI özellikleri devre dışı)${NC}"
fi

# Headless mod
export HEADLESS=true
echo "export HEADLESS=true" >> ~/.bashrc

echo -e "${YELLOW}[8/8]${NC} Kurulum tamamlanıyor..."

# Dosyaları kontrol et
if [ ! -f "whatsapp_userbot.py" ]; then
    echo -e "${RED}❌ whatsapp_userbot.py bulunamadı!${NC}"
    echo "Dosyayı manuel olarak yükleyin:"
    echo "  nano whatsapp_userbot.py"
    exit 1
fi

echo ""
echo -e "${GREEN}=================================="
echo "✓ Kurulum Tamamlandı!"
echo "==================================${NC}"
echo ""
echo "📱 Sonraki adımlar:"
echo ""
echo "1. İlk çalıştırma (QR kod taramak için):"
echo "   ${YELLOW}python whatsapp_userbot.py${NC}"
echo "   (Lokal bilgisayarda QR tara, User_Data klasörünü sunucuya kopyala)"
echo ""
echo "2. Screen ile arka planda çalıştır:"
echo "   ${YELLOW}screen -S whatsapp-bot${NC}"
echo "   ${YELLOW}source venv/bin/activate${NC}"
echo "   ${YELLOW}python whatsapp_userbot.py${NC}"
echo "   ${YELLOW}Ctrl+A, D (detach)${NC}"
echo ""
echo "3. Systemd service ile otomatik başlat:"
echo "   ${YELLOW}sudo nano /etc/systemd/system/whatsapp-bot.service${NC}"
echo "   (whatsapp-bot.service içeriğini yapıştır)"
echo "   ${YELLOW}sudo systemctl enable whatsapp-bot${NC}"
echo "   ${YELLOW}sudo systemctl start whatsapp-bot${NC}"
echo ""
echo "🔌 Gemini AI: ${GEMINI_KEY:+✅ Aktif}${GEMINI_KEY:-❌ Devre dışı}"
echo ""
echo "📚 Detaylı bilgi: README.md"
