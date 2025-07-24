# Build container and mount local directory to /data
```bash
docker build -t mergeicons .
docker run -it --rm -v .:/data mergeicons 
```

# Create veeam icon set for example
```bash
python /build/merge.py -o /data/veeam_iconset.svg -i /build/icons/Final/
```

# Why this way?
I cant redistribute modified version of the logo's but you can do it yourself this way. This doesn't really alter them (or at least that is the purpose), it just removes white backgrounds and transforms classes into style attributes directly
