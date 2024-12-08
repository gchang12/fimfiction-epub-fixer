_:
	for epub in queue/*.epub; do ./zipper.py "$$epub"; done;
	#./zipper.py queue/a-little-sunshine-fresh-air-never-hurt-anybody.epub;
	xreader output/*.epub;
