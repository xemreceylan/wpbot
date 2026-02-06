# 🤖 WhatsApp UserBot v4.0 - AI Powered Edition

**Google Gemini AI entegrasyonu ile gelişmiş WhatsApp otomasyon botu!**

WhatsApp içinden AI ile konuş, AI'ya plugin yazdır, bulut sunucuda 24/7 çalıştır!

## ✨ Ana Özellikler

### 🧠 Google Gemini AI Entegrasyonu
- ✅ **AI Sohbet** - Gemini ile doğal dilde konuş
- ✅ **AI Plugin Oluşturucu** - "bitcoin fiyatı gösteren plugin yap" → AI kodu yazar!
- ✅ **Sürekli AI Modu** - Tüm mesajlar AI'ya gider
- ✅ **Kod Analizi** - AI kodlarını açıklar
- ✅ **Çeviri & Özet** - AI destekli metin işleme

### 🔌 Dinamik Plugin Sistemi
- WhatsApp'tan direkt plugin oluştur
- AI ile otomatik plugin üret
- Veri saklama desteği
- Anında yükleme

### ☁️ Bulut Sunucu Desteği
- **Google Cloud Platform** tam kurulum rehberi
- AWS, Azure, DigitalOcean uyumlu
- Headless mod (GUI olmadan)
- Screen/tmux ile arka plan
- Auto-restart desteği

### 📝 Standart Özellikler
- Hatırlatma sistemi
- Not alma/saklama
- İstatistikler
- AFK modu
- Otomatik yanıt
- 15+ built-in komut

---

## 🚀 Hızlı Başlangıç (Yerel)

### 1. Kurulum
```bash
# Depoyu klonla
git clone https://github.com/kullaniciadi/whatsapp-userbot.git
cd whatsapp-userbot

# Bağımlılıkları yükle
pip install -r requirements.txt

# ChromeDriver kur
# Linux:
sudo apt-get install chromium-chromedriver

# macOS:
brew install chromedriver

# Windows: https://chromedriver.chromium.org/downloads
```

### 2. AI API Anahtarı (Opsiyonel ama Önerilen!)

Google Gemini API anahtarı al (ÜCRETSİZ):
1. https://makersuite.google.com/app/apikey adresine git
2. "Create API Key" tıkla
3. Anahtarı kopyala

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Çalıştır
```bash
python whatsapp_userbot.py
```

İlk çalıştırmada QR kodu tarayın, sonraki çalıştırmalarda otomatik giriş!

---

## ☁️ Google Cloud Platform Kurulumu (24/7 Çalışma)

### Adım 1: GCP Hesabı ve Proje Oluştur

1. **Google Cloud Console'a git**: https://console.cloud.google.com
2. **Yeni proje oluştur**: "WhatsApp-UserBot" gibi bir isim ver
3. **Faturalandırma aktif et**: $300 ücretsiz kredi var (1 yıl)

### Adım 2: VM Instance Oluştur

#### a) Compute Engine'e Git
- Sol menüden: **Compute Engine > VM instances**
- **CREATE INSTANCE** butonuna tıkla

#### b) Instance Ayarları

**Temel Ayarlar:**
```
Name: whatsapp-bot
Region: europe-west1 (Belçika) veya us-central1
Zone: Otomatik seçim
```

**Machine Configuration:**
```
Series: E2
Machine type: e2-micro (0.25-2 vCPU, 1 GB RAM)
  → ÜCRETSİZ: Aylık 1 e2-micro instance ücretsiz!
```

**Boot Disk:**
```
Operating System: Ubuntu
Version: Ubuntu 24.04 LTS (Minimal)
Boot disk type: Standard persistent disk
Size: 10 GB
```

**Firewall:**
```
☐ Allow HTTP traffic (gerekli değil)
☐ Allow HTTPS traffic (gerekli değil)
```

**CREATE** butonuna tıkla!

### Adım 3: VM'ye Bağlan

