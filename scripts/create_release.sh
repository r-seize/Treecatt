#!/bin/bash
# Script pour créer une nouvelle release de TreeCatt

set -e

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌳 TreeCatt Release Script${NC}\n"

# Vérifier que nous sommes sur la branche main
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${RED}❌ Erreur: Vous devez être sur la branche 'main' pour créer une release${NC}"
    echo "   Branche actuelle: $CURRENT_BRANCH"
    exit 1
fi

# Vérifier qu'il n'y a pas de changements non commités
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}❌ Erreur: Il y a des changements non commités${NC}"
    echo "   Commitez ou stashez vos changements avant de continuer"
    git status --short
    exit 1
fi

# Récupérer la dernière version
CURRENT_VERSION=$(grep 'version = "' pyproject.toml | head -1 | cut -d'"' -f2)
echo -e "📌 Version actuelle: ${YELLOW}$CURRENT_VERSION${NC}"
echo ""

# Demander la nouvelle version
echo -e "${BLUE}Quelle est la nouvelle version ?${NC}"
echo "   Format: MAJOR.MINOR.PATCH (ex: 0.2.0)"
echo "   Types:"
echo "   - MAJOR: Changements incompatibles"
echo "   - MINOR: Nouvelles fonctionnalités rétrocompatibles"
echo "   - PATCH: Corrections de bugs"
echo ""
read -p "Nouvelle version: " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    echo -e "${RED}❌ Erreur: Version vide${NC}"
    exit 1
fi

# Valider le format de version
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}❌ Erreur: Format de version invalide${NC}"
    echo "   Utilisez le format: MAJOR.MINOR.PATCH (ex: 0.2.0)"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Version validée: $NEW_VERSION${NC}"
echo ""

# Demander le type de release
echo -e "${BLUE}Type de release :${NC}"
echo "   1. Release normale (stable)"
echo "   2. Pre-release (beta, rc)"
read -p "Choisissez (1 ou 2) [1]: " RELEASE_TYPE
RELEASE_TYPE=${RELEASE_TYPE:-1}

IS_PRERELEASE="false"
if [ "$RELEASE_TYPE" = "2" ]; then
    IS_PRERELEASE="true"
fi

# Résumé des changements
echo ""
echo -e "${BLUE}Décrivez les changements principaux de cette release:${NC}"
echo "   (Une ligne par changement, ligne vide pour terminer)"
echo ""

CHANGES=""
while IFS= read -r line; do
    [ -z "$line" ] && break
    CHANGES="${CHANGES}- ${line}\n"
done

# Confirmation
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 Résumé de la release${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Version actuelle:  ${CURRENT_VERSION}"
echo -e "Nouvelle version:  ${GREEN}${NEW_VERSION}${NC}"
echo -e "Type:              $([ "$IS_PRERELEASE" = "true" ] && echo "Pre-release" || echo "Stable")"
echo -e ""
echo -e "Changements:"
echo -e "${CHANGES}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
read -p "Continuer avec cette release ? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Release annulée${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}🚀 Création de la release...${NC}"
echo ""

# 1. Mettre à jour pyproject.toml
echo -e "${YELLOW}📝 Mise à jour de pyproject.toml...${NC}"
sed -i.bak "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml && rm pyproject.toml.bak

# 2. Mettre à jour __init__.py
echo -e "${YELLOW}📝 Mise à jour de src/treecatt/__init__.py...${NC}"
sed -i.bak "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" src/treecatt/__init__.py && rm src/treecatt/__init__.py.bak

# 3. Mettre à jour setup.py
echo -e "${YELLOW}📝 Mise à jour de setup.py...${NC}"
sed -i.bak "s/version         = \"$CURRENT_VERSION\"/version         = \"$NEW_VERSION\"/" setup.py && rm setup.py.bak

# 4. Mettre à jour cli.py
echo -e "${YELLOW}📝 Mise à jour de src/treecatt/cli.py...${NC}"
sed -i.bak "s/%(prog)s $CURRENT_VERSION/%(prog)s $NEW_VERSION/" src/treecatt/cli.py && rm src/treecatt/cli.py.bak

# 5. Mettre à jour install.sh et build_deb.sh
echo -e "${YELLOW}📝 Mise à jour des scripts...${NC}"
sed -i.bak "s/VERSION=\"$CURRENT_VERSION\"/VERSION=\"$NEW_VERSION\"/" install.sh && rm install.sh.bak
sed -i.bak "s/VERSION=\"$CURRENT_VERSION\"/VERSION=\"$NEW_VERSION\"/" build_deb.sh && rm build_deb.sh.bak

# 6. Commit des changements
echo -e "${YELLOW}📦 Commit des changements...${NC}"
git add pyproject.toml src/treecatt/__init__.py setup.py src/treecatt/cli.py install.sh build_deb.sh
git commit -m "chore: bump version to $NEW_VERSION"

# 6. Créer le tag
echo -e "${YELLOW}🏷️  Création du tag v$NEW_VERSION...${NC}"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION

${CHANGES}"

# 7. Exécuter les tests
echo -e "${YELLOW}🧪 Exécution des tests...${NC}"
if command -v pytest &> /dev/null; then
    pytest || {
        echo -e "${RED}❌ Les tests ont échoué!${NC}"
        echo "   Annulation du tag..."
        git tag -d "v$NEW_VERSION"
        git reset --hard HEAD~1
        exit 1
    }
else
    echo -e "${YELLOW}⚠️  pytest non installé, tests ignorés${NC}"
fi

# 8. Build des packages
echo -e "${YELLOW}🔨 Build des packages...${NC}"
make clean
make release

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Release v$NEW_VERSION créée avec succès!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📦 Fichiers créés:${NC}"
ls -lh dist/

echo ""
echo -e "${BLUE}🚀 Prochaines étapes:${NC}"
echo ""
echo -e "1. ${YELLOW}Vérifier les packages générés${NC}"
echo "   cd dist/ && ls -lh"
echo ""
echo -e "2. ${YELLOW}Pousser vers GitHub${NC}"
echo "   git push origin main"
echo "   git push origin v$NEW_VERSION"
echo ""
echo -e "3. ${YELLOW}Créer la release sur GitHub${NC}"
echo "   - Aller sur https://github.com/r-seize/TreeCatt/releases/new"
echo "   - Sélectionner le tag v$NEW_VERSION"
echo "   - Attacher les fichiers de dist/"
echo "   - Publier"
echo ""
echo -e "4. ${YELLOW}(Optionnel) Publier sur PyPI${NC}"
echo "   twine upload dist/*.whl dist/*.tar.gz"
echo ""
echo -e "${GREEN}🎉 Félicitations pour cette nouvelle release!${NC}"