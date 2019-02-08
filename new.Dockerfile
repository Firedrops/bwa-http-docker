FROM google/cloud-sdk
LABEL maintainer="Larry Cai <larrycai.jpl@gmail.com>"
# Original Builder="Allen Day <allenday@allenday.com"

EXPOSE 443

ENV IMAGE_PACKAGES="apache2 bwa gzip kalign tar wget"

RUN apt-get -y update
RUN apt-get -y --no-install-recommends install $IMAGE_PACKAGES

RUN apt-get install autoconf automake make gcc perl zlib1g-dev libz-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev libssl-dev libncurses5-dev
RUN apt install python3-pip -y
RUN apt install vim -y
RUN git clone https://github.com/lh3/minimap2
RUN cd minimap2 && make
RUN cd /
RUN git clone https://github.com/samtools/htslib
RUN cd htslib && make
RUN cd /
RUN git clone git://github.com/samtools/samtools.git
RUN cd samtools
RUN autoheader
RUN autoconf -Wno-syntax
RUN ./configure
RUN make
RUN make install
RUN apt-get install pip
RUN cd /

RUN a2enmod cgi
RUN a2enmod ssl

COPY fqdn.conf /etc/apache2/conf-available/fqdn.conf
RUN a2enconf fqdn

RUN mkdir -p /data
RUN mkdir -p /etc/apache2/ssl

RUN rm -rf /var/lib/apt/lists/*

COPY bwa.cgi /usr/lib/cgi-bin/bwa.cgi
RUN chmod +x /usr/lib/cgi-bin/bwa.cgi

COPY kalign.cgi /usr/lib/cgi-bin/kalign.cgi
RUN chmod +x /usr/lib/cgi-bin/kalign.cgi

COPY apache2.conf /etc/apache2/sites-available/000-default.conf
COPY ssl-info.txt /tmp/ssl-info.txt
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT bash /entrypoint.sh $BWA_FILES
