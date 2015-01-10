-- example of static and dynamic type differing for a dispatch

class BookList inherits IO { 

    m1(hd : Book) : Cons {
		let new_cell : Cons <- new Cons in 10 * 30
    };

    m2(hd : Book) : Cons {
		let new_cell : Cons <- new Cons in 10 * 30.init()
    };
};

