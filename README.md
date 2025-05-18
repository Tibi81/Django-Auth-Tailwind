# Django Auth Tailwind
### Ez a projekt egy Django alapú autentikációs rendszer, amely Tailwind CSS-t használ a dizájnhoz.

# 🚧  Fejlesztés alatt
Ez a projekt már működőképes és használható formában van, azonban jelenleg nincsenek még automatikus tesztek írva hozzá. A közeljövőben a kód strukturálásán, olvashatóságán és teszteléssel való lefedettségén dolgozom a jobb karbantarthatóság és megbízhatóság érdekében.

<table>
  <tr>
    <td style="border: 3px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/Macbook-Air-127.0.0.1.png" width="300"/>
    </td>
    <td style="border: 3px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/iPad-Air-4-127.0.0.1.png" width="300"/>
    </td>
  </tr>
  <tr>
    <td style="border: 3px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/iPhone-13-PRO-127.0.0.1.png" width="200"/>
    </td>
    <td style="border: 3px solid #4F46E5; padding: 5px;">
      <img src="https://raw.githubusercontent.com/Tibi81/Django_Auth-Tailwind/refs/heads/main/Macbook-Air-127.0.0.1%20(1).png" width="300"/>
    </td>
  </tr>
</table>






### Cél
A cél egy könnyen integrálható, biztonságos felhasználói autentikációs rendszer biztosítása Django és Tailwind CSS segítségével. A rendszer gyors és egyszerű módot kínál a regisztrációra, bejelentkezésre és a jelszó visszaállítására.

### Jellemzők
-Felhasználói regisztráció és bejelentkezés.

-Jelszó visszaállítása.

-Email hitelesítés.

-Tailwind CSS alapú reszponzív dizájn.

-Könnyen testreszabható autentikációs oldalak.

### Követelmények
-Python 3.8+

-Django 3.0+

-Node.js 12+

-Npm

### Dokumentáció

A teljes dokumentáció itt található: (https://django-tailwind.readthedocs.io/)

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
### Készíts migrációkat:

```bash
python manage.py migrate
```
### Állítsd be a statikus fájlokat (ha szükséges):

```bash
python manage.py collectstatic
```
### Fejlesztés<br>

## Email hitelesítés beállítása

A projektben az email hitelesítés működéséhez szükséges egy `.env` fájl létrehozása, amely tartalmazza az email beállításokat. Kövesd az alábbi lépéseket:

1. Hozz létre egy `.env` nevű fájlt a projekt gyökérkönyvtárában.
2. Írd bele az alábbi tartalmat:

    ```env
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_password
    ```

3. Cseréld le a `your_email@example.com`-ot a saját email címedre, és a `your_password`-ot a megfelelő jelszóra.
4. Mentsd el a fájlt.

Miután ezt megtetted, most már futtathatod a projektet.


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

