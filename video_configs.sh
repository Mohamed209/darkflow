#!/bin/bash
echo "Download test video"
wget --header="Host: doc-0s-9s-docs.googleusercontent.com" --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" --header="Accept-Language: en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7" --header="Referer: https://drive.google.com/drive/my-drive" --header="Cookie: AUTH_u2j0t6bv6dftjmt2lsba7r3rvpi7gdis_nonce=ppp4ib98veb98" --header="Connection: keep-alive" "https://doc-0s-9s-docs.googleusercontent.com/docs/securesc/3dqr5f7kd72k46kubklelqd888nobt2a/rva5hkt43vklv63hqvi9qnmicm7ge9bq/1580998500000/11516553764628263985/01449274755406512808/1k_F39n6sHWVD3gplhVZLmY73BW2qtzrq?e=download&authuser=0&nonce=ppp4ib98veb98&user=01449274755406512808&hash=h2uh0tl1l74lm124o434blkrl8ujcdrp" -O "GP010080.mov" -c
apt-add-repository ppa:jonathonf/ffmpeg-3
apt-get update
apt-get install ffmpeg # to cut sample videos
mkdir videos/
ffmpeg -i GP010080.mov -ss 00:00:00 -t 00:00:20 videos/video_1.mp4
ffmpeg -i GP010080.mov -ss 00:01:30 -t 00:01:50 videos/video_2.mp4
ffmpeg -i GP010080.mov -ss 00:03:00 -t 00:03:20 videos/video_3.mp4
ffmpeg -i GP010080.mov -ss 00:10:00 -t 00:10:20 videos/video_4.mp4
ffmpeg -i GP010080.mov -ss 00:12:00 -t 00:12:20 videos/video_5.mp4
