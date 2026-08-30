#!/usr/bin/env bash
set -euo pipefail

VERSION="0.73.0"
EXPECTED_SHA256="2edd39da482bb4e9831962487b68f68e3928ec3137794757f54d00383d79547b"
DEST="${1:-${RUNNER_TEMP:-/tmp}/trivy-bin}"
ARCHIVE="${RUNNER_TEMP:-/tmp}/trivy_${VERSION}_Linux-64bit.tar.gz"
URL="https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/trivy_${VERSION}_Linux-64bit.tar.gz"

mkdir -p "$DEST"
curl --fail --silent --show-error --location "$URL" --output "$ARCHIVE"
echo "${EXPECTED_SHA256}  ${ARCHIVE}" | sha256sum --check --strict
tar -xzf "$ARCHIVE" -C "$DEST" trivy
chmod +x "$DEST/trivy"
echo "$DEST" >> "${GITHUB_PATH:-/dev/null}"
"$DEST/trivy" --version
