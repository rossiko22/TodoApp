# 🚀 Quick Start - Rešitev za GitHub Pages Deployment

## ⚡ 3 Koraki za Uspešen Deployment

### ✅ Korak 1: Omogočite GitHub Pages (v brskalniku)

1. Odprite vaš GitHub repozitorij
2. Kliknite **Settings** (zgoraj desno)
3. V levem meniju kliknite **Pages**
4. Pri **"Build and deployment"** izberite:
   ```
   Source: GitHub Actions
   ```
   (POMEMBNO: NE izbirajte "Deploy from a branch")

### ✅ Korak 2: Commitajte in pushajte spremembe

```bash
# Preverite status
git status

# Dodajte spremembe (če še niso)
git add .github/workflows/ci-cd.yml
git commit -m "Optimize GitHub Pages deployment with concurrency control"

# Pushajte na GitHub
git push origin main
```

### ✅ Korak 3: Preverite Deployment

1. Pojdite na **Actions** tab v vašem repozitoriju
2. Sledite trenutnemu workflow run-u
3. Job "Deploy to GitHub Pages" naj bi se uspešno zaključil v ~1 minuti
4. URL vaše strani bo prikazan v job summary

---

## 📊 Kaj smo izboljšali v workflow-u

1. **Concurrency Control** - Preprečuje multiple simultane deploymente
2. **Debugging Steps** - Prikazuje vsebino docs/ direktorija
3. **Summary Output** - Prikazuje URL strani po uspešnem deploymentu
4. **Better Error Handling** - Lažje odkrivanje problemov

---

## 🔍 Če še vedno ne deluje

### Možnost A: Cancel in Re-run

1. Actions → Izberite trenutni workflow run
2. Kliknite "Cancel workflow"
3. Kliknite "Re-run all jobs"

### Možnost B: Preverite GitHub Pages Permissions

1. Settings → Actions → General
2. Scroll do "Workflow permissions"
3. Izberite: **"Read and write permissions"**
4. Kliknite Save

### Možnost C: Ročno Enable GitHub Pages

Če GitHub Actions source ni na voljo:

1. Settings → Pages
2. Če vidite samo "Deploy from a branch":
   - Začasno izberite: Branch: `main`, Folder: `/docs`
   - Počakajte 30 sekund
   - Ponovno izberite: Source: `GitHub Actions`

---

## ✅ Kontrolni seznam

- [ ] GitHub Pages source nastavljen na "GitHub Actions"
- [ ] Workflow permissions so "Read and write"
- [ ] Commit in push sprememb je uspel
- [ ] GitHub Actions workflow je tekočil
- [ ] Job "Deploy to GitHub Pages" je uspel
- [ ] URL strani je dostopen

---

## 🎯 Pričakovani rezultat

Po uspešnem deploymentu:

```
✅ Build Application
✅ Deploy to GitHub Pages
✅ Deploy to Development
✅ Deploy to Render
```

Vaša stran bo dostopna na:
```
https://[username].github.io/[repository-name]/
```

---

## 📞 Dodatna pomoč

Če po vseh teh korakih še vedno ne deluje:

1. Preverite workflow logs: Actions → izberite run → Deploy to GitHub Pages
2. Poiščite morebitne error message-e
3. Preverite da:
   - Datoteka `docs/index.html` obstaja
   - Datoteka `docs/.nojekyll` obstaja
   - Repository je public (ali imate GitHub Pro za private repos)

Podrobnejše informacije: `GITHUB_PAGES_SETUP.md`