#### SSH ile Bağlan
Google Cloud Console'da instance'ın yanındaki **SSH** butonuna tıkla.

Veya terminal'den:
```bash
gcloud compute ssh whatsapp-bot --zone=europe-west1-b
```

### Adım 4: Sunucuyu Hazırla

```bash
# Sistem güncellemesi
sudo apt-get update
sudo apt-get upgrade -y

# Python ve pip
sudo apt-get install -y python3 python3-pip python3-venv

# Chrome ve ChromeDriver
sudo apt-get install -y chromium-browser chromium-chromedriver

# Git
sudo apt-get install -y git screen

# Çalışma dizini oluştur
mkdir ~/whatsapp-bot
cd ~/whatsapp-bot
```

### Adım 5: Bot Dosyalarını Yükle

**Seçenek 1: Git ile (Önerilen)**
```bash
git clone https://github.com/kullaniciadi/whatsapp-userbot.git .
```

**Seçenek 2: Manuel Upload**
```bash
# Lokal bilgisayarınızdan (başka bir terminal):
gcloud compute scp whatsapp_userbot.py whatsapp-bot:~/whatsapp-bot/
gcloud compute scp requirements.txt whatsapp-bot:~/whatsapp-bot/
```

**Seçenek 3: Nano ile Oluştur**
```bash
nano whatsapp_userbot.py
# Kodu yapıştır (Ctrl+Shift+V), Ctrl+X, Y, Enter

nano requirements.txt
# İçeriği yapıştır, kaydet
```

### Adım 6: Python Bağımlılıkları

```bash
# Virtual environment oluştur (önerilen)
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install --upgrade pip
pip install -r requirements.txt
```

### Adım 7: Gemini API Anahtarı Ayarla

```bash
# Geçici (bu oturum için)
export GEMINI_API_KEY="your-api-key-here"

# Kalıcı (önerilen)
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Adım 8: İlk Çalıştırma (QR Kod Tarama)

İlk kez çalıştırmak için X11 forwarding veya VNC gerekli.

**Kolay Yöntem: Lokal bilgisayarda QR tara, sonra sunucuya taşı:**

```bash
# 1. Lokal bilgisayarınızda (GUI olan):
python whatsapp_userbot.py
# QR kodu tara, giriş yap, Ctrl+C ile durdur

# 2. User_Data klasörünü sunucuya kopyala:
gcloud compute scp --recurse User_Data whatsapp-bot:~/whatsapp-bot/
```

**Alternatif: VNC ile GUI Kurulumu**
```bash
# Desktop environment kur
sudo apt-get install -y ubuntu-desktop-minimal

# VNC server kur
sudo apt-get install -y tightvncserver

# VNC başlat
vncserver :1

# Şifre belirle ve lokal bilgisayardan VNC client ile bağlan
# IP: EXTERNAL_IP:5901
```

### Adım 9: Screen ile Arka Planda Çalıştır

```bash
# Screen oturumu başlat
screen -S whatsapp-bot

# Virtual environment aktif et
source venv/bin/activate

# Botu başlat
python whatsapp_userbot.py

# Screen'den çık (bot çalışmaya devam eder)
# Ctrl+A, ardından D tuşlarına bas
```

**Screen Komutları:**
```bash
screen -ls              # Aktif screen'leri listele
screen -r whatsapp-bot  # Screen'e geri dön
screen -X -S whatsapp-bot quit  # Screen'i kapat
```

### Adım 10: Systemd Service (Auto-Restart)

Daha profesyonel: Systemd service oluştur

```bash
sudo nano /etc/systemd/system/whatsapp-bot.service
```

İçeriği:
```ini
[Unit]
Description=WhatsApp UserBot v4.0
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/whatsapp-bot
Environment="GEMINI_API_KEY=your-api-key"
Environment="HEADLESS=true"
ExecStart=/home/YOUR_USERNAME/whatsapp-bot/venv/bin/python /home/YOUR_USERNAME/whatsapp-bot/whatsapp_userbot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

