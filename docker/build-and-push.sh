#!/bin/bash

# Build and Push Script for Peer Lens AI to Quay.io
# Usage: ./build-and-push.sh
# Target: quay.io/rhdeveldocs/peer-lens

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
QUAY_USERNAME="rhdeveldocs"
IMAGE_NAME="peer-lens"
TAG="latest"
FULL_IMAGE="quay.io/${QUAY_USERNAME}/${IMAGE_NAME}:${TAG}"

echo -e "${BLUE}🚀 Building Peer Lens AI Docker Image${NC}"
echo -e "${YELLOW}Registry: quay.io${NC}"
echo -e "${YELLOW}Username: ${QUAY_USERNAME}${NC}"
echo -e "${YELLOW}Image: ${IMAGE_NAME}${NC}"
echo -e "${YELLOW}Tag: ${TAG}${NC}"
echo -e "${YELLOW}Full Image: ${FULL_IMAGE}${NC}"
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if we're in the docker directory
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}❌ Error: Please run this script from the docker directory${NC}"
    echo -e "${YELLOW}   cd docker && ./build-and-push.sh${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 Docker Layer Caching Optimization Active:${NC}"
echo -e '   ✅ Ollama installation (~200MB) - cached'
echo -e '   ✅ Llama 8B model (~4.7GB) - cached'
echo -e '   ✅ Python dependencies - cached (unless requirements.txt changed)'
echo -e '   ✅ NLP models - cached'
echo
echo -e "${YELLOW}⚠️  Only rebuilds if you changed:${NC}"
echo -e "   - App code (fast rebuild)"
echo -e "   - requirements.txt (rebuilds dependencies)"
echo -e "   - Ollama version updates"
echo

# Build the full image (with pre-downloaded model) - OPTIMIZED FOR REGULAR USERS
echo -e "${BLUE}🔨 Building full image (with pre-downloaded Llama 8B)...${NC}"
echo -e "${YELLOW}   Note: First build = 10-15 min | Subsequent builds = 1-2 min${NC}"
docker build -f Dockerfile -t ${FULL_IMAGE} ..

# Show image size
echo -e "${BLUE}📊 Image size:${NC}"
docker images | grep ${QUAY_USERNAME}/${IMAGE_NAME}

# Ask for confirmation before pushing
echo
echo -e "${YELLOW}⚠️  Ready to push to Quay.io registry?${NC}"
echo -e "${YELLOW}This will upload the images to: ${FULL_IMAGE}${NC}"
read -p "Continue? (y/N): " REPLY
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Push cancelled.${NC}"
    exit 1
fi

# Login to Quay.io
echo -e "${BLUE}🔐 Logging in to Quay.io...${NC}"
echo -e "${YELLOW}Please enter your Quay.io credentials:${NC}"
docker login quay.io

# Push the full image
echo -e "${BLUE}📤 Pushing full image optimized for regular users...${NC}"
echo -e "${YELLOW}   Note: Only changed layers get uploaded (layer caching)${NC}"
docker push ${FULL_IMAGE}

echo -e "${GREEN}✅ Successfully pushed images to Quay.io!${NC}"
echo
echo -e "${BLUE}🎉 Your image is now available at:${NC}"
echo -e "${YELLOW}Full image (optimized for regular users): ${FULL_IMAGE}${NC}"
echo
echo -e "${BLUE}📖 Users can now run your app with:${NC}"
echo -e "${GREEN}docker run -p 5000:5000 -p 11434:11434 ${FULL_IMAGE}${NC}"
echo
echo -e "${BLUE}🌐 App will be available at: http://localhost:5000${NC}"
echo -e "${BLUE}🤖 Ollama API at: http://localhost:11434${NC}"
echo
echo -e "${BLUE}💡 Next time you build, it will be much faster thanks to layer caching!${NC}" 