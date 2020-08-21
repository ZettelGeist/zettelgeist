---
layout: page
title: Tutorial-Terminal
permalink: /tutorial-term/
---

\[**ZettelGeist documentation is in development and split between this page and the [User's Guide](/gs).]**

# Notetaking with ZettelGeist: a workflow

**First, create a template card.**
This is the starting point for notetaking: create a "template" note that you can use to take a series of notes (zettels) on a particular source (book, article, etc.). 
The subsequent commands will then lead you through various ways to create new notes and adjust tags.

```shell
(zenv) $ zettel --set-title "My Favorite Ada and Charles Book" --append-tags "Charles Babbage" "Ada Lovelace" "Victorian Era" --set-cite Campbell_Kelly_2010 "pp. 1-2" --save campbell-kelly-template.yaml 
```

View the file: 

```shell
$ cat campbell-kelly-template.yaml
```

Now create a new zettel but (1) change the page numbers, (2) prompt for a note, and (3) save the note with a unique identifier:

```shell
$ zettel --file campbell-kelly-template.yaml --set-cite "" "pp. 2-4" --prompt-note --id campbell-kelly --counter campbell-kelly --name id counter
```

When entering the `note`, avoid a trailing space at the end of lines. This will result in `\n` between lines.
Special characters will cause ZettelGeist to go to "safe" format and add backslashes `\`. The note will look ugly, but it will work. 

To take a sequence of notes on a source, use the up arrow or `ctrl p` to retrieve the previous command, then edit the command as needed.
For example, retrieve the previous command and add a new tag and page numbers:

```shell
$ zettel --file campbell-kelly-template.yaml --append-tags "Analytical Engine" --set-cite "" "pp. 4-5" --prompt-note --id campbell-kelly --counter campbell-kelly --name id counter
```

(Alternatively, use `ctrl r` to search and retrieve a command from your shell history.)

The `prompt-<FIELD>` command can be used for tags: 

```shell
$ zettel --file campbell-kelly-template.yaml --set-cite "" "p. 33" --prompt-note --prompt-tags --id campbell-kelly --counter campbell-kelly --name id counter
```

This will have you enter a note and tags on the command line.
The command `--prompt-cite` will ask for both `bibkey` and `page`, so you would need to keep entering `bibkey`.
Most users will prefer the syntax `--set-cite "" "PAGE"`, which lets you change the page number while reusing the `bibkey` entered in the template file.

The command `--reset-tags` deletes tags from the template file; 
`--prompt-tags` prompts you to add new ones:

```shell
$ zettel --file campbell-kelly-template.yaml --set-cite "" "p. 33" --reset-tags --prompt-note --prompt-tags --id campbell-kelly --counter campbell-kelly --name id counter
```


<!--
- George uses prompt mainly for note:  For the rest, he uses set. 
-->

<!--
# Process Notes
[**The remainder of this document is internal process notes**]

# Search results

Results have dashed lines between each 

-------------------------------

[TODO: This line could be a configurable option... Make this configurable?]

[TODO: next tool is a report, with a way to style what you see. Make each field name a markdown heading.] 

[TODO: add zFind command option to make headings into markdown. Put everything into a nice markdown format.] 

## To have _just_ the basic stuff to pull into a document, just include 

- notes and citations are really all you need if you search on good tags that you have created. 

```
zfind --database index.db --find-tags "babbage" --show-note --show-cite 
```

- Then you would just get the notes (maybe commments and summary too, and citation for the material tagged as "babbage."  This could be copied or read right into a file or section of an outline.  Clean, with just the material so tagged. 

- THIS IS the way to get things out of the system!!!! 

[TODO: reporting... and turning citations into proper citations.  Turn it into something pandoc friendly and pandoc plus cite.]  

[TODO: future lecture process for teaching -- do zfind on everything on a topic. then just go through the results.   This is the memory extender that lets you pull up information through a retrieval system.   The retrieval system is what is the new and the best of the system.  This is what Onenote is lacking. ] 


# Some recipes for using VIM to make Zettel commands and work with PDFS.

### Use VIM to edit command

In Oh-My-Zsh: add "vi-mode" to plugins in .zshrc   [plugins=(git vi-mode)]

Set up first command [save for future use]

```
zettel --set-title "Notes on Tedre" --set-cite tedre_science-2014 "0" --set-note "First note on Tedre" --set-comment "First note" --append-tags  "Tedre" "General computer history" --now --now-id tedre-science
```

Repeat [up arrow]
Hit [esc-v] to edit in VIM [move quickly to delete all between quotation marks, etc. Replace tags, comments, page number, note, etc.]

ci"    will replace everything within quotation marks.  [Do this between note: and page: and tags:]

```
:wq 
[enter]
```
Arrow up, REPEAT endlessly

# Alias to zcreate database [alias "zcreatetoday"]

```
zcreate --database Zettels-Today.db"
```

zcreate --database Zettels-Today.db"
## Alias to zimport into new database

```
alias zimporttoday="zimport --database Zettels-Today.db --zettel-dir ~/zettels/hocz/dbdz"
```

## zFilter 

- Create query file "zql" 

```
title:Campbell & ( note:"Charles Babbage" | note:"Ada Lovelace") 
```

save as charles-and-ada.zql 

- zql = Zettel Query Language

```
zfilter --database index.db --query docs/zquery-examples/charles-and-ada.zql --count 
```

[TODO: --count doesn't really do much for a zfilter command... still produces all the yaml.in cards.  Better to zfind to count, then zfilter?]

[TODO: results on yaml.in still read as "zfind" results, rather than "zfilter" results... Minor detail to fix ] 

[TODO: default name suffix for a zfilter folder is "-zfind".  This should be changed to "-zfilter"]

[TODO: Can URL go into cite?  Or should we make bibcard with bibkey for all videos and add url there?]

- Add, for instance... 

```
--show-filename
```

```
--show-note 
```

```
--show-note | less
```

/ada to search less to see just Ada, etc. 

/Babbage to search less to see just Babbage... 

## Adjust query 

- edit charles-and-ada.zql to 

```
title:Campbell & ( note:"Charles Babbage" | note:"Ada Lovelace") & note:"programming language" 
```

- save as new query 

```
charles-and-ada+programming.zql
```

- Do same zFilter as above... fewer results, etc. 

## Use Zettel command for "replace" 

- Copy filepath/filename from the results of the search

- pass that into 

```
zettel --file [filepath/filename.yaml] 
```

```
--append tags "programming language"
```

- That adds the new tag to the end of that yaml.

- Save as a new zettel by adding 

```
--now -now-id ada-programming
```

- This creates new zettel with new tag at the end.

## Adding tags to multiple Zettels 

- To get list of filenames from a set of query results, use grep

```
zfilter --database index.db --query docs/zquery-examples/charles-and-ada.zql --count --show-filename | grap filename: 
```

- This gives list of all the files that were found. 

```
zfilter --database index.db --query docs/zquery-examples/charles-and-ada.zql --count --show-filename | grap filename: | cut -f2 -d" "
```

- This cuts off the "filename:" part to give list of files 

- This could all be in a for loop:  

```
for filename in $(zfilter --database index.db --query docs/zquery-examples/charles-and-ada.zql --count --show-filename | grap filename: | cut -f2 -d" "); do 
zettel --file $filename --now --now-id "new id" --append-tags "programmming languages "demo for Dave" 
done 
```

- This will create new zettels with the new tags added to all of the zettels found with the original query.  

[Taking the results of the command, just filenames, to create new "pile" of zettels with the new tags.]   

- Zettel command a way to edit any zettel.  Supports adding a tag, not deleting a tag.  Removing may came later. 

- Use it to pipe through results from zFilter, or zFind. 

[TODO: Now that zFilter creates note.txt, title.txt, ... and yaml.in, how would you make a "for loop" to create zettels with new tags for all of the results? [Which is what you were doing at this stage?]]

## How to create zql files with prompt

```
zfilter [or zfind?] --database index.db --prompt --save-query quantum-computing.zql 
```
- This will prompt for the search you want to do, for instance: 

```
zquery> note:"quantum computing" & note:"Seth Lloyd"
```

- That will create a valid zql file.

[TODO: Does this still work with zfilter?  It seems to create a yaml.in directory file in addition to a zql file.]

Now do search:  

```
zfind [or zfilter?] --database index.db --query quantum-computing.zql --count --show-filename --show-title --show-note 
```

## To put into text file

add > new-filename.md 

```
zfind [or zfilter?] --database index.db --query quantum-computing.zql --count --show-filename --show-title --show-note > quantum-computing-textfile.md 
```

## For Loop

As we do a search we want to add tag to all the zettels. Then we don't have to worry about the query again...

## Add bibtex

```
--show-bibtex
```
```
--show-cite  
```

# 2017-12-29 12.25.52 ZG INSTRUCTIONS

```
zfind --database index.db --query docs/zquery-examples/charles-and-ada.zql --count --show-note --show-summary --show-bibtex --use-index --output charles-and-ada [folder name]
```

- Inside the results... create new zettels with new title and new tags... 

```
for filename in *.yaml
do
zettel --file $filename --now --now-id charles+ada --append-tags "Charles Babbage" "Ada Lovelace" --set-title "Thoughts for Chapter 1" 
done
```

- This will let us do anything with the Zettels - add tags, (delete/replace?], etc. 

[TODO: now that zfilter creates note.txt and yaml.in files, this doesn't work... How would one just make yamls out of "hits" from zfilter or zfind? I assume it would mean writing loop that passes both yaml.in and note.txt somehow--as below.]

## See everything in a folder 

```
less | *.yaml 
cat folder/*.yaml |less
```
## 2018-01-03 11.04.04 ZG INSTRUCTIONS

```
zimport --database index.db $(pwd)/docs  
```

- That would only do docs folder.... 

```
zfilter --database index.db --query docs/zquery-examples/kurzweil2.zql --count --show-title --show-summary --show-cite --output kurzweil-singularity 
```

- Go into folder 

filename.Note.txt files for results in notes field
title.txt for results in title
summary.txt for results in summary, etc.
yaml.in files for the yaml associated with each

yaml.in 
shows what the query was 

filename 
says where to see the actual snippets
includes cite: if in original...

note.txt file has "snippets" and the filename and the field name they came from. 

- Make a zettel out of it.  

```
zettel --file name.yaml.in --load-note name.note.txt 
```

- Result is zettel which joins the yaml.in with the note.txt that has only the snippets with the selections from the book!  

[Putting it into a text file makes it easier than moving from yaml to yaml...]

- Something for amusement purposes

```
for filename in *.yaml.in
do
rootname=$(basename $filename .yaml.in)
zettel --now --now-id new-zettel --append-tags "searched notes" --load-note $rootname-note.txt
done
```

- This would create yamls from all the fragments from the search results... And it will add a new name indicating this and a new tag. Haha. 

- Then you would have yamls of each snippet set with the correct cite, etc.  

## - To just do "human" in the title.

- Change zql file

```
title:Human & note:Kurzweil & note:singularity 
```
- Run search again

- then you will have 

note.txt
title.txt
yaml.in 

## To create zettel from _each_ or just one of the found snippet sets at a time.

- for each set

```
zettel --file filename.yaml.in --load-note filename.note.txt --load-title filename.title.txt 
```

-same thing with real content

```
zettel --file 20180205130743-09.yaml.in --load-note 20180205130743-09-note.txt --now --now-id new-note-from-snippets-in-09.txt
```

- same thing, and add tag indicating content of that snippet set

```
zettel --file 20180205130743-09.yaml.in --load-note 20180205130743-09-note.txt --now --now-id new-note-from-snippets-in-09.txt --append-tags "new zettel from a single set of snippets"
```

- that would create zettel with all of the found material from note and other zettel info... 

- The note is where the details are.  But you may want to see summary too, etc. Could add --load-title --load-summary --load-comment --load tags, etc.  Can see snippets whereever, but main target is note or comments.  

## Create zettel from just an interesting part of a snippet 

- Read note.txt on console using cat

- copy what you want 

```
zettel --file filename.yaml.in --prompt-note --prompt-summary --now 
```
- follow prompt to write summary and past in the note that you copied. 

[no editor] 

## Limited indexing  

```
zcreate --database new-research.db
zimport --database new-research.db --dir $(pwd)/foldername 
```

- this would just do the folder indicated after $(pwd)

## Filing things in right places

- copy new yamls from studying zfilter results into another directory  

- delete notes.txt delete yaml.in  [They won't be indexed anyway, but they can be deleted after you are done studying them and creating yamls, in various ways.] 

- Actually create the zettels in second session in preferred hocz directory... 

- Specify location of zettel creation 

```
zettel --save /temp/blank.yaml
```

- Just can't do that AND --now   

(That could be a feature added later)

[TODO: Make it possible to do a cite without a page number...]


## Creating Queries:

& and
| or
! not 

## Whole section on creating bibcards... 

But we ran into some problems....

# 2018-01-12 11.11.15 ZG INSTRUCTIONS

Dave demonstrating Voom to George...   

# SOME OTHER Examples of using Zfilter 

## First create database and index it

```
zcreate --database index.db
zimport --database index.db --dir $(pwd)
```
## Example 0 

- show note for filtered results, but limit to 1000 character context 

```
zfilter --database index.db --query iPhone4.zql --count --show-title --show-note --snip-size 1000 --output iPhone4-search
```

## Example 1

- do basic zfilter search, put all results into a .txt file to 

```
zfilter --database index.db --query ~/Work/zettels/zfiltering/zql-files/kurzweil2.zql --count --show-title --show-note --show-summary --show-cite --show-url --output kurzweil-singularity
```

- Move into created directory

```
cd 20180105135229-kurzweil-singularity
```

- to look at all the results in same file

```
more *.txt > results.txt
```

- open results.txt to copy the parts you like [if you are using VIM, the command is "+y to copy into shared register so you can paste into the prompt] then create zettel and paste selection into "note" prompt

```
zettel --file 20180105135229-01.yaml.in --prompt-note --prompt-comment --prompt-tags --now --now-id Testing-new-zFilter
```

- take note of the correct note.txt file that you are working with and adjusting the yaml.in filename accordingly

## Example 2

- make sure you include --show-cite to get full bibkey and page 

- include --show-url to get url of videos referenced

- pick preferred snip size

```
zfilter --database ~/Work/zettels/index.db --query ~/Work/zettels/zfiltering/zql-files/Apollo-Guidance-Computer.zql --count --show-title --show-note --show-summary --show-cite --show-url --snip-size 3000 --output Apollo-Guidance-Computer
```


- Inside the directory created, /20180131113830-Apollo-Guidance-Computer, open the "note.txt" files with VIM to study and select. 

- [if you are using VIM, the command is "+y to copy into shared register so you can paste into the prompt]

- Open another terminal session and go into the directory where you want to create zettels. [hocz/dbdz or gktz]  Then you can create zettels there, referring back to this zfiltering directory. 

- To do this, make sure you use full file location for the yaml information. [readlink -f filename will give it to you].  

```
zettel --file ~/Work/zettels/zfiltering/20180131113830-Apollo-Guidance-Computer/20180131113830-58.yaml.in --prompt-note --prompt-comment --prompt-tags --now --now-id Testing-new-zFilter

```
- Again, as you look at different note.txt files for results, change the _number_ of the yaml.in file accordingly... Just the last digits. 

- Then you can just go through and create notes based on the filtered results. 

## Example 3

- Do a zfilter.  Select a portion of one [inside vim or from cat], and create a new card that will include the zettel information from the original, but prompt for you to paste in the portion you want, and comment about it. 

```
zfilter --database ~/Work/zettels/index.db --query ~/Work/zettels/zfiltering/zql-files/Apollo-Guidance-Computer.zql --count --show-title --show-note --show-summary --show-cite --show-url --snip-size 3000 --output Apollo-Guidance-Computer
ls
cd 20180109115129-Apollo-Guidance-Computer
ls
vim 20180109115129-58-note.txt
zettel --file ~/Work/zettels/zfiltering/20180109115129-Apollo-Guidance-Computer/20180109115129-58.yaml.in --prompt-note --prompt-comment --prompt-tags --now --now-id Testing-new-zFilter
```

## Example 4 

- Tried some zfinds just to see basic results -- how many zettels have some information.... 

```
zfind --database index.db --find-note "Second World War Zuse Computer Nazi Hitler Rocket" --count --show-title --show-filename --show-cite
```

- went to Work/zettels/zfiltering/zql-files 

- opened VIM and added 


note:"Second World War" & note:Zuse & note:Computer & note:Nazi & note:Hitler & note:rocket

- saved as Second-World-War-Zuse-Computer-Nazi-Hitler-Rocket.zql

- did zfilter [Reduced snip size for this one...] 

```
zfilter --database ~/Work/zettels/index.db --query ~/Work/zettels/zfiltering/zql-files/Second-World-War-Zuse-Computer-Nazi-Hitler-Rocket.zql --count --show-title --show-note --show-summary --show-cite --show-url --snip-size 300 --output Second-World-War-Zuse-test
```



## Example 4 

- Taking the next step to use zFind to find some material. 


```
zfind --database index.db --find-note "saved the Apollo team from prematurely aborting the mission" --show-filename --show-note | less
```

- searched for passage using /saved 

- highlighted and copied passage

- created zettel

```
zettel --prompt-note --prompt-comment --prompt-tags --now --now-id Saving-Apollo
Zettel saved to 20180131133145-Saving-Apollo.yaml
Enter text for comment. ctrl-d to end.
comment> This is a note I am creating to test process.
comment> 
Enter text for note. ctrl-d to end.
note> Their solution was to just ignore the errors since the AGC would free up memory on it's own by terminating non-critical programs through a reboot. Garman and Bale's quick-thinking saved the Apollo team from prematurely aborting the mission. While we may look at those errors as glitches in the AGC, but in reality the computer was behaving exactly as it was designed to. The near disaster the Apollo team encountered is a testament to the ingenuity of the AGC engineering team and training of the mission crew.
note> 
Enter text for tags. ctrl-d to end.
tags> Test
tags> Apollo
tags> 
```

- create Markdown from that zettel 

```
zettel --save Saving-Apollo.md --file 20180131133145-Saving-Apollo.yaml
Zettel being saved to Saving-Apollo.md (mode = .md)
```


- import into a .md file using VIM and VOoM.

```
VIM 
:r 
tab to filename
enter
```

- File entered into Vim with .md


```
comment
=======

This is a note I am creating to test process.


note
====

Their solution was to just ignore the errors since the AGC would free up memory on it's own by terminating non-critical programs through a reboot. Garman and Bale's quick-thinking saved the Apollo team from prematurely aborting the mission. While we may look at those errors as glitches in the AGC, but in reality the computer was behaving exactly as it was designed to. The near disaster the Apollo team encountered is a testament to the ingenuity of the AGC engineering team and training of the mission crew.


tags
====

- Test
- Apollo
```


## Example 6 

- zfind some notes, and automatically put them into a new zettel...[used semi-colon to combine]  

```
zfind --database ~/Work/zettels/index.db --find-note "saved the Apollo team from prematurely aborting the mission" --show-filename --show-cite > test.md; zettel --load-note test.md --prompt-title --prompt-comment --now --now-id test-piping
```

## Example 7 

- OR, use zfind to get notes, then use zettel to create a markdown file out of them.  [Used semi-colon to combine.] Pass zfind results to Markdown using Zettel!! Write to a temp file, then load that and save with zettel.  Use semi-colon to combine .  

```
zfind --database ~/Work/zettels/index.db --find-note "saved the Apollo team from prematurely aborting the mission" --show-filename --show-cite > test.md; zettel --load-note test.md --prompt-title --prompt-comment --save piping-test-save.md

Zettel being saved to piping-test-save.md (mode = .md)
Enter text for title. ctrl-d to end.
title> a title
title> 
Enter text for comment. ctrl-d to end.
comment> a comment
comment> 
```



# Commands from Zoom Demonstration Video 20180206 Updated zettel zfind zfilter recipes 

## Getting started 

```
zcreate --database mlb.db
zimport --database mlb.db --dir $(pwd)
ls
```

## Zfind basics

```
zfind --database mlb.db --find-note "World Series" --count
zfind --database mlb.db --find-note "World Series" --show-summary --count
zfind --database mlb.db --find-note "World Series" --show-summary --show-note --count
zfind --database mlb.db --find-note "World Series" --show-summary --show-note --show-cite --count
```

## 

```
ls
ls baseball
ls bibs
more bibs/chicago-cubs.yaml
zfind --database mlb.db --find-bibkey chicago --show-bibkey
```

##

```
zettel --set-title "George's scholarly notes about the Chicago Cubs" --prompt-summary --prompt-cite
cat > chicago-cubs-gkt-notes.yaml
ls
mkdir gkt-musings
mv chicago-cubs-gkt-notes.yaml gkt-musings
ls
```

##

```
rm mlb.db
zcreate --database mlb.db
zimport --database mlb.db --dir $(pwd)
zfind --database mlb.db --find-summary "lovable losers" --show-summary
zfind --database mlb.db --find-summary "Cubs" --show-summary
zfind --database mlb.db --find-note "Cubs" --show-note
zfind --database mlb.db --find-note "Cubs" --show-note  --show-title
zfind --help
zfind --database mlb.db --find-note "Cubs" --show-note --show-title
zfind --database mlb.db --find-note "Cubs" --show-note --show-title > the-cubs-report.md
vim the-cubs-report.md
zfind --database mlb.db --find-summary "Cubs" --show-summary --show-note > the-cubs-report.md
vim the-cubs-report.md
pandoc the-cubs-report.md -o the-cubs-report.html
open the-cubs-report.html
vim the-cubs-report.md
pandoc the-cubs-report.md -o the-cubs-report.html
open the-cubs-report.
open the-cubs-report.html
```

##

```
pwd
cd examples
ls
cd ..
ls
cd baseball
ls
cat chicago-cubs.yaml
zettel --file chicago-cubs.yaml
zettel --file chicago-cubs.yaml --append-tags "World Champions 2016"
zettel --file chicago-cubs.yaml --append-tags "World Champions 2016" --now
diff chicago-cubs.yaml 20180206135815.yaml
mv 20180206135815.yaml chicago-cubs.yaml
git diff
zfind --database mlb.db --find-note "World Series" --show-summary --show-note --show-cite
pwd
cd ../..
ls
cd -
ls
pwd
mv mlb.db ..
cd .
cd ..
ls
```

##

```
rm mlb.db
zcreate --database mlb.db; zimport --database mlb.db --dir $(pwd)
zfind --database mlb.db --find-note "World Series" --show-summary --show-note --show-cite
zfind --database mlb.db --find-note "World Series" --show-summary --show-note --show-cite > gkt-musings/world-series-ch1.yaml
vim gkt-musings/world-series-ch1.yaml
ls
zettel --file gkt-musings/world-series-ch1.yaml
zcreate --database mlb.db; zimport --database mlb.db --dir $(pwd)
vim gkt-musings/world-series-ch1.yaml
zettel --file gkt-musings/world-series-ch1.yaml
```

##

```
zcreate --database mlb.db; zimport --database mlb.db --dir $(pwd)
zfind --find-tags "Chapter 10" --show-note
zfind --database mlb.db --find-tags "Chapter 10" --show-note
zfind --database mlb.db --find-tags "Chapter 10" --show-note --show-tags
zfind --database mlb.db --find-tags "Chapter 10" --show-note --show-tags > temp.yaml; zettel --file temp.yaml
ls
cd baseball
ls
more arizona-diamondbacks.yaml
ls
for team in *.yaml\ndo\n  team_name=$(basename $team .yaml)\n  echo $team_name\ndone
for team in *.yaml\ndo\n  team_name=$(basename $team .yaml)\n  zettel --file $team --append-tags "Baseball History" --save $team.yaml.new\ndone
ls
rm *yaml.yaml*
for team in *.yaml\ndo\n  team_name=$(basename $team .yaml)\n  zettel --file $team --append-tags "Baseball History" --save $team_name.new.yaml\ndone
diff chicago-cubs.yaml chicago-cubs.new.yaml
for team in *.new.yaml\ndo\n  team_name=$(basename $team .new.yaml)\n  mv $team $team_name.yaml\ndone
ls
more chicago-cubs.yaml
ls
git diff
```

## Find out which tags you have used. [TODO: this did not work on NUC.  Which zettelgeist directory should one use? ] 

```
ls
cd
cd Work/zettelgeist
ls
cat zdb_funcs.sh
source zdb_funcs.sh
zdb_tags
zdb_tags blah
cd ..
ls
cd zg-tutorial
ls
cd zettels
zdb_tags mlb.db
```

##

```
ls
pwd
ls ~/Work/zettelgeist/
ls ~/Work/zettels/docs/zquery-examples/charles-and-ada.zql
cat ~/Work/zettels/docs/zquery-examples/charles-and-ada.zql
ls
pw
pwd
cd ..
ls
mkdir queries
vim queries/chicago-world-series.zql
ls
rm zettels/mlb.db
zcreate --database mlb.db; zimport --database mlb.db --dir $(pwd)
ls
cat queries/chicago-world-series.zql
zfilter --help
zfilter --query queries/chicago-world-series.zql --database mlb.db --show-summary --show-note --show-cite
ls
cd 20180206142546-zfind
ls
more 20180206142546-0.yaml.in
ls
more 20180206142546-0.yaml.in
ls
more 20180206142546-0-summary.txt
ls
zettel --file 20180206142546-0.yaml.in --load-summary 20180206142546-0-summary.txt --load-note 20180206142546-0-note.txt
zettel --file 20180206142546-0.yaml.in --load-summary 20180206142546-0-summary.txt --load-note 20180206142546-0-note.txt  --save chicago-cubs-zfilter.yaml
subl chicago-cubs-zfilter.yaml
zettel --file chicago-cubs-zfilter.yaml
ls
zettel --file 20180206142546-1.yaml.in --load-summary 20180206142546-1-summary.txt --load-note 20180206142546-1-note.txt  --save chicago-white-sox-zfilter.yaml
ls
vim chicago-cubs-zfilter.yaml
vim chicago-white-sox-zfilter.yaml
ls
zettel --file 20180206142546-1.yaml.in --load-summary 20180206142546-1-summary.txt --load-note 20180206142546-1-note.txt  --save chicago-white-sox-zfilter.md
vim chicago-white-sox-zfilter.
vim chicago-white-sox-zfilter.md
pandoc chicago-white-sox-zfilter.md chicago-white-sox-zfilter.html
pandoc chicago-white-sox-zfilter.md -o chicago-white-sox-zfilter.html
open chicago-white-sox-zfilter.
open chicago-white-sox-zfilter.html
```

##

```
. ~/zenv/bin/activate
ls
cd Work/zg-tutorial
ls
cd 20180206142546-zfind
ls
for file in *.yaml.in\ndo\n  name=$(basename $file .yaml.in)\n  zettel --file $file --load-summary ${name}-summary.txt --load-note ${name}-note.txt \ndone
for file in *.yaml.in\ndo\n  name=$(basename $file .yaml.in)\n  zettel --file $file --load-summary ${name}-summary.txt --load-note ${name}-note.txt --save ${file}.md\ndone
for file in *.yaml.in\ndo\n  name=$(basename $file .yaml.in)\n  zettel --file $file --load-summary ${name}-summary.txt --load-note ${name}-note.txt --save ${name}.md\ndone
```

# Some more recipes by Dave

## Study results of a zfilter in a single file, using Vim. 

```
zfilter --database ~/Work/zettels/index.db --query ~/Work/zettels/zfiltering/zql-files/Renaissance+Medici.zql --show-title --show-note --show-cite --snip-size 500 
```

```
cat *note.txt > results-Renaissance-Medici.md 
```
```
vim results-Renaissance-Medici.md 
```
Inside vim 

```
:set hlsearch "set highlight searches
:set ignorcase "will ignore case for searches
```
```
/Renaissance\|Medici  "search Renaissance OR Medici in document with vim.... Then see what you want and build zettels using above techniques with copied material...  
```
## Find something and make a zettel from it.

- Go through results.md file in vim as above 

- Find something to make a real zettel out of...

- notice which filename it came from. 

- open another session in zfilter results directory

- determine which yaml.in file is associated with that filename

```
grep "keyword from that filename title" *.yaml.in
```

- note results 

- create zettel command passing that yaml.in in as file, and then prompting for note  [--prompt-note] 

```
zettel --file 20180207121633-1.yaml.in --prompt-note --now --now-id Renaissance+Medici
```

- in Vim, select (and justify, if you wish) the section  you want to make a note with

VjJ

- yank it to the common register 

"+y

- go back to zettel command and copy into note prompt

```
zettel --file 20180207121633-1.yaml.in --prompt-note --now --now-id Renaissance+Medici
Zettel saved to 20180207122548-Renaissance+Medici.yaml
Enter text for note. ctrl-d to end.
note> the press in terms relatively familiar to them. At the heart of printing, as they saw it, was a practical activity--a craft. It was a fast-growing and in some ways extraordinary one, to be sure, but it was still a craft nonetheless. And that suggested how it could be accommodated.  Early modern people knew how crafts should be organized, conducted, and regulated so as to take their place in an orderly commonwealth. The practitioners of the press, therefore--ranging from the great scholar-printers of Renaissance Italy to the first denizens of Grub Street-- organized themselves into communities large and small, along lines familiar from existing crafts. They established "chapels" of journeymen in their houses, and formed guilds or companies to handle the aOairs of the book trades as a whole in particular cities. At the same time, ecclesiastical, academic, and royal authorities devised their own systems to render these 8
note> 
```

- Zettel now created.  It will include all the original title and cite information because you pulled that from the yaml.in file

```
title: Adrian-Johns-Piracy-The-Intellectual-Property-W-BookFi.pdf
note: the press in terms relatively familiar to them. At the heart of printing, as
they saw it, was a practical activity--a craft. It was a fast-growing and in some
ways extraordinary one, to be sure, but it was still a craft nonetheless. And that
suggested how it could be accommodated.  Early modern people knew how crafts should
be organized, conducted, and regulated so as to take their place in an orderly commonwealth.
The practitioners of the press, therefore--ranging from the great scholar-printers
of Renaissance Italy to the first denizens of Grub Street-- organized themselves
into communities large and small, along lines familiar from existing crafts. They
established "chapels" of journeymen in their houses, and formed guilds or companies
to handle the aOairs of the book trades as a whole in particular cities. At the
same time, ecclesiastical, academic, and royal authorities devised their own systems
to render these 8
cite:
bibkey: Johns_Piracyintellectualproperty_2011
```

- Move to your Zettel collection directory.  [OR, create it in that directory using full filenames.  OR, make all notes in this directory, then do 

```
mv *.yaml ~/Work/zettels/hocz/dbdz/
```

- This will move all the proper zettels you have created to your data directory.  Then you can delete all the zfilter results.  

## To find the yaml.in for the precise quotation you want to use... 

- Select the quotation, then grep the whole thing or just a unique phrase in it.  

```
grep -i "The clerks and scribes of the Middle Ages" *note.txt
```
This will give you the name of the note.txt it is in, and then you can build the zettel with the corresponding yaml.in, as above. 
## To easily make zql queries

```
cat > zql-files/name-of-new-query.zql 
note:SearchTerm & note:"Second Search Term" etc. 
ctrl-d
```

- now just pass that query name into last iteration of zfilter. 

```
zfilter --database ~/Work/zettels/index.db --query ~/Work/zettels/zfiltering/zql-files/Ancient-Egypt.zql --show-title --show-note --show-cite --snip-size 500 --output Ancient-Egypt
```


## Create and zimport database that ONLY includes hocz material.... 

```
zcreate --database index.db
zimport --database index.db --dir $(pwd)/hocz/
```

## create the results.md files for the zfilter results and save them in hocz/dbdz, etc. 

- THEN GO BACK AND STUDY THEM, using the above recipes to create new zettels.

- You can REDO the zfilter searches using the ZQLs to get the new set of note.txt and yaml.in, and then just grep for right number based on selected string to make zettels later. [As above.]  

## Sample command flows creating these results.md files 

```
cat > zql-files/Mesopotamia.zql
zfilter --database ~/Work/zettels/index.db --query ~/Work/zettels/zfiltering/zql-files/Mesopotamia.zql --show-title --show-not
e --show-cite --snip-size 500 --output Mesopotamia
ls
cd 20180207132331-Mesopotamia
ls
cat *note.txt > results-Mesopotamia.md
vim results-Mesopotamia.md
mv results* ~/Work/zettels/hocz/dbdz/
cd ..
ls
rm -r 20180207132331-Mesopotamia
ls
cat > zql-files/Ancient-Greece.zql
zfilter --database ~/Work/zettels/index.db --query ~/Work/zettels/zfiltering/zql-files/Ancient-Greece.zql --show-title --show-
note --show-cite --snip-size 1000 --output Ancient-Greece
ls
cd 20180207133450-Ancient-Greece
ls
cat *note.txt > results-Ancient-Greece.md
ls
vim results-Ancient-Greece.md
mv results* ~/Work/zettels/hocz/dbdz/
```

## Sample with creation of a Zettel 

```
vim results-Medieval+Middle-Ages+Gothic.md
grep -i "The clerks and scribes of the Middle Ages" *note.txt
zettel --file 20180207135333-010.yaml.in --prompt-note --now --now-id Medieval-Gothic
```

## [TODO: searching in zql does not allow use of hyphens, even in quotation marks: "seventeenth-century" doesn't work. 

## In order to remove duplicate lines from the results.md file

```
awk '/^#/ || !seen[$0]++' results.md > results-without-duplicates.md
```
This will retain all the lines that start with #, so all the filename and field, etc., will remain in place.  So this will zap the duplicate lines, AND leave the data indicating the sources...  Which lets you then put the quote together with the proper yaml.in file.

Here is a single command to create duplicate-free results files from all the note.txt files from a zfilter.

```
cat *note.txt > temp.md; awk '/^#/ || !a[$0]++' temp.md > results.md; rm temp.md
```

## TO remove duplicate lines from files IN zfind directory (retaining each) 

```
for file in *note.txt
do
  awk '/^#/ || !a[$0]++' "$file" >  "$file.nodups.txt"
  done
```

Then, in vim, do

```args: *nodups.txt
```
`:n` moves to next 
`ctrl-g` tells you which nodups.txt you are in so you can associate with correct yaml.in file

This lets you study each zfilter file individually, using vim search, etc., and then more easily create new zettels with associated yaml.in files.
And, you can move around in all of them, while seeing where you are to make zettels in separate session. 

If you do that combined with

`:set hlsearch`
[highlight search]

and `:set ignorecase`

you can really look around at the results and make zettels.


Using args in VIM you can do a lot of moving around.  But this alone lets you go through each and see what's there. 


-->
