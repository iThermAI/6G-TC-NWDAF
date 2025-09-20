#! /bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the parent directory of SCRIPT_DIR
cd "$SCRIPT_DIR/../../oai-cn5g-nwdaf" || { echo "Failed to change directory"; exit 1; }


# Array of image details
images=(
    "oai-nwdaf-nbi-analytics:components/oai-nwdaf-nbi-analytics/docker/Dockerfile.nbi-analytics:components/oai-nwdaf-nbi-analytics"
    "oai-nwdaf-nbi-events:components/oai-nwdaf-nbi-events/docker/Dockerfile.nbi-events:components/oai-nwdaf-nbi-events"
    "oai-nwdaf-nbi-ml:components/oai-nwdaf-nbi-ml/docker/Dockerfile.nbi-ml:components/oai-nwdaf-nbi-ml"
    "oai-nwdaf-engine:components/oai-nwdaf-engine/docker/Dockerfile.engine:components/oai-nwdaf-engine"
    "oai-nwdaf-engine-ads:components/oai-nwdaf-engine-ads/docker/Dockerfile.engine-ads:components/oai-nwdaf-engine-ads"
    "oai-nwdaf-sbi:components/oai-nwdaf-sbi/docker/Dockerfile.sbi:components/oai-nwdaf-sbi"
)

# Function to build images
build_image() {
    local tag=$1
    local dockerfile=$2
    local context=$3

    echo "Building $tag..."
    docker build --network=host --no-cache \
        --target $tag --tag $tag:latest \
        --file $dockerfile $context

    if [ $? -ne 0 ]; then
        echo "Error: Failed to build $tag. Exiting."
        exit 1
    fi
}

# Loop through images
for image in "${images[@]}"; do
    IFS=":" read -r tag dockerfile context <<< "$image"
    build_image $tag $dockerfile $context
done

# Pull additional images
docker pull mongo || { echo "Failed to pull mongo. Exiting."; exit 1; }
docker pull kong || { echo "Failed to pull kong. Exiting."; exit 1; }

echo "All images built and pulled successfully."

