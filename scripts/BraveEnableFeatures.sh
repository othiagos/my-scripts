#!/bin/zsh

file="/usr/share/applications/brave-browser.desktop"
text=" --enable-features=TouchpadOverscrollHistoryNavigation"

sed -i "/Exec/{/$text/!s/$/ $text/}" "$file"
