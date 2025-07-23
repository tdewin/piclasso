FROM ubuntu

RUN apt-get update -y && apt-get install emscripten build-essential make tar patch curl -y
RUN curl -L https://pikchr.org/home/tarball/trunk/pikchr.tar.gz | tar xz
WORKDIR /pikchr
COPY data-orig.patch .
RUN patch pikchr.y data-orig.patch && make all

COPY Makefile /pikchr

RUN make all

VOLUME DATA 

#docker build -t emcc .
#docker container run -it --rm -v .:/data emcc 
#docker container run -it --rm -v .:/data emcc cp /pikchr/pikchr.js /data 
#docker container run -it --rm -v .:/data emcc cp /pikchr/pikchr.c /data 