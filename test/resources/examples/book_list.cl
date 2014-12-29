-- example of static and dynamic type differing for a dispatch

class BookList inherits IO { 

    m1(hd : Book) : Cons {
        (let new_cell : Cons <- new Cons in
            new_cell.init(hd,self)
        )
    };

    m2(hd : Book) : Cons {
        (let new_cell : Cons <- new Cons in
       	    new_cell + 10
        )
    };

    m3(hd : Book) : Cons {
        (let new_cell : Cons <- new Cons in
       	   new_cell * 10
        )
    };

};

