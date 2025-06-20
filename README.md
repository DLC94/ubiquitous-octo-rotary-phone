# ubiquitous-octo-rotary-phone

# Semantic Release Instalation y Configuracion
1. Moverse al directorio de trabajo (repositorio git)
2. Iniciar proyecto NPM
```bash
npm init -y
```
3. Instalar semantic-release a traves de NPM
```bash
npm install --save-dev semantic-release @semantic-release/git @semantic-release/github @semantic-release/changelog @semantic-release/commit-analyzer @semantic-release/release-notes-generator conventional-changelog-conventionalcommits
```
4. Crea y Configura archivo `.releaserc.json`
```json
{
    "branches": ["main"], // corre solo cuando se modifique branch main
    "plugins": [
        [
            "@semantic-release/commit-analyzer", // analyza commit en base a preset
            {
                "preset": "conventionalcommits" // sigue estandar conventional commit
            }
        ],  
        "@semantic-release/release-notes-generator", // crea notas para release
        "@semantic-release/changelog", // genera change log de manera automatizada
        "@semantic-release/git", // permite leer commits
        "@semantic-release/github" // public tag, release, commit a branch
    ]
}
```
5. Crea archivo `CHANGELOG.md` en root del proyecto

# Release Automatizado
1. En repositorio Github > Settings > Actions > General > Workflow Permissions > Read and Write
2. Crea archivo workflow `.github/workflows/release.yml`
```yaml
name: Release CI

on:
  push:
    branches:
      - main ## corre workflow solo en push a main branch

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest # ejecuta los pasos / tasks en ubuntu
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4 # checkout repositorio (descarga ultimos cambios)
      
      - name: Setup Node JS
        uses: actions/setup-node@v4 # instala / setup npm y node 20
        with:
          node-version: 20
      
      - name: Install dependencies
        run: npm ci # instala dependencias de mi package-lock.json
      
      - name: Release with semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # token con permisos para escribir y leer en github
        run: npx semantic-release # ejecuta release
```
3. Push cambios
```bash
git push
```

# Release "Manual"
1. Exporta variable de entorno GH_TOKEN y CI
(en Github: Settings > Developers Settings > Personal access tokens > Generate new token)
```
set GH_TOKEN=github_pat_11AAASRRQ0u4gB1eDPaEXq...
set CI=true 
```
2. Push de tus cambios
```bash
git push
```
3. Corre comando sematic-release
```bash
npx semantic-release --dry-run

npx semantic-release
```

## Troubleshooting
### Error instalando semantic-release
1. Si estas dentro de la red de la oficina / svpn. Modifica archivo `.npmrc`. Agrega estas lineas

**Red oficina**
```
strict-ssl=false
proxy=http://105.102.157.11:8080
https-proxy=http://105.102.157.11:8080
registry=http://registry.npmjs.org/
```
**svpn**
```
strict-ssl=false
```

### Trabajar con Github Enterprise
1. En `.releaserc.json` agrega este codigo al plugin de Github
```json
{
    "branches": ["main"],
    "plugins": [
        [
            "@semantic-release/commit-analyzer",
            {
                "preset": "conventionalcommits"
            }
        ],  
        "@semantic-release/release-notes-generator",
        "@semantic-release/changelog",
        "@semantic-release/git",
        // nuevas codigo, especificando proxy
        [
            "@semantic-release/github",
            {
                "proxy": { "host": "105.102.157.11", "port": 8080 }
            }
        ]
    ]
}
```
2. exporta la variable de entorno GH_URL con el valor de github enterprise
```
set GH_URL=https://github.sec.samsung.net/api/v3
```
3. Si quieres usar Github Actions dentro de Github Enterprise. Crea self-hosted runner. Github Repository > Settings > Actions > Runners > New Self-hosted runner (sigue las instrucciones para descargar runner e instalarlo)