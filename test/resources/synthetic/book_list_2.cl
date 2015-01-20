-- example of static and dynamic type differing for a dispatch

class Book inherits IO {
    title : Object;

    initBook() : Book {
        {
            title <- new String;
            self;
        }
    };

};

class Silly {
   copy() : SELF_TYPE { self };
};

class Sally inherits Silly { };

class Main {
   x : Sally <- (new Sally).copy();
   main() : Sally { x };
};