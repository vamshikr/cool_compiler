class Count {
	i: Int <- 0;
	inc() : Count {
		{
			i <- i+1;
			self;
		}
	};
};


class Stock inherits Count {

	name: String; --name of iterm
};

class Main {

	a : Stock <- (new Stock).inc();
};
		
