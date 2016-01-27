# Buddyfile

Sublime Text 3 plugin for displaying coupled files in two panes.

Really useful for by example loading (s)css file along with associated js file.

## Usage

Simply add a comment in master file at first line as :
// --buddyfile: ./my/relative/path/to/coupled/file

(should work with # comments)

And pointed file will be loaded and displayed in second pane  when master file is opened 
(buddy file is loaded by default but you could override that in settings)

When master file is closed, buddy file is closed to. (also overridable in settings)


## Target labels

We could add labels in buddyfile and point to it in master file :

At top of master file : `// --buddyfile: ./my/path @myLabel`

Somewhere in buddy file : `// --buddylabel: myLabel`

When buddy opens, it will scrolls to label.


## Keymap

OSX only for the moment :

ctrl+super+b :  	open or show buddy file but keep focus in master file

ctrl+super+alt+b :	open or show buddy file and focus on it

ctrl+super+shift+b : 	close buddy file 


## Todo

- Add package to package-control
- manage keymap for all plateforms

