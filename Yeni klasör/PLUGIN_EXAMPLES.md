# 🔌 Örnek Plugin'ler

WhatsApp'tan kopyala-yapıştır yapabileceğiniz hazır plugin örnekleri.

## 💰 Bitcoin Fiyatı (API ile)

```
.plugin bitcoin | Bitcoin fiyatı |
    import requests
    try:
        r = requests.get('https://api.coindesk.com/v1/bpi/currentprice/USD.json', timeout=5)
        data = r.json()
        price = data['bpi']['USD']['rate']
        return f"₿ Bitcoin: ${price}"
    except:
        return "❌ Fiyat alınamadı!"
```

## 🎲 Zar Atma

```
.plugin zar | Zar atar |
    import random
    sayi = int(args) if args and args.isdigit() else 1
    zarlar = [random.randint(1, 6) for _ in range(min(sayi, 10))]
    emoji = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    sonuc = " ".join([emoji[z] for z in zarlar])
    return f"🎲 {sonuc}\nToplam: {sum(zarlar)}"
```

## 🔐 Şifre Üretici

```
.plugin sifre | Güçlü şifre üretir |
    import random
    import string
    uzunluk = int(args) if args and args.isdigit() else 12
    karakterler = string.ascii_letters + string.digits + "!@#$%^&*"
    sifre = ''.join(random.choice(karakterler) for _ in range(min(uzunluk, 50)))
    return f"🔐 Şifre ({len(sifre)} karakter):\n{sifre}"
```

## 📊 BMI Hesaplayıcı

```
.plugin bmi | Vücut kitle indeksi |
    try:
        parts = args.split()
        kilo, boy = float(parts[0]), float(parts[1]) / 100
        bmi = kilo / (boy ** 2)
        
        if bmi < 18.5:
            durum = "Zayıf"
        elif bmi < 25:
            durum = "Normal"
        elif bmi < 30:
            durum = "Fazla kilolu"
        else:
            durum = "Obez"
        
        return f"📊 BMI: {bmi:.1f}\n📌 {durum}"
    except:
        return "❌ Kullanım: .bmi <kilo> <boy(cm)>"
```

## ✅ Todo Listesi

```
.plugin todo | Yapılacaklar |
    import json
    
    todos_str = bot.db.get_plugin_data('todo', 'list')
    todos = json.loads(todos_str) if todos_str else []
    
    if not args:
        if not todos:
            return "✅ Liste boş!"
        return "✅ *Todo*\n\n" + "\n".join([f"{i+1}. {t}" for i, t in enumerate(todos)])
    
    if args.startswith('sil '):
        try:
            index = int(args.split()[1]) - 1
            removed = todos.pop(index)
            bot.db.save_plugin_data('todo', 'list', json.dumps(todos))
            return f"✅ Silindi: {removed}"
        except:
            return "❌ Geçersiz!"
    
    if args == 'temizle':
        bot.db.save_plugin_data('todo', 'list', '[]')
        return "✅ Liste temizlendi!"
    
    todos.append(args)
    bot.db.save_plugin_data('todo', 'list', json.dumps(todos))
    return f"✅ Eklendi: {args}"
```

## 🎯 Sayaç

```
.plugin sayac | Tıklama sayacı |
    count = bot.db.get_plugin_data('sayac', 'count')
    count = int(count) if count else 0
    
    if args == 'sifirla':
        bot.db.save_plugin_data('sayac', 'count', '0')
        return "🔢 Sayaç sıfırlandı!"
    
    count += 1
    bot.db.save_plugin_data('sayac', 'count', str(count))
    return f"🔢 Sayaç: {count}"
```

## 💱 Para Çevirici

```
.plugin para | Dolar/TL çevirici |
    try:
        miktar = float(args)
        kur = 32.50  # Güncel kuru buradan değiştirin
        tl = miktar * kur
        return f"💵 ${miktar} = ₺{tl:.2f}\n(Kur: {kur})"
    except:
        return "❌ Kullanım: .para <miktar>"
```

## 🌡️ Hava Durumu (API ile)

```
.plugin hava | Hava durumu |
    import requests
    if not args:
        return "❌ Kullanım: .hava <şehir>"
    
    try:
        # OpenWeatherMap API (ücretsiz)
        # API_KEY almanız gerekiyor: https://openweathermap.org/api
        api_key = "YOUR_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={args}&appid={api_key}&units=metric&lang=tr"
        r = requests.get(url, timeout=5)
        data = r.json()
        
        sehir = data['name']
        sicaklik = data['main']['temp']
        hissedilen = data['main']['feels_like']
        durum = data['weather'][0]['description']
        
        return f"🌤️ *{sehir}*\n\n🌡️ {sicaklik}°C (Hissedilen: {hissedilen}°C)\n☁️ {durum.capitalize()}"
    except:
        return "❌ Hava durumu alınamadı!"
```

## 📝 Not Defteri

```
.plugin defter | Hızlı not defteri |
    import json
    
    notes_str = bot.db.get_plugin_data('defter', 'notes')
    notes = json.loads(notes_str) if notes_str else []
    
    if not args:
        if not notes:
            return "📝 Defter boş!"
        return "📝 *Notlar*\n\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(notes)])
    
    if args.startswith('sil '):
        try:
            index = int(args.split()[1]) - 1
            removed = notes.pop(index)
            bot.db.save_plugin_data('defter', 'notes', json.dumps(notes))
            return f"✅ Silindi: {removed}"
        except:
            return "❌ Geçersiz!"
    
    notes.append(args)
    bot.db.save_plugin_data('defter', 'notes', json.dumps(notes))
    return f"✅ Not eklendi!"
```

## 🎮 Sayı Tahmin Oyunu

```
.plugin oyun | Sayı tahmin oyunu |
    import random
    
    if args == "yeni":
        sayi = random.randint(1, 100)
        bot.db.save_plugin_data('oyun', 'sayi', str(sayi))
        bot.db.save_plugin_data('oyun', 'tahmin', '0')
        return "🎮 1-100 arası sayı tuttum!\nTahmin et!"
    
    sayi = bot.db.get_plugin_data('oyun', 'sayi')
    if not sayi:
        return "❌ Önce 'yeni' yaz!"
    
    try:
        tahmin_count = int(bot.db.get_plugin_data('oyun', 'tahmin') or '0')
        tahmin_count += 1
        bot.db.save_plugin_data('oyun', 'tahmin', str(tahmin_count))
        
        tahmin = int(args)
        sayi = int(sayi)
        
        if tahmin == sayi:
            bot.db.save_plugin_data('oyun', 'sayi', '')
            return f"🎉 DOĞRU! {tahmin_count} tahminde buldun!\n\nYeni oyun: .oyun yeni"
        elif tahmin < sayi:
            return f"⬆️ Daha BÜYÜK! ({tahmin_count}. tahmin)"
        else:
            return f"⬇️ Daha KÜÇÜK! ({tahmin_count}. tahmin)"
    except:
        return "❌ Geçersiz sayı!"
```

---

## 💡 AI ile Daha Fazlası!

Bu örnekleri kullanmak yerine AI'ya söyleyin:

```
.aiplugin kelime sayacı
.aiplugin rastgele isim üretici
.aiplugin alışveriş listesi
.aiplugin pomodoro zamanlayıcı
```

AI sizin için plugin kodunu otomatik oluşturur!

---

**Kolay gelsin! 🚀**
