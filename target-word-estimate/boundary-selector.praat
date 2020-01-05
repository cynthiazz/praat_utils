# This script reads from a boundaries text file (presumably containing a table of audio file names
# and the estimated start and end timestamps of the target word in that audio)
# and creates a text grid with the specified word boundary for each audio file.
# It then automatically saves the text grid to the directory of the audio files.

form Boundary selector
	#an absolute path, or file name if script is in the same directory
	sentence Directory /Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/8/
	sentence Boundaries_file bounds.txt
	comment Boundaries file contains [audio_file_name, start, end] on each line separated by tabs
endform

if fileReadable(boundaries_file$)
	
	boundaries$ = readFile$(boundaries_file$)
	filelen = length(boundaries$)
	# copy for iterating through the string
	file_ptr$ = boundaries$

	# each iteration parses a line (audio_file_name, start, end) from the boundaries file
	while filelen > 0
		# extract audio file name
		tab_ptr = index(file_ptr$, tab$)
		audio_file$ = left$(file_ptr$, (tab_ptr - 1))

		# decrement file pointer and filelen
		filelen = filelen - tab_ptr
		file_ptr$ = right$(file_ptr$, filelen)

		# add audio file to objects list
		Read from file... 'directory$''audio_file$'

		# stripping .wav from file name for selecting
		object_name$ = "'audio_file$'" - ".wav"

		# extract start and end timestamps
		tab_ptr = index(file_ptr$, tab$)
		start = number(left$(file_ptr$, (tab_ptr - 1)))
		newline_ptr = index(file_ptr$, newline$)
		end = number(mid$(file_ptr$, (tab_ptr + 1), (newline_ptr - 1)))

		# decrement file pointer and filelen
		filelen = filelen - newline_ptr
		file_ptr$ = right$(file_ptr$, filelen)

		# create textgrid named target for the sound file
		select Sound 'object_name$'
		To TextGrid... target

		# select the sound and textgrid file, open them together
		select Sound 'object_name$'
		plus TextGrid 'object_name$'
		View & Edit

		# select the specified boundary and add the interval to the target tier
		editor: "TextGrid " + object_name$
		    Select: start, end
		    Add on selected tier
		endeditor

		pause Adjust estimated boundaries...

		# save the textgrid
		select TextGrid 'object_name$'
		Write to text file... 'directory$''object_name$'.TextGrid

		# clean up
		select all
		Remove
	endwhile
endif