# Use a minimal base image
FROM alpine:latest

# An argument to control the size of the dummy file in Megabytes (MB)
ARG DUMMY_SIZE_MB=8

# Install tools needed to create the file
RUN apk add --no-cache util-linux

# Create a dummy file of the specified size.
# 'fallocate' is very fast as it just allocates blocks without writing data.
RUN fallocate -l ${DUMMY_SIZE_MB}M /dummy_file