
FROM google/cloud-sdk
LABEL maintainer="Allen Day <allenday@allenday.com>"

EXPOSE 80

ENV IMAGE_PACKAGES="apache2 bwa gzip kalign tar wget build-essential"

RUN apt-get -y update
RUN apt-get -y --no-install-recommends install $IMAGE_PACKAGES

RUN apt-get -y install autoconf automake make gcc perl zlib1g-dev libz-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev libssl-dev libncurses5-dev
RUN git clone https://github.com/lh3/minimap2
RUN cd minimap2 && make
RUN cd /

# install Perl CGI module, it's not included into the standard distribution anymore
RUN curl -L https://cpanmin.us | perl - App::cpanminus
RUN cpanm install CGI

RUN a2enmod cgi

COPY fqdn.conf /etc/apache2/conf-available/fqdn.conf
RUN a2enconf fqdn

RUN mkdir -p /data

RUN rm -rf /var/lib/apt/lists/*

COPY mm2.cgi /usr/lib/cgi-bin/bwa.cgi
RUN chmod +x /usr/lib/cgi-bin/bwa.cgi

#COPY mm2.cgi /usr/lib/cgi-bin/mm2.cgi
#RUN chmod +x /usr/lib/cgi-bin/mm2.cgi

COPY kalign.cgi /usr/lib/cgi-bin/kalign.cgi
RUN chmod +x /usr/lib/cgi-bin/kalign.cgi

COPY http/apache2.conf /etc/apache2/sites-available/000-default.conf
COPY http/entrypoint.sh /entrypoint.sh

ENTRYPOINT bash /entrypoint.sh $BWA_FILES
