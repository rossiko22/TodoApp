# GitHub Pages in Environments - Navodila za nastavitev

## 📋 Pregled implementacije

Implementiral sem vse zahteve naloge:

### ✅ 1. GitHub Pages (30%)
- **Lokacija**: `/docs/index.html`
- **Vsebina**:
  - Ime projekta: Todo App
  - Člani ekipe: 3 člani (prosim, posodobite z dejanskimi imeni)
  - Kratek opis projekta s funkcionalnostmi
  - Pregled tehnologij in CI/CD pipeline-a
- **Deployment**: Avtomatski deployment prek GitHub Actions pri push na `main` vejo

### ✅ 2. Environments (70%)

#### Development Environment
- **Trigger**: Push na `main` ali `master` vejo
- **Docker Hub tag**: `dev` in `dev-{commit-sha}`
- **Avtomatsko**: Brez ročne odobritve

#### Production Environment
- **Trigger**: Push na `production` vejo
- **Docker Hub tag**: `prod`, `prod-{commit-sha}`, in `latest`
- **Ročna odobritev**: DA (nastaviti je potrebno v GitHub Environments)

## 🔧 Koraki za nastavitev

### 1. Omogočitev GitHub Pages

1. Pojdite na **Settings** vašega GitHub repozitorija
2. V levem meniju izberite **Pages**
3. Pri **Source** nastavite:
   - Source: `Deploy from a branch`
   - Branch: `main` (ali `master`)
   - Folder: `/docs`
4. Kliknite **Save**

GitHub Pages bo dostopen na: `https://[username].github.io/[repository-name]/`

### 2. Nastavitev GitHub Environments

#### A. Nastavitev Development Environment

1. Pojdite na **Settings** → **Environments**
2. Kliknite **New environment**
3. Ime: `Development`
4. Kliknite **Configure environment**
5. **Brez dodatnih nastavitev** - pustite privzete nastavitve
6. Kliknite **Save protection rules**

#### B. Nastavitev Production Environment z ročno odobritvijo

1. Pojdite na **Settings** → **Environments**
2. Kliknite **New environment**
3. Ime: `Production`
4. Kliknite **Configure environment**
5. **Omogočite zaščito**:
   - ✅ Obkljukajte **Required reviewers**
   - Dodajte sebe ali člane ekipe kot reviewers (vsaj 1 oseba)
   - Opcijsko: Nastavite **Wait timer** (npr. 5 minut)
6. Kliknite **Save protection rules**

### 3. Preverjanje Docker Hub credentials

Prepričajte se, da imate nastavljene GitHub Secrets:
- `DOCKER_USERNAME`: Vaše Docker Hub uporabniško ime
- `DOCKER_PASSWORD`: Docker Hub access token ali geslo

Če še niste nastavili:
1. **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Dodajte oba secret-a

### 4. Kreiranje production veje

```bash
# Ustvarite production vejo iz main
git checkout main
git pull origin main
git checkout -b production
git push -u origin production
```

## 🚀 Kako deluje CI/CD Pipeline

### Pri push na `main` vejo:

```
Push na main
    ↓
┌─────────────────────┐
│   1. Build Job      │ ← Zgradi aplikacijo, preveri sintakso
└─────────────────────┘
    ↓
┌─────────────────────┬─────────────────────┬──────────────────────┐
│ 2. GitHub Pages     │ 3. Development      │ 5. Render Deploy     │
│    Deployment       │    Environment      │    (Optional)        │
│                     │                     │                      │
│ Deploy docs/ na     │ Build & Push na     │ Trigger Render       │
│ GitHub Pages        │ Docker Hub:         │ deployment           │
│                     │ - tag: dev          │                      │
│                     │ - tag: dev-{sha}    │                      │
└─────────────────────┴─────────────────────┴──────────────────────┘
```

### Pri push na `production` vejo:

