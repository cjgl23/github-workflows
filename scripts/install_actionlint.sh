#!/usr/bin/env bash
set -euo pipefail

VERSION="1.7.12"
EXPECTED_SHA256="8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8"
DEST="${1:-${RUNNER_TEMP:-/tmp}/actionlint-bin}"
ARCHIVE="${RUNNER_TEMP:-/tmp}/actionlint_${VERSION}_linux_x86_64.tar.gz"
URL="https://github.com/rhysd/actionlint/releases/download/v${VERSION}/actionlint_${VERSION}_linux_x86_64.tar.gz"

mkdir -p "$DEST"
curl --fail --silent --show-error --location "$URL" --output "$ARCHIVE"
echo "${EXPECTED_SHA256}  ${ARCHIVE}" | sha256sum --check --strict
tar -xzf "$ARCHIVE" -C "$DEST" actionlint
chmod +x "$DEST/actionlint"
echo "$DEST" >> "${GITHUB_PATH:-/dev/null}"
"$DEST/actionlint" -version
