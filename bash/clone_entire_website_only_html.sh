#!/bin/bash

website = "barclays.co.uk"

# reference - https://superuser.com/questions/709702/how-to-crawl-using-wget-to-download-only-html-files-ignore-images-css-js
wget --limit-rate=200k --no-clobber --convert-links --random-wait -r -E -e robots=off -U "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36" -A html --follow-tags=a --reject '*.js,*.css,*.ico,*.txt,*.gif,*.jpg,*.jpeg,*.png,*.mp3,*.pdf,*.tgz,*.flv,*.avi,*.mpeg,*.iso' --ignore-tags=img,link,script --reject --domain=$website --url "https://www.$website"