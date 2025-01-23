#!/bin/bash
# To run use: bash ipm_package.bash --version x.x.x --ip_name name

# Enable safety options to turn some bugs into errors
set -o errexit -o pipefail -o nounset

# Define the options for getopt
LONGOPTS=version:,ip_name:
OPTIONS=

# Parse the options using getopt
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@") || exit 2

# Read getopt's output to handle quoting correctly
eval set -- "$PARSED"

# Initialize variables
version=""
ip_name=""

# Process the options
while true; do
    case "$1" in
        --version)
            version="$2"
            shift 2
            ;;
        --ip_name)
            ip_name="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error: unknown option $1"
            exit 3
            ;;
    esac
done

# Ensure required arguments are set
if [[ -z "$version" || -z "$ip_name" ]]; then
    echo "Error: Both --version and --ip_name options are required."
    exit 1
fi

# Output the parsed arguments
echo "+ version=$version"
echo "+ ip_name=$ip_name"


set -x

# Generate the list of files to include in the tarball
files_to_compress=$(find . \
    ! -path "./hdl" \
    ! -path "./hdl/rtl" \
    ! -path "./hdl/rtl/bus_wrappers" \
    ! -path "./hdl/rtl/bus_wrappers/dft" \
    | grep -v "\./verify" \
    | grep -v "\./ipm_package.bash" \
    | grep -v ".*\.dev\.v" \
    | grep -v "\.git" \
    | grep -v "\.tar\.gz" \
    | grep -v "\./ip" \
    | grep -v "\./docs" \
    | grep -v "\./README.md" \
    | grep -v "\.\$"; ls "./ip/dependencies.json")

# Print the files that will be compressed
echo "Files to be compressed:"
echo "$files_to_compress"

# Write the list of files to a temporary file
temp_file=$(mktemp)
echo "$files_to_compress" > "$temp_file"

# Create the tarball using the temporary file
tar czf v$version.tar.gz --files-from="$temp_file"

# Clean up the temporary file
rm -f "$temp_file"

# get checksum
shasum -a 256 v$version.tar.gz > v$version.tar.gz.sha256

# update yaml
sed -i "s/version.*/version: v$version/" *.yaml
sed -i "s/date.*/date: $(date +"%Y-%m-%d")/" *.yaml

# Extract information from YAML using sed
date=$(sed -n 's/^[[:space:]]*date:[[:space:]]*//p' $ip_name.yaml)
maturity=$(sed -n 's/^[[:space:]]*status:[[:space:]]*//p' $ip_name.yaml)
bus=$(sed -n '/^[[:space:]]*bus:/,/^[[:space:]]*type:/p' $ip_name.yaml | sed -n 's/^[[:space:]]*-[[:space:]]*//p' | paste -sd "," -)
type=$(sed -n 's/^[[:space:]]*type:[[:space:]]*//p' $ip_name.yaml)
width=$(sed -n 's/^[[:space:]]*width":[[:space:]]*//p' $ip_name.yaml)
height=$(sed -n 's/^[[:space:]]*height":[[:space:]]*//p' $ip_name.yaml)
cell_count=$(sed -n '/^[[:space:]]*cell_count:/,/^[[:space:]]*width:/p' $ip_name.yaml | sed -n 's/^[[:space:]]*-[[:space:]]*//p' | paste -sd "," -)
clock_freq_mhz=$(sed -n '/^[[:space:]]*clock_freq_mhz:/,/^[[:space:]]*digital_supply_voltage:/p' $ip_name.yaml | sed -n 's/^[[:space:]]*-[[:space:]]*//p' | paste -sd "," -)
supply_voltage=$(sed -n 's/^[[:space:]]*digital_supply_voltage:[[:space:]]*//p' $ip_name.yaml)
sha256=$(cat v$version.tar.gz.sha256 | awk '{print $1}')

# Format JSON section
json_section=$(cat <<EOF
  ,"release": {
      "v$version": {
          "date": "$date",
          "maturity": "$maturity",
          "bus": [
              "$bus"
          ],
          "type": "$type",
          "width": "$width",
          "height": "$height",
          "cell_count": "$cell_count",
          "clock_freq_mhz": "$clock_freq_mhz",
          "supply_voltage": [
              "$supply_voltage"
          ],
          "sha256": "$sha256"
      }
EOF
)


# create tag
git tag -a $ip_name-v$version -m "Release version $version"
git push origin $ip_name-v$version

# create release
set -x
if gh release view $ip_name-v$version > /dev/null 2>&1; then
    echo "Release $ip_name-v$version already exists. Skipping..."
else
    echo "Creating release $ip_name-v$version..."
    gh release create $ip_name-v$version v$version.tar.gz -t "$ip_name-v$version" --notes "$json_section"
fi
