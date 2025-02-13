# Use an official Debian as a parent image for a lightweight build
FROM debian:stable-slim

# Set the GNUPGHOME environment variable
ENV GNUPGHOME=/home/pguser/.gnupg

# Install PostgreSQL client and GPG
# Create a non-root user and group (using user ID 1000 and group ID 1000 for compatibility)
# Fixed commands for Debian
RUN apt-get update \
	&& apt-get install --no-install-recommends -y gnupg2=2.2.* curl=7.88.* postgresql-client-15=15.*  \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& groupadd -g 1000 pguser \
	&& useradd -m -u 1000 -g pguser pguser

# Set working directory
WORKDIR /home/pguser

# Copy the GPG public key
COPY gpg-public-key /home/pguser/gpg-public-key

# Import the GPG key
# The command to switch users before running a command has also been adjusted for Debian compatibility
RUN chown pguser:pguser /home/pguser/gpg-public-key && \
    chmod 600 /home/pguser/gpg-public-key && \
    su pguser -c 'gpg --import /home/pguser/gpg-public-key'

# Switch to the non-root user
USER pguser

