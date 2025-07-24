FROM python:3

VOLUME /data

WORKDIR /build

COPY merge.py /build
RUN apt-get update -y &&\
 apt-get install -y curl &&\
 curl -o icon.zip https://www.veeam.com/content/dam/veeam/global/brand-resource-center/veeam_architecture_icon.zip &&\
 unzip icon -d /build/icons


ENTRYPOINT ["/bin/bash"]

# docker build -t mergeicons .
# docker run -it --rm -v .:/data mergeicons 
# python /build/merge.py -o /data/veeam_iconset.svg -i /build/icons/Final/

