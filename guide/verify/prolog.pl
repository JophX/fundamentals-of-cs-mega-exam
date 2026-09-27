studies(charlie, csc135).
studies(olivia, csc135).
studies(jack, csc131).
teaches(kirke, csc135).
teaches(collins, csc131).
professor(X, Y) :- teaches(X, C), studies(Y, C).
