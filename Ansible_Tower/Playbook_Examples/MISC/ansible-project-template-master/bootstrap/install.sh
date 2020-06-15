#! /bin/bash
set -ex

ssato_repo_url_base=http://file.nrt.redhat.com/ssato/yum/fedora/
ssato_repo_release_url=$(
(grep -q 27 /etc/fedora-release && \
        echo "${ssato_repo_url_base}/27/x86_64/fedora-nrt-ssato-release-0.1.0-1.fc27.noarch.rpm") || \
(grep -q 26 /etc/fedora-release && \
        echo "${ssato_repo_url_base}/26/x86_64/fedora-nrt-ssato-release-0.1.0-1.fc26.noarch.rpm") || \
echo "UNKNOWN"
)
test ! "${ssato_repo_release_url:?}" = "UNKNOWN"

repos=$(dnf repolist)

echo "[Info] Enable the internal yum repo, fedora-nrt-ssato, required if not"
cat << EOR | grep -q fedora-nrt-ssato || sudo dnf install -y ${ssato_repo_release_url}
$repos
EOR

echo "[Info] Enable the copr yum repo required if not"
cat << EOR | grep -q ssato-python-anyconfig || sudo dnf copr enable ssato/python-anyconfig
$repos
EOR

rpms='
python3-docutils
gimp
inkscape
optipng
python3-anyconfig
python3-anytemplate
miniascape
python-docutils-exts
'

rpm -q ${rpms:?} || sudo dnf install -y ${rpms}
