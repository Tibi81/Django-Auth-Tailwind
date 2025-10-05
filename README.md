# Django Auth Tailwind
### Ez a projekt egy Django alapú autentikációs rendszer, amely Tailwind CSS-t használ a dizájnhoz.

# ✅ Projekt állapota
Ez a projekt teljesen működőképes és használható formában van. A kód tisztított, biztonságos és teljes tesztlefedettséggel rendelkezik. Fejlesztési környezetben azonnal használható, éles környezetbe telepítéshez minimális konfiguráció szükséges.

<table style="width: 150%;">
  <tr>
    <td style="border: 10px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/Macbook-Air-127.0.0.1.png" width="300"/>
    </td>
    <td style="border: 10px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/iPad-Air-4-127.0.0.1.png" width="300"/>
    </td>
  </tr>
  <tr>
    <td style="border: 10px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/iPhone-13-PRO-127.0.0.1.png" width="200"/>
    </td>
    <td style="border: 10px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/Macbook-Air-127.0.0.1%20(1).png" width="300"/>
    </td>
  </tr>
</table>






### Cél
A cél egy könnyen integrálható, biztonságos felhasználói autentikációs rendszer biztosítása Django és Tailwind CSS segítségével. A rendszer gyors és egyszerű módot kínál a regisztrációra, bejelentkezésre és a jelszó visszaállítására.

### Jellemzők
- ✅ Felhasználói regisztráció és bejelentkezés
- ✅ Jelszó visszaállítása és változtatása
- ✅ Email cím hitelesítés és módosítás
- ✅ Profil kezelés (szerkesztés, törlés)
- ✅ Tailwind CSS alapú reszponzív dizájn
- ✅ Biztonságos autentikációs rendszer
- ✅ Teljes tesztlefedettség (43 teszt)
- ✅ Proper logging és hibakezelés
- ✅ Környezeti változók támogatása

### Követelmények
- Python 3.8+
- Django 5.1.7
- Node.js 12+
- NPM
- Pillow (képek kezeléséhez)

### Használhatóság

**Fejlesztési környezet:** ✅ Azonnal használható
- Minden funkció működik
- Teljes tesztlefedettség
- Biztonságos konfiguráció

**Éles környezet:** ⚠️ Minimális konfiguráció szükséges
- Adatbázis váltás (SQLite → PostgreSQL/MySQL)
- HTTPS beállítások
- Static files CDN-re költöztetése

### Dokumentáció

A teljes dokumentáció itt található: (https://django-tailwind.readthedocs.io/)

## 🚀 Gyors kezdés

### Telepítés
Klónozd a repót:

```bash
git clone https://github.com/Tibi81/Django_Auth-Tailwind.git
```

### Hozz létre egy virtuális környezetet és aktiváld:
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

### Lépj a projekt mappájába:

```bash
cd Django_Auth-Tailwind
```

### Telepítsd a szükséges csomagokat:

```bash
pip install -r requirements.txt
```

### Környezeti változók beállítása:

1. Másold az `env.example` fájlt `.env` néven:
```bash
copy env.example .env
```

2. Szerkeszd a `.env` fájlt és add meg a saját értékeidet:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Készíts migrációkat:

```bash
python manage.py migrate
```

### Állítsd be a statikus fájlokat (ha szükséges):

```bash
python manage.py collectstatic
```
### Fejlesztés

## Email hitelesítés beállítása

Az email hitelesítés már be van állítva a környezeti változókon keresztül. A `.env` fájlban add meg az email beállításokat:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Fontos:** Gmail esetén használj App Password-ot a normál jelszó helyett!


### Futtasd a szervert:

```bash
python manage.py runserver
```
## Tailwind CSS konfigurálás<br>

### Telepítsd a Node.js csomagokat:

```bash
npm install
```
### Futtasd a Tailwind build-et:

```bash
npm run build
```

## Legutóbbi javítások (2025.01.05)

### Biztonsági javítások:
- ✅ SECRET_KEY környezeti változóból olvasása
- ✅ DEBUG és ALLOWED_HOSTS biztonságos beállítása
- ✅ Email beállítások környezeti változókkal

### Kód minőség javítások:
- ✅ Debug print üzenetek eltávolítása és proper logging beállítása
- ✅ Duplikált kód refaktorálása (email értesítések)
- ✅ Duplikált URL pattern javítása
- ✅ Duplikált DEFAULT_FROM_EMAIL javítása

### Dokumentáció javítások:
- ✅ Környezeti változók dokumentálása
- ✅ Telepítési útmutató frissítése
- ✅ env.example fájl létrehozása

### Tesztelés:
- ✅ Minden teszt sikeresen lefut (43/43)
- ✅ Django check sikeresen lefut hibák nélkül

## Projekt státusz

**Stabil verzió:** ✅ v1.0.0
- Minden alapvető funkció implementálva
- Biztonsági problémák javítva
- Kód tisztított és optimalizált
- Teljes dokumentáció

**Karbantartás:** ✅ Aktív
- Hibajavítások és biztonsági frissítések
- Új funkciók fejlesztése
- Dokumentáció frissítése

## Hibajelzés és javítási javaslatok
Ha hibát találsz a projektben, kérjük, nyiss egy új Issue-t a GitHub repóban. A hiba leírása mellett kérjük, add meg a következő információkat:

-A hiba pontos leírása

-A használt rendszer és verzió

-Lépések, amelyek reprodukálják a hibát

## Felhasználási feltételek

Ez a projekt a MIT licenc alatt elérhető. Szabadon másolhatod, módosíthatod és terjesztheted a projektet, amennyiben betartod a következő feltételeket:

A szerzői jogok és licencfeltételek megőrzése.

A módosított verziók nem kerülhetnek más licenc alatt terjesztésre.

A teljes licencet [itt találhatod.](https://opensource.org/license/mit)

## Ha tetszett a projekt, kérlek, adj neki csillagot! 🌟

A csillagok segítenek abban, hogy a projekt jobban látható legyen, és mások is felfedezhessék!

