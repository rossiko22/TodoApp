# 🔧 GitHub Pages Deployment - Rešitev za "deployment_queued"

## Problem
Deployment ostaja v `deployment_queued` statusu in ne napreduje.

## Razlog
Ko uporabljamo GitHub Actions workflow z `actions/deploy-pages@v4`, mora biti GitHub Pages source nastavljen na **"GitHub Actions"**, NE "Deploy from a branch".

## ✅ Pravilna rešitev

### Korak 1: Omogočite GitHub Pages z GitHub Actions source

1. **Pojdite na Settings vašega GitHub repozitorija**
2. **V levem meniju kliknite na "Pages"**
3. **Pri "Source" izberite:**
   - **Build and deployment**
   - **Source:** `GitHub Actions` ⬅️ **TO JE KLJUČNO!**
   - (NE izbirajte "Deploy from a branch")
4. **Shranite in počakajte nekaj sekund**

### Korak 2: Ponovno poženite workflow

1. Pojdite na **Actions** tab
2. Izberite zadnji workflow run (tisti, ki je stuck)
3. Kliknite **"Cancel workflow"** (če še vedno teče)
4. Nato kliknite **"Re-run all jobs"**

ALI

1. Naredite nov commit:
   ```bash
   git commit --allow-empty -m "Trigger GitHub Pages deployment"
   git push origin main
   ```

### Korak 3: Preverite deployment

Po nekaj sekundah ali minutah:
1. Pojdite na **Actions** → izberite workflow
2. Job "Deploy to GitHub Pages" naj bi se uspešno zaključil
3. Pojdite na **Settings** → **Pages**
4. Videli boste URL vaše strani: `https://[username].github.io/[repo-name]/`

## 🎯 Povzetek

**NAROBE** (stara navodila):
```
Source: Deploy from a branch
Branch: main
Folder: /docs
```

**PRAVILNO** (za GitHub Actions workflow):
```
Source: GitHub Actions
```

Workflow sam poskrbi za deployment iz `/docs` folderja!

## 📝 Opomba

Če želite uporabljati "Deploy from a branch" metodo namesto GitHub Actions, potem:
1. Odstranite `deploy-pages` job iz workflow-a
2. GitHub bo avtomatsko deploynal iz `/docs` folderja pri vsakem pushu na main
3. Vendar za to nalogo potrebujemo GitHub Actions workflow, zato uporabite **GitHub Actions** source!