`YOUR_USERNAME` kısmını değiştir:
```bash
whoami  # kullanıcı adını öğren
```

Service'i aktif et:
```bash
sudo systemctl daemon-reload
sudo systemctl enable whatsapp-bot
sudo systemctl start whatsapp-bot

# Durumu kontrol et
sudo systemctl status whatsapp-bot

# Logları izle
sudo journalctl -u whatsapp-bot -f
```

### Adım 11: Firewall ve Güvenlik

```bash
# UFW firewall aktif et
sudo ufw enable

# SSH'yi izin ver (önemli!)
sudo ufw allow ssh

# Durumu kontrol et
sudo ufw status
```

---

## 🖥️ Diğer Bulut Platformlar

### AWS EC2

```bash
# Instance Type: t2.micro (Free Tier)
# AMI: Ubuntu 24.04 LTS
# Storage: 8 GB GP2

# Bağlantı:
ssh -i "your-key.pem" ubuntu@your-instance-ip

# Kurulum aynı (Adım 4'ten başla)
```

### DigitalOcean Droplet

```bash
# Droplet: Basic - $4/mo (1 GB RAM)
# Image: Ubuntu 24.04 LTS
# Datacenter: Amsterdam veya Frankfurt

# SSH:
ssh root@your-droplet-ip

# Kurulum aynı
```

### Azure VM

```bash
# VM Size: B1s (1 vCPU, 1 GB RAM) - $7.59/mo
# Image: Ubuntu Server 24.04 LTS
# Region: West Europe

# SSH:
ssh azureuser@your-vm-ip
```

---

## 💡 Kullanım - AI Özellikleri

### AI ile Sohbet

```
.ai Merhaba! Python nedir?
🤖 Python, yorumlamalı, yüksek seviyeli...

.aisor En iyi programlama dili hangisi?
🤖 En iyi dil yoktur, ihtiyaca göre...
```

### AI Sürekli Sohbet Modu

```
.aichat
🤖 AI Sohbet Modu AÇIK

[Artık tüm mesajlarınız AI'ya gider]

Bugün nasılsın?
🤖 Ben bir AI'yım, hislerim yok ama...

.aichat
❌ AI Sohbet Modu KAPALI
```

### AI ile Plugin Oluştur

```
.aiplugin bitcoin fiyatını gösteren plugin
🤖 AI plugin oluşturuyor...
✅ Plugin oluşturuldu!
Ad: ai_bitcoinfiyatigosterenplugin
Kullanım: .ai_bitcoinfiyatigosterenplugin

.ai_bitcoinfiyatigosterenplugin
💰 Bitcoin: $43,250
```

**Daha Fazla Örnek:**
```
.aiplugin kelime sayacı
.aiplugin rastgele şifre oluşturucu
.aiplugin dolar tl çevirici
.aiplugin bmi hesaplayıcı
```

---

## 📱 Komut Listesi

### 🧠 AI Komutları

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `.ai <mesaj>` | AI ile sohbet | `.ai Python öğren` |
| `.aisor <soru>` | AI'ya soru | `.aisor En iyi framework?` |
| `.aichat` | Sürekli AI modu aç/kapa | `.aichat` |
| `.aiplugin <açıklama>` | AI plugin oluştur | `.aiplugin todo listesi` |

### 📝 Temel Komutlar

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `.help` | Yardım menüsü | `.help` |
| `.ping` | Bot testi | `.ping` |
| `.zaman` | Tarih ve saat | `.zaman` |
| `.bilgi` | Bot bilgisi | `.bilgi` |

### ⏰ Hatırlatma & Notlar

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `.hatirlatma <dk> <mesaj>` | Hatırlatma | `.hatirlatma 30 Toplantı` |
| `.not <etiket> <içerik>` | Not kaydet | `.not sifre abc123` |
| `.not <etiket>` | Not göster | `.not sifre` |
| `.notlar` | Notları listele | `.notlar` |
| `.notsil <etiket>` | Not sil | `.notsil sifre` |

