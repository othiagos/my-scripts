#!/bin/zsh

file="/usr/share/applications/brave-browser.desktop"
input="TouchpadOverscrollHistoryNavigation"
features=" --enable-features=${input}"

search=$(cat $file | grep $input)

if [ -z $search ]; then
	sed -i "/Exec/{/$features/!s/$/ $features/}" "$file"
fi
