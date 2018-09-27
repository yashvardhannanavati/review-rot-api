FROM fedora:28
LABEL maintainer="Factory 2.0"

WORKDIR /src
RUN dnf -y install \
    --setopt=deltarpm=0 \
    --setopt=install_weak_deps=false \
    --setopt=tsflags=nodocs \
    bash \
    python3-flask \
    python3-gunicorn \
    python3-six \
    && dnf clean all
# This will allow a non-root user to install a custom root CA at run-time
RUN chmod 777 /etc/pki/tls/certs/ca-bundle.crt
RUN pip3 install https://github.com/nirzari/review-rot/tarball/master#egg=review_rot
COPY . .
RUN pip3 install . --no-deps
USER 1001
CMD ["/usr/bin/bash", "-c", "./install-ca.sh && exec gunicorn-3 --bind 0.0.0.0:8080 --access-logfile=- --enable-stdio-inheritance review_rot_api.app:app"]