### 🔌 Plugin Yönetimi

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `.plugin <ad> \| <desc> \| <kod>` | Manuel plugin | `.plugin test \| Test \| return "OK"` |
| `.aiplugin <açıklama>` | AI plugin | `.aiplugin hava durumu` |
| `.pluginler` | Plugin listesi | `.pluginler` |
| `.pluginsil <ad>` | Plugin sil | `.pluginsil test` |

### 🤖 Otomasyon

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `.afk <mesaj>` | AFK modu | `.afk Toplantıdayım` |
| `.otocevap <trigger> \| <cevap>` | Otomatik yanıt | `.otocevap merhaba \| Selam!` |

### 🛠️ Araçlar

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `.hesapla <işlem>` | Hesaplama | `.hesapla 15 * 8` |
| `.google <arama>` | Google arama | `.google Python` |
| `.spam <sayı> <mesaj>` | Toplu mesaj | `.spam 5 Test` |
| `.istatistik` | Mesaj istatistikleri | `.istatistik` |

---

## 🔧 Yapılandırma

### Ortam Değişkenleri

```bash
# AI API Anahtarı (önerilen!)
export GEMINI_API_KEY="your-api-key"

# Headless mod (sunucu için)
export HEADLESS="true"  # veya "false"
```

### Komut Öneki Değiştirme

`whatsapp_userbot.py` dosyasında:
```python
self.prefix = "."  # "!" veya "/" yapabilirsiniz
```

### Loglama

Loglar `userbot.log` dosyasında:
```bash
# Canlı log takibi
tail -f userbot.log

# Son 50 satır
tail -n 50 userbot.log
```

---

## 🐛 Sorun Giderme

### GCP'de Bot Başlamıyor

**Sorun:** ChromeDriver bulunamıyor
```bash
# Çözüm:
sudo apt-get install -y chromium-browser chromium-chromedriver
which chromedriver  # Yolu kontrol et
```

**Sorun:** Bellek yetersiz
```bash
# Çözüm: Swap ekle
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### QR Kod Tarama

**Sorun:** Headless modda QR göremiyorum

**Çözüm 1:** Lokal'de tara, User_Data'yı taşı (Adım 8)

**Çözüm 2:** VNC kur ve GUI'den tara

**Çözüm 3:** Screenshot al
```python
# whatsapp_userbot.py'de setup_driver() içine ekle:
time.sleep(10)  # QR için bekle
self.driver.save_screenshot('qr_code.png')

# Sonra sunucudan indir:
gcloud compute scp whatsapp-bot:~/whatsapp-bot/qr_code.png ./
```

### AI Çalışmıyor

**Sorun:** "GEMINI_API_KEY ayarlanmamış"

**Çözüm:**
```bash
# API anahtarını kontrol et
echo $GEMINI_API_KEY

# Yoksa ekle:
export GEMINI_API_KEY="your-key"

# Kalıcı yap:
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

### Bot Duruyor

**Sorun:** Screen/service kapanıyor

**Çözüm 1 (Screen):**
```bash
screen -r whatsapp-bot  # Durumu kontrol et
# Ctrl+A, D ile detach et
```

**Çözüm 2 (Systemd):**
```bash
sudo systemctl status whatsapp-bot
sudo systemctl restart whatsapp-bot
sudo journalctl -u whatsapp-bot -n 50
```

### Plugin Hatası

**Sorun:** Plugin çalışmıyor

**Çözüm:**
```bash
# Log'lara bak
tail -f userbot.log

# Plugin klasörünü kontrol et
ls -la plugins/

# Plugin'i manuel test et
python3 -c "from plugins.plugin_name import execute; print(execute(None, 'test'))"
```

---

## 📊 Performans & Maliyetler

### GCP e2-micro (ÜCRETSİZ)

```
CPU: 0.25-2 vCPU (paylaşımlı)
RAM: 1 GB
Disk: 10 GB
Ağ: 1 GB çıkış/ay ücretsiz
Maliyet: $0/ay (Always Free)
```

