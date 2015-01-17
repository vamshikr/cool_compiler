class Object {
	
	abort() : Object {
		-- Not sure how to implement
		self
	};

	type_name() : String {
		"Object"
    };

	copy() : SELF_TYPE {
		self
	};
};

class Int inherits Object {

};

class Bool inherits Object {

};

class String inherits Object {
	length() : Int {
		0
	};
	
	concat(s : String) : String {
		self
	};

	substr(i : Int, l : Int) : String {
		self
	};
};

class IO inherits Object {

	  out_string(x : String) : SELF_TYPE {
	  	self
	  };

	  out_int(x : Int) : SELF_TYPE {
	  	self
	  };

	  in_string() : String {
	    "IO"
	  };
	  
	  in_int() : Int {
	    0
	  };
};
