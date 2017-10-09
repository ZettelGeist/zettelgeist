# To use these in bash/zsh, you can source this file.
# Usage:
#   db_keywords filename.db
#   db_mentions filename.db
#
# This is for keyword/mention discoery in a zdb until we can decide on
# proper z-commands and how they would work.

zdb_keywords() {
	sqlite3 $1 'select distinct(lower(tag)) from tags' | sort -f | uniq -i
}

zdb_mentions() {
	sqlite3 $1 'select distinct(lower(mention)) from mentions' | sort -f | uniq -i
}


