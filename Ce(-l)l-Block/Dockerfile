FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y openssh-server sudo && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash user && \
    echo 'user:user' | chpasswd && \
    mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN echo "user ALL=(root) NOPASSWD: /usr/bin/find" > /etc/sudoers.d/user && \
    chmod 0440 /etc/sudoers.d/user
RUN echo "SKL{5ud0_1n53cur1ty_4ll0w5_f1nd_3xpl01t}" > /root/flag.txt && \
    chmod 600 /root/flag.txt
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