**Performans:**
- ✅ 1-5 sohbet: Sorunsuz
- ✅ AI kullanımı: Normal
- ⚠️ 10+ sohbet: Yavaşlama olabilir

### Ücretsiz Limiti Aştıysanız

**Upgrade Seçenekleri:**
```
e2-small: 2 vCPU, 2 GB RAM → $13/ay
e2-medium: 2 vCPU, 4 GB RAM → $27/ay
```

### Maliyet Optimizasyonu

```bash
# Bot'u sadece gerektiğinde çalıştır
sudo systemctl stop whatsapp-bot

# VM'yi durdur (ücretlendirme durur)
gcloud compute instances stop whatsapp-bot

# Tekrar başlat
gcloud compute instances start whatsapp-bot
```

---

## 🔐 Güvenlik Önerileri

### 1. API Anahtarını Gizle

```bash
# .bashrc yerine .env dosyası kullan
nano ~/.env

# İçerik:
GEMINI_API_KEY=your-key

# .env'yi yükle
source ~/.env
```

### 2. SSH Güvenliği

```bash
# SSH key ile giriş (şifre devre dışı)
sudo nano /etc/ssh/sshd_config

# Değiştir:
PasswordAuthentication no
PermitRootLogin no

# Restart:
sudo systemctl restart sshd
```

### 3. Güncellemeleri Otomatikleştir

```bash
# Unattended upgrades
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 4. Fail2Ban (Brute Force Koruması)

```bash
sudo apt-get install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 📈 İzleme & Monitoring

### Sistem Kaynakları

```bash
# CPU & RAM
htop

# Disk kullanımı
df -h

# Bot process
ps aux | grep python

# Ağ bağlantıları
netstat -tulpn | grep python
```

### GCP Monitoring

Google Cloud Console:
1. **Monitoring > Dashboards**
2. VM metrics: CPU, RAM, Disk, Network
3. Alert Policy oluştur (örn: CPU > %80)

---

## 🎯 En İyi Uygulamalar

### 1. Düzenli Yedekleme

```bash
# Veritabanını yedekle
cp userbot_data.db userbot_data.db.backup

# User_Data'yı yedekle
tar -czf user_data_backup.tar.gz User_Data/

# Lokal'e indir
gcloud compute scp whatsapp-bot:~/whatsapp-bot/*.backup ./
```

### 2. Plugin Yedekleme

```bash
# Tüm pluginleri yedekle
tar -czf plugins_backup.tar.gz plugins/

# Git ile versiyonlama
git init
git add plugins/
git commit -m "Plugin backup"
```

### 3. Log Rotasyonu

```bash
# Logrotate yapılandırması
sudo nano /etc/logrotate.d/whatsapp-bot

# İçerik:
/home/YOUR_USERNAME/whatsapp-bot/userbot.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Commit edin (`git commit -m 'Yeni özellik'`)
4. Push edin (`git push origin feature/YeniOzellik`)
5. Pull Request açın

---

## 📄 Lisans

MIT License - Özgürce kullanabilirsiniz!

---

## ⚠️ Sorumluluk Reddi

- Bu bot eğitim amaçlıdır
- WhatsApp'ın kullanım koşullarına dikkat edin
- Spam yapmayın, hesabınız banlanabilir
- Bulut maliyetlerinden kendiniz sorumlusunuz
- API kullanım limitlerini kontrol edin

---

## 🙏 Teşekkürler

- [Google Gemini](https://ai.google.dev/) - AI desteği
- [Selenium](https://www.selenium.dev/) - Web otomasyon
- [Google Cloud Platform](https://cloud.google.com/) - Hosting
- Tüm katkıda bulunanlara ❤️

---

**Made with ❤️ in Turkey 🇹🇷**

**WhatsApp UserBot v4.0** - AI Powered, Cloud Ready!

⭐ Beğendiyseniz yıldız vermeyi unutmayın!
