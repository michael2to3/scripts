FROM accetto/debian-vnc-xfce-g3

USER 0

RUN apt-get update \
    && apt-get install -y telegram-desktop python3-dev python3-tk xdotool opencv-data python3-opencv \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://bootstrap.pypa.io/get-pip.py \
    && python3 ./get-pip.py --break-system-packages

RUN chmod 666 /etc/passwd /etc/group

USER "${HEADLESS_USER_ID}"

RUN pip3 install -r /app/requirements.txt --break-system-packages
