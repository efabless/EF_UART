#!/bin/bash
# to run use bash ipm_package.bash --version x.x.x --ip_name name
# More safety, by turning some bugs into errors.
set -o errexit -o pipefail -o nounset

# now enjoy the options in order and nicely split until we see --
# option --output/-o requires 1 argument
LONGOPTS=version:ip_name:
OPTIONS=

# -temporarily store output to be able to check for errors
# -activate quoting/enhanced mode (e.g. by writing out "--options")
# -pass arguments only via   -- "$@"   to separate them correctly
# -if getopt fails, it complains itself to stdout
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@") || exit 2
# read getopt's output this way to handle the quoting right:
eval set -- "$PARSED"
unset PARSED


while true; do
    case "$1" in
        --version)
            version="$2"
            shift 2
            ;;
        --)
        --ip_name)
            ip_name="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done

echo "+ version=$version"

# zip needed files


tar czf v$version.tar.gz --files-from <(find . | grep -v "\./verify" | grep -v "\./fw/Doxyfile" | grep -v "\./ipm_package.bash" | grep -v ".*\.dev\.v" | grep -v "\./hdl/rtl/bus_wrappers/dft" | grep -v "\.git" | grep -v "\.tar\.gz" | grep -v "\./ip" | grep -v "\./docs" | grep -v "\.\$"; ls "./ip/dependencies.json")
# tar czf v$version.tar.gz \
#     --exclude='verify' \
#     --exclude='hdl/rtl/bus_wrappers/dft' \
#     --exclude='hdl/rtl/bus_wrappers/*.dev.v' \
#     --exclude='ipm_package.bash' \
#     --exclude='fw/Doxyfile' \
#     --include='*.c' \
#     *
# get checksum
shasum -a 256 v$version.tar.gz > v$version.tar.gz.sha256

# update yaml
sed -i "s/version.*/version: v$version/" *.yaml
sed -i "s/date.*/date: $(date +"%Y-%m-%d")/" *.yaml

# create tag
git tag -a $ip_name-v$version -m "Release version $version"
git push origin $ip_name-v$version

# create release
set -x
if gh release view $ip_name-v$version > /dev/null 2>&1; then
    echo "Release $ip_name-v$version already exists. Skipping..."
else
    echo "Creating release $ip_name-v$version..."
    gh release create $ip_name-v$version v$version.tar.gz -t "$ip_name-v$version" --notes "sha256: $(cat v$version.tar.gz.sha256)"
fi