```
Push na production
    ↓
┌─────────────────────┐
│   1. Build Job      │ ← Zgradi aplikacijo
└─────────────────────┘
    ↓
┌─────────────────────┐
│ 4. Production Env   │
│                     │
│ ⏸️  ČAKA NA ROČNO   │ ← Manual approval required
│    ODOBRITEV        │
└─────────────────────┘
    ↓ (po odobritvi)
┌─────────────────────┐
│ Build & Push na     │
│ Docker Hub:         │
│ - tag: prod         │
│ - tag: prod-{sha}   │
│ - tag: latest       │
└─────────────────────┘
```

## 📊 Testiranje

### Test 1: GitHub Pages
1. Naredite commit in push na `main`:
   ```bash
   git add docs/index.html
   git commit -m "Add GitHub Pages documentation"
   git push origin main
   ```
2. Pojdite na **Actions** in preverite, da job `Deploy to GitHub Pages` uspešno zaključi
3. Odprite GitHub Pages URL in preverite vsebino

### Test 2: Development Environment
1. Push na `main` bo avtomatsko sprožil `Deploy to Development`
2. Preverite na Docker Hub: `https://hub.docker.com/r/[username]/todo-app/tags`
3. Morali bi videti tag `dev` in `dev-{sha}`

### Test 3: Production Environment
1. Push na `production` vejo:
   ```bash
   git checkout production
   git merge main
   git push origin production
   ```
2. Pojdite na **Actions**
3. Job `Deploy to Production` bo ČAKAL na odobritev
4. Kliknite na workflow → **Review deployments** → Izberite **Production** → **Approve and deploy**
5. Po odobritvi preverite Docker Hub za tags: `prod`, `prod-{sha}`, `latest`

## 📝 Posodobitev članov ekipe

V datoteki `/docs/index.html` poiščite ta del in ga posodobite:

```html
<div class="team-members">
    <div class="team-member">
        <h3>Član 1</h3>
        <p>Razvijalec / DevOps</p>
    </div>
    <div class="team-member">
        <h3>Član 2</h3>
        <p>Frontend Razvijalec</p>
    </div>
    <div class="team-member">
        <h3>Član 3</h3>
        <p>Backend Razvijalec</p>
    </div>
</div>
```

Zamenjajte "Član 1", "Član 2", "Član 3" z dejanskimi imeni članov vaše ekipe.

## 🎯 Kontrolni seznam za oddajo

- [ ] GitHub Pages je omogočen in dostopen
- [ ] Statična stran vsebuje ime projekta, člane ekipe in opis
- [ ] Development environment je ustvarjen
- [ ] Production environment je ustvarjen z ročno odobritvijo
- [ ] Docker Hub secrets so nastavljeni
- [ ] Push na `main` ustvari `dev` tag na Docker Hub
- [ ] Push na `production` zahteva odobritev in ustvari `prod` tag
- [ ] Vsi workflow job-i uspešno zaključijo

## 🔍 Troubleshooting

### GitHub Pages ne deluje
- Preverite, da je Pages omogočen v Settings → Pages
- Preverite, da je izbran `/docs` folder
- Počakajte 1-2 minuti po prvem deployment-u

### Docker Hub push ne deluje
- Preverite GitHub Secrets (`DOCKER_USERNAME`, `DOCKER_PASSWORD`)
- Preverite, da je Docker Hub repozitorij ustvarjen (lahko je private ali public)
- Preverite workflow logs za natančnejša sporočila o napakah

### Production deployment ne čaka na odobritev
- Preverite, da je Production environment pravilno nastavljen
- Preverite, da je dodan vsaj 1 reviewer
- Preverite, da pushate na `production` vejo (ne `main`)

## 📚 Dodatne informacije

### Workflow datoteka
Glavna CI/CD konfiguracija: `.github/workflows/ci-cd.yml`

### Struktura job-ov
1. **build** - Zgradi aplikacijo in preveri sintakso
2. **deploy-pages** - Deploy na GitHub Pages (samo main)
3. **deploy-development** - Deploy na Docker Hub z dev tag (samo main)
4. **deploy-production** - Deploy na Docker Hub z prod tag (samo production, z ročno odobritvijo)
5. **deploy-render** - Deploy na Render (opcijsko, samo main)

Vse zahteve naloge so implementirane! 🎉
