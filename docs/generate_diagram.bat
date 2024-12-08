:: REF: https://gitlab.com/Screwtapello/sqlite-schema-diagram/-/tree/main
sqlite3 ..\db.sqlite3 -init .\sqlite-schema-diagram.sql "" > schema.dot
dot -Tpng schema.dot > schema.png
