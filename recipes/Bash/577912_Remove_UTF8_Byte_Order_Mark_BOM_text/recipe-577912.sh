#!/bin/bash
for x in "$@"; do
 if [[ "$(file "$x")" == *UTF-8\ Unicode\ \(with\ BOM\)* ]]; then
   echo "Removing UTF-8 BOM for $x"
   # The +4 tells it to tail from the 4th byte (skipping BOM)
   tail -c +4 "$x" > "/tmp/killbom" || { echo "Failed to tail to /tmp/killbom"; exit 1; }
   mv "/tmp/killbom" "$x"
 fi
done
