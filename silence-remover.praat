# Remove long silences from all .wav files in a directory
# And creates a new trimmed copy for each
# Modified from Kathryn Flack and Shigeto Kawahara's Textgrid_helper_Praat

form Silence remover
	sentence Directory /Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/12/
	boolean generate_textgrid 0
	comment Check "generate textgrid" if you want to generate textgrids with trimming info. 
endform

# put all .wav file names in current directory into a list of strings
Create Strings as file list... list 'directory$'*.wav
numberOfFiles = Get number of strings

for ifile to numberOfFiles
	# load a .wav file name from strings list
	select Strings list
	fileName$ = Get string... ifile
	Read from file... 'directory$''fileName$'

	# remove .wav affix from file name for furthur use
	object_name$ = "'fileName$'" - ".wav"

	# select the sound file loaded and run trim silences on it
	select Sound 'object_name$'
	#params: trimDuration, onlyAtStartAndEnd, minPitch, timeStep, 
	# silenceThreshold, minSilenceDuration, minSoundingDuration, textGrid, trimLabel
	do ("Trim silences...", 0.05, 1, 100, 0, -30, 0.05, 0.09, generate_textgrid, "silence")

	# save the trimmed audio file
	trimmed_name$ = "'object_name$'" + "_trimmed"
	select Sound 'trimmed_name$'
	Write to WAV file... 'directory$''trimmed_name$'.wav

	if generate_textgrid
		select TextGrid 'trimmed_name$'
		Write to text file... 'directory$''object_name$'_triminfo.TextGrid
	endif

	select all
    minus Strings list
    Remove
endfor

select all
Remove