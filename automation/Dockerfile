FROM archlinux

RUN pacman -Syy --noconfirm --noprogress
RUN pacman -Syu --noconfirm --noprogress

RUN pacman -S docker gcc git openssh ninja kicad xclip python python-pip python-wxpython python-wand python-lxml --noconfirm --noprogress
RUN python -m pip install kicad_netlist_reader numpy

COPY configure.py /ferris/automation/configure.py
COPY tools/kiplot /ferris/automation/tools/kiplot
COPY tools/ninja /ferris/automation/tools/ninja
WORKDIR ferris
RUN python -m pip install -e automation/tools/kiplot
RUN python ./automation/configure.py

RUN pacman -S xorg-server-xvfb --noconfirm --noprogress
RUN pacman -S zip --noconfirm --noprogress

ENV DISPLAY ":98"

VOLUME /workdir
WORKDIR /workdir
