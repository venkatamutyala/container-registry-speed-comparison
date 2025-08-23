# Use a minimal base image
FROM alpine:latest

# An argument to control the size of the dummy file in Megabytes (MB)
ARG DUMMY_SIZE_MB=8

# Install tools needed to create the file
RUN apk add --no-cache coreutils

# Create a dummy file of the specified size by writing incompressible random data
RUN dd if=/dev/urandom of=/dummy_file bs=1M count=${DUMMY_SIZE_MB}
