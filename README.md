# csv_sorter

This is a project for work which creates a sorting function for our warehouse packing system that is not implemented by default.
It takes in a product list CSV file with product information, turns it into a dataframe and transforms certain aspects like category linking with custom zones to create a sortable list.

It creates a HTML file since I was most familiar with manipulating it to get desired visual representation of data.

sorted.py - sorts items by zones which are designated inside the file. It sorts by zone, then by product category.

unsorted.py - this is for different kind of manipulation that does not require sorting, but requires relabeling invoices and getting extra data through webscraping (later is not possible to share nor demonstrate since it contains sensitive and proprietary data.)
