# Gastromapa 🍴

Gastromapa je Django aplikace sloužící k objevování restaurací, hodnocení návštěvníků a ukládání oblíbených podniků.

---

## 🚀 Funkcionality
- Databáze restaurací a hodnocení zákazníků.
- Nahrávání fotek a médií.
- Uživatelská autentizace a hodnocení.
- Správa podniků pomocí administrace Django.

---

## 📚 Technologie

Tento projekt je postaven pomocí následujících nástrojů a technologií:

- **Python 3.9** 
- **Django Web Framework** 
- **HTML, CSS, JavaScript** (frontend)
- **SQLite** (pro lokální vývoj)

---

## 🛠️ Instalace

1. Naklonujte repozitář:

   ```bash
   git clone https://github.com/uzivatel/gastromapa.git
   cd gastromapa
   ```

2. Vytvoř si virtuální prostředí a aktivuj ho:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Na Windows použij `venv\Scripts\activate`
   ```

3. Nainstalujte potřebné závislosti:

   ```bash
   pip install -r requirements.txt
   ```

4. Vytvoř databázi:

   ```bash
   python manage.py migrate
   ```

5. Spusť vývojový server:

   ```bash
   python manage.py runserver
   ```

Aplikace poběží na `http://127.0.0.1:8000/`.

---

## 🗺️ Použití

1. Uživatel se může zaregistrovat a přihlásit.
2. Může přidávat oblíbené restaurace, prohlížet recenze nebo přidat vlastní.

---
