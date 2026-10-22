# Additional CA certificates

Place the PEM files of CAs this API must trust here (`*.crt` or `*.pem`, one
certificate per file), typically `ca.crt` of the proxy instance. The API
calls Keycloak (signing keys) and the type service (vocabularies) under their
public `https` URLs through the proxy and needs to trust its certificate.

The files are git-ignored and this directory is on the cruft skip list. They
are added to the system trust store when the image is built, so rebuild the
image after a change. Never put private keys here: the directory is part of
the build context.
