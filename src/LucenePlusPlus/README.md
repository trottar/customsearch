Lucene++
==========

Welcome to lucene++ version **3.0.8**.

Lucene++ is a C++ port of the popular Java [Lucene](http://lucene.apache.org/)
library, a high-performance, full-featured text search engine.


Lucene++ Components
----------------

- liblucene++ library
- liblucene++-contrib library
- lucene++-tester (unit tester)
- deletefiles (demo)
- indexfiles (demo)
- searchfiles (demo)

For information on building the Lucene++ suite, please read doc/BUILDING.md


Useful Resources
----------------

Official [Java Lucene](http://lucene.apache.org/java/docs/index.html) - useful links and
documentation relevant to Lucene and lucene++. [Lucene in Action](https://www.amazon.com/dp/1932394281/)
by Otis Gospodnetic and Erik Hatcher.


To build
----------------------

```
   cd LucenePlusPlus
   mkdir build
   cd build
   cmake ..
   ccmake ..
   make -jN
   make install
```

May need to sudo make install.

To run the demos
----------------

Start by indexing a directory of files - open a command prompt and run
```
    ./indexfiles <directory to index> <directory to store index>
```
Once the indexer has finished, you can query the index using searchfiles
```
    ./searchfiles -index <directory you stored the index in>
```
This uses an interactive command for you to enter queries, type a query to search the index press enter and you'll see the results.


Acknowledgements
----------------

- Ben van Klinken and contributors to the CLucene project for inspiring this project.
- md5 Copyright (C) 1999, 2000, 2002 Aladdin Enterprises
- `Unicode character properties (guniprop)[http://library.gnome.org/devel/glib/] Copyright (C) 1999 Tom Tromey, Copyright (C) 2000 Red Hat, Inc.
- `Cotire (compile time reducer)[https://github.com/sakra/cotire] by Sascha Kratky.
