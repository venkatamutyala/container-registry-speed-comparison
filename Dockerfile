# Use a minimal base image
FROM alpine:latest

# An argument to control the size of the dummy file in Megabytes (MB)
ARG DUMMY_SIZE_MB=8

# Install tools needed to create the file
RUN apk add --no-cache coreutils # dd is in the coreutils package

# Create a dummy file of the specified size by writing actual zeros to it
RUN dd if=/dev/zero of=/dummy_file bs=1M count=${DUMMY_SIZE_MB}
