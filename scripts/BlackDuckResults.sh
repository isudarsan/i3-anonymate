#!/usr/bin/env bash

GITHUB_USER="${1:-}"
GITHUB_PWD="${2:-}"
CURRENT_BRANCH="${3:-}"

# Treats unset variables as an error and causes the script to exit
set -o nounset
# Causes a pipeline of commands to fail if any command within the pipeline fails
set -o pipefail

log_prefix() {
  echo -n "$(date '+%Y-%m-%d %H:%M:%S,%3N') INFO: I3 pushToGithub.sh:"
}

echo "**Commit Black Duck Scan Results to Github**"

TEMP_FOLDER="blackduck-temp"
BLACKDUCK_FOLDER="blackduck"
IMAGE_NAME="i3-anonymate"
GIT_REPO_BLACK_DUCK="https://$GITHUB_USER:$GITHUB_PWD@git.i.mercedes-benz.com/i3/i3-blackduck-scan-results.git"

# Fetch all tags
git fetch --tags

# Get the latest git tag
LATEST_TAG=$(git tag --sort=-creatordate | head -n 1)

# Check if any tags exist
if [[ -z "$LATEST_TAG" ]]; then
    echo "No tags found in the repository."
    exit 1
fi

# Remove the 'v' prefix from the latest tag if it exists
CLEAN_TAG=${LATEST_TAG#v}

# Get the numeric parts of the latest tag (assumes it is of the form X.Y.Z)
IFS='.' read -r major minor patch <<< "$CLEAN_TAG"

# Increment the minor version
NEXT_MINOR=$((minor + 1))
NEXT_TAG="$major.$NEXT_MINOR.0"  # Reset patch version to 0 for the new tag

# Clone black duck repo
git clone "$GIT_REPO_BLACK_DUCK" "$BLACKDUCK_FOLDER"
# Check if the clone was successful
if [ $? -eq 0 ]; then
    echo "Repository cloned successfully into $BLACKDUCK_FOLDER"
    # Change to BD directory
    cd "$BLACKDUCK_FOLDER" || exit
else
   echo "Git clone was not succesful. Cloning into another folder."
   git clone "$GIT_REPO_BLACK_DUCK" "$TEMP_FOLDER"
   # Change to BD directory
   cd "$TEMP_FOLDER" || exit
fi

# Declare variables
FOLDER_NAME="$NEXT_TAG"
echo "current tag: ${FOLDER_NAME}"
date=$(date +%Y-%m-%d_%H-%M-%S)
NOTICES_FILE_OLD="LICENSE-3RD-PARTY.txt"
NOTICES_FILE_NEW="${IMAGE_NAME}-${FOLDER_NAME}-$date.zip"
RISK_REPORT="I3_AnonyMate_I3_AnonyMate_${CURRENT_BRANCH}_BlackDuck_RiskReport.pdf"
RISK_REPORT_NEW="${IMAGE_NAME}-${FOLDER_NAME}-risk-report.pdf"
SCAN_FILE="i3_anonymate.bdio"
SCAN_FILE_NEW="${IMAGE_NAME}-${FOLDER_NAME}-$date.bdio"
SCAN_FOLDER="${IMAGE_NAME}/${FOLDER_NAME}/scans"
REPORTS_FOLDER="${IMAGE_NAME}/${FOLDER_NAME}/reports"

# If directory does not exist, then create
if [[ ! -d "$IMAGE_NAME/$FOLDER_NAME" ]]; then
  mkdir -p "$IMAGE_NAME/$FOLDER_NAME"
fi

if [[ ! -d "$SCAN_FOLDER" ]]; then
  mkdir -p "$SCAN_FOLDER"
fi

if [[ ! -d "$REPORTS_FOLDER" ]]; then
  mkdir -p "$REPORTS_FOLDER"
fi

# Zip notices file
zip -j "$NOTICES_FILE_NEW" "../$NOTICES_FILE_OLD"
# Steps to move into desired directory
echo "moving risk report"
mv "../$RISK_REPORT" "$RISK_REPORT_NEW"
mv "$RISK_REPORT_NEW" "$REPORTS_FOLDER"
echo "moving notice report"
mv "$NOTICES_FILE_NEW" "$REPORTS_FOLDER"
echo "moving bdio file"
mv "../$SCAN_FILE" "$SCAN_FILE_NEW"
mv "$SCAN_FILE_NEW" "$SCAN_FOLDER"

# Commit and push to GitHub
git config user.email "i3.consulting@mercedes-benz.com"
git config user.name "I3 Team B"

git add "$SCAN_FOLDER"/"$SCAN_FILE_NEW"
git add "$REPORTS_FOLDER"/"$NOTICES_FILE_NEW"
git add "$REPORTS_FOLDER"/"$RISK_REPORT_NEW"

git commit -m "Add scan results for Black Duck"
git push -u origin master