---
layout: page
title: Getting Started
permalink: /gs/
---

ZettelGeist is only a few days old at the time of writing and is thus a work in progress. We're certainly excited about the direction in which the work is heading but at the same time don't want to commit to the interfaces you see here. At least until release (expected mid-summer) you should assume that many aspects of the interface and internals might change.

Owing to the nature of our work, where we are often keeping some proprietary materials in actual Zettels (that is, our notes), we cannot provide actual data files for you at this time. You most certainly can write your own notes based on literature you might be reviewing for your own scholarly project but we cannot provide any of our data sets (yet).

Luckily, we have a script that can *generate* some test data for you. The instructions here assume you have done a checkout or download of the ZettelGeist system and installed any needed dependencies. That is covered on our Installation page (or will be soon).

## Generate some Zettels

Let's start by creating some data so we can take the tool for a spin. We'll generate enough data so the random words we are using in our searches will work! Keep in mind that the answers you get to queries might vary from what you see here.

```shell
$ python generate_random_zettels.py 1000
Generating 1000 docs. Please wait.
...100
...200
...300
...400
...500
...600
...700
...800
...900
...1000
```

This will create a folder, `data`, in the same directory. (The random generation tool is not quite as configurable as our other tools--yet. So there are no options to change the location where this is written.)

To make sure you got some actual data:

```shell
$ ls -l data | wc -l
1001
```
You're more than welcome to look at what gets generated in this folder. We are generating random filenames with random contents in ZettelGeist format.

As an example, here is one of the randomly generated notes that appears in my folder:

```yaml
$ cat overtime-invoice-cents-aggravation-gun-stamp-fractures-exhausts.yaml 

bibkey: opinion preservers tick lights partners basis pit diamonds plow
bibtex: convulsions radar return feeders ticket circuitry
cite: circuits semaphore clearances straw additions
dates: television possessions colleges catalogs overflow news major taps
inline: conjunction harness blurs bands signature purposes sash minutes plug
mentions: [Zac, Annabella, Cooper, Noreen, Roy, Mada, Hector, Jodi, Owen, Brandi]
note: tars chimney tear interval sailors
outline: root tanks majority vendors ornament zip stall
ris: operation bites microphones latitudes laboratory typewriter son fiction languages
summary: deaths sunday receiver formulas beginners police blindfolds deposits dots
  tub canvas sir sum multitask buzzer retrieval blur surface reinforcement threat
  advantage speeds stars overalls danger display sentence swells prerequisite scrap
  alphabets centimeters dots tray doorstep losses park ditches frigates turnarounds
  emitters binder handlers lighters poison curve fruits nozzle inlet runway counts
  training discards cashier azimuths cure restraints twist drunkeness combs ammonia
  apples rock tourniquet lookout discrepancy symptoms schoolrooms crack significance
  formations probabilities sharpeners drivers twos knives breasts plan agreements
  conjunctions loran depositions thyristors tones income personalities hatches alternate
  drawings disks wash recipient congress regulators auditor arch leak tapers levers
  breaks pennant hardcopies hardcopies executions ringing structures
tags: [top, puddle, vessels]
text: precision sleeves qualifiers hoists schoolrooms knot rig friend daybreak forests
  approval drivers nozzles boost marines shape interface farad date house puffs breasts
  badges blows science specialization talk control employee test chances silk guns
  patients confusions sleeve cargoes rifle overload pilot donor elections knees solution
  glides preventions sons superstructures lumps list establishment filler detachment
  pavement trials slot refunds dynamometer lifeboats superlatives reason securities
  injection listings thresholds resistances input eliminator body governments rescuer
  erasers cruiser acronym qualifiers sod thimbles diagnosis disgust soils convulsions
  altimeter airplane similarity strokes digestion desires future snow shaves vines
  web microphone foam tuesdays company launchers pennant coder convention console
  limbs springs cylinders records litres ball construction perforators
title: ring waterlines muscles priority turbine communities
url: planes blindfold topping secretary centerline seams discrimination
```

So it is just a bunch of key value pairs. In some cases, we use lists as the values, especially in the case of items like mentions and tags, which are intended to have lists of names or words, respectively. 

## Create the ZDB (Zettel Database)

Anyway, enough about random note generation. It is just giving you some test data so you can learn about using the rest of our tools. We'll start by creating the Zettel Database, which is a bit of a misnomer, since we are mainly using databases to drive full-text search on an arbitrary number of fields. Then you can use other aptly named z-tools to do various operations on notes.

```
$ python zcreate.py --database randomdata.db
Creating new database randomdata.db
```

In the current set of tools, you will *always* need to use the `--database` option to indicate where your index is located. (Future work is going to make this all configurable as a YAML/JSON file, pointing to the database and folder of Zettels.)

If all has gone according to plan, you should see `randomdata.db` in your folder.

```shell
$ ls -l randomdata.db 
-rw-r--r--. 1 gkt gkt 28672 May 25 11:34 randomdata.db
```

## Importing Zettels

Now that we have the ZDB ready, the next step is to import the dataset.

```shell
$ python zimport.py --database randomdata.db --zettel-dir ./data
```

This will generate a lot of output. In the normal case, the file being imported shows up. But if there are errors, these will appear directly below the filename.

Here is some (successful) output that was generated. Not all 1000 files are shown for conciseness.

```shell
directive-laps-custodians-daytime-competition-cloths-choice-resource-puddles.yaml:
solids-meridians-alignment-distresses-bunch-eliminator-patches-bauds.yaml:
suggestion-tubing-secretaries-love-allowance-armaments-bias-passengers-detection-refurbishment.yaml:
assaults-shadow-lapses-headsets-furnace.yaml:
rotation-propulsions-sessions-contract.yaml:
capacity-spade-development-nozzles-pattern-references-area-trial-dot-administration.yaml:
resident-field-rubber-vent-yield-schoolhouses-instruments.yaml:
threats-firefighting-parks-abuses-jugs-toothpick-stakes-locations-fines-davit.yaml:
brother-beliefs-families-fellow-sand.yaml:
farads-analog-lake-pass.yaml:
injuries-delays-freezes-gravity-closure-adviser-basin-hills-cone-diameter.yaml:
modem-terrain-grade-fence-trims-offsets.yaml:
tuesday-color-date-factories-berth-escapes-pail-tactic-analog-bypasses.yaml:
cane-millions-mineral-integrity.yaml:
weave-portions-relief-clip-acceptance-vibrations-percentages-post-spiral.yaml:
insertion-sewer-echoes.yaml:
deliveries-modules-sexes-bet-grinders-nothing-microphones-tenths-cheeks-introductions.yaml:
asterisks-feather-veteran-dealers.yaml:
looks-presumptions-sleeves.yaml:
ammunition-gases-raise-perforation.yaml:
pitches-programmer-jumper-whirls.yaml:
roar-inclines-disk-inches-polishes-year-fabrication-float-streaks-editor.yaml:
touches-management-father-offers-decoders-starboard-sentries-wind-parts.yaml:
methods-articles-acceptances-cone-fumes-bucket-amplifiers-bilge-attachments.yaml:
repairs-assemblies-keys-ores-workload-piles-verses-headset-groups.yaml:
berths-stationery-blade.yaml:
yaws-strikers-departures-presence-horizons.yaml:
accusation-bends-fare-tears-nylon-bushel-preservers-chains-fluid.yaml:
tug-cupful-hardship-rinses-taste-counter-computers.yaml:
gangways-wall-truck-damage-news.yaml:
artilleries-futures-tactics-factories.yaml:
democracies-locations-breath-ratings-volts-sources-bends-vices-duty-strikers.yaml:
bomb-smash-prefix-efforts.yaml:
```

Ok, so assuming that was successful, your ZDB file should be larger than it was previously:

```shell
$ ls -l *.db
-rw-r--r--. 1 gkt gkt  11329536 May 25 11:38 randomdata.db
```

And it is. The previous size was 28672 (bytes).

## Querying

The `zfind.py` tool allows you to perform conjunctive queries on the various fields. You can query anything you like, but it must be a valid word or set of words separated by whitespace. Because this is sqlite3, you can do some limited non-matching (with NOT) or alternatives (with OR). But our plan is to to make a human-friendly set of options for doing same. Words should be kept in lowercase to avoid conflicts with AND, OR, and NOT and other built-in SQL operators.

```shell
$ python zfind.py --help
usage: zfind.py [-h] [--database DATABASE] [--find-filename FIND_FILENAME]
                [--exclude-filename EXCLUDE_FILENAME] [--show-filename]
                [--find-title FIND_TITLE] [--exclude-title EXCLUDE_TITLE]
                [--show-title] [--find-tags FIND_TAGS]
                [--exclude-tags EXCLUDE_TAGS] [--show-tags]
                [--find-mentions FIND_MENTIONS]
                [--exclude-mentions EXCLUDE_MENTIONS] [--show-mentions]
                [--find-outline FIND_OUTLINE]
                [--exclude-outline EXCLUDE_OUTLINE] [--show-outline]
                [--find-cite FIND_CITE] [--exclude-cite EXCLUDE_CITE]
                [--show-cite] [--find-dates FIND_DATES]
                [--exclude-dates EXCLUDE_DATES] [--show-dates]
                [--find-summary FIND_SUMMARY]
                [--exclude-summary EXCLUDE_SUMMARY] [--show-summary]
                [--find-text FIND_TEXT] [--exclude-text EXCLUDE_TEXT]
                [--show-text] [--find-bibkey FIND_BIBKEY]
                [--exclude-bibkey EXCLUDE_BIBKEY] [--show-bibkey]
                [--find-bibtex FIND_BIBTEX] [--exclude-bibtex EXCLUDE_BIBTEX]
                [--show-bibtex] [--find-ris FIND_RIS]
                [--exclude-ris EXCLUDE_RIS] [--show-ris]
                [--find-inline FIND_INLINE] [--exclude-inline EXCLUDE_INLINE]
                [--show-inline] [--find-note FIND_NOTE]
                [--exclude-note EXCLUDE_NOTE] [--show-note]
                [--find-url FIND_URL] [--exclude-url EXCLUDE_URL] [--show-url]
                [--count]

```

While this looks intimidating at first, there are in fact only a few options. All of the options were generated from the known Zettel fields. So you don't even need to memorize them.

There are essentially 3 options:
- `--find-<FIELD>` is used to find text in a certain Zettel's YAML field
- `--show-<FIELD>` is used to show the <FIELD> when outputting the matching Zettels
- `--exclude-<FIELD>` is used to find text that does not appear in a Zettel's YAML field

So we do have support for not matching text but it cannot be done in OR-style queries yet. 

We'll do a few examples:

Find all documents containing _temperature_ in the *text* field. Show the *title* field and the number of documents that matched.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --show-title --count

title:
liter tars distortions stones shock

----------------------------------------

title:
supermarkets patter narcotics rewards stand channel checker decision morning

----------------------------------------

title:
pennant hardcopy excuse hoists interface jams returns water presentation

----------------------------------------

title:
boom prerequisite net drydocks specialization ships odds custodian kilogram

----------------------------------------

title:
moons fork formats methodology steel fan twigs heads

----------------------------------------

59 Zettels matched search
(zenv) [gkt@wilddog zettelgeist]$ ^Cthon zfind.py --database randomdata.db --find-text temperature --sho
w-title --count$ python zfind.py --database randomdata.db --find-text temperature --show-title --count
```

Again, we have omitted some results for conciseness.

Now take a look at some of the results. Since _methodology_ appears in one of them, let's do a search to restrict the results further by searching *title* for _methodology_.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --count
1 Zettels matched search
```

Now that we found a Zettel of interest (well, it's not that interesting compared to our real notes, but...) we can project some addition fields of interest:

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --show-mentions --show-tags --count
mentions:
Raul,Candace,Petar,Shawnette,Darren,Camryn,Brett,Kailey

tags:
dock,reach,itineraries

----------------------------------------

1 Zettels matched search
```

The output you see here is slightly different than the source Zettel (note) in YAML, because we _flatten_ the lists and text for full-text searching purposes. Future work will pull up everything from the actual Zettel, mainly for pretty printing purposes.

As you can see above, we were able to project different columns than what was actually matched.

So this is where we stand with our tools right now. We'll be updating the docs as work progresses but this is already proving useful for organizing our notes. Feel free to follow our project for the latest developments. We also welcome Issues in the Issue Tracker.




ZettelGeist is only a few days old at the time of writing and is thus a work in progress. We're certainly excited about the direction in which the work is heading but at the same time don't want to commit to the interfaces you see here. At least until release (expected mid-summer) you should assume that many aspects of the interface and internals might change.

Owing to the nature of our work, where we are often keeping some proprietary materials in actual Zettels (that is, our notes), we cannot provide actual data files for you at this time. You most certainly can write your own notes based on literature you might be reviewing for your own scholarly project but we cannot provide any of our data sets (yet).

Luckily, we have a script that can *generate* some test data for you. The instructions here assume you have done a checkout or download of the ZettelGeist system and installed any needed dependencies. That is covered on our Installation page (or will be soon).

## Generate some Zettels

Let's start by creating some data so we can take the tool for a spin. We'll generate enough data so the random words we are using in our searches will work! Keep in mind that the answers you get to queries might vary from what you see here.

```shell
$ python generate_random_zettels.py 1000
Generating 1000 docs. Please wait.
...100
...200
...300
...400
...500
...600
...700
...800
...900
...1000
```

This will create a folder, `data`, in the same directory. (The random generation tool is not quite as configurable as our other tools--yet. So there are no options to change the location where this is written.)

To make sure you got some actual data:

```shell
$ ls -l data | wc -l
1001
```
You're more than welcome to look at what gets generated in this folder. We are generating random filenames with random contents in ZettelGeist format.

As an example, here is one of the randomly generated notes that appears in my folder:

```yaml
$ cat overtime-invoice-cents-aggravation-gun-stamp-fractures-exhausts.yaml 

bibkey: opinion preservers tick lights partners basis pit diamonds plow
bibtex: convulsions radar return feeders ticket circuitry
cite: circuits semaphore clearances straw additions
dates: television possessions colleges catalogs overflow news major taps
inline: conjunction harness blurs bands signature purposes sash minutes plug
mentions: [Zac, Annabella, Cooper, Noreen, Roy, Mada, Hector, Jodi, Owen, Brandi]
note: tars chimney tear interval sailors
outline: root tanks majority vendors ornament zip stall
ris: operation bites microphones latitudes laboratory typewriter son fiction languages
summary: deaths sunday receiver formulas beginners police blindfolds deposits dots
  tub canvas sir sum multitask buzzer retrieval blur surface reinforcement threat
  advantage speeds stars overalls danger display sentence swells prerequisite scrap
  alphabets centimeters dots tray doorstep losses park ditches frigates turnarounds
  emitters binder handlers lighters poison curve fruits nozzle inlet runway counts
  training discards cashier azimuths cure restraints twist drunkeness combs ammonia
  apples rock tourniquet lookout discrepancy symptoms schoolrooms crack significance
  formations probabilities sharpeners drivers twos knives breasts plan agreements
  conjunctions loran depositions thyristors tones income personalities hatches alternate
  drawings disks wash recipient congress regulators auditor arch leak tapers levers
  breaks pennant hardcopies hardcopies executions ringing structures
tags: [top, puddle, vessels]
text: precision sleeves qualifiers hoists schoolrooms knot rig friend daybreak forests
  approval drivers nozzles boost marines shape interface farad date house puffs breasts
  badges blows science specialization talk control employee test chances silk guns
  patients confusions sleeve cargoes rifle overload pilot donor elections knees solution
  glides preventions sons superstructures lumps list establishment filler detachment
  pavement trials slot refunds dynamometer lifeboats superlatives reason securities
  injection listings thresholds resistances input eliminator body governments rescuer
  erasers cruiser acronym qualifiers sod thimbles diagnosis disgust soils convulsions
  altimeter airplane similarity strokes digestion desires future snow shaves vines
  web microphone foam tuesdays company launchers pennant coder convention console
  limbs springs cylinders records litres ball construction perforators
title: ring waterlines muscles priority turbine communities
url: planes blindfold topping secretary centerline seams discrimination
```

So it is just a bunch of key value pairs. In some cases, we use lists as the values, especially in the case of items like mentions and tags, which are intended to have lists of names or words, respectively. 

## Create the ZDB (Zettel Database)

Anyway, enough about random note generation. It is just giving you some test data so you can learn about using the rest of our tools. We'll start by creating the Zettel Database, which is a bit of a misnomer, since we are mainly using databases to drive full-text search on an arbitrary number of fields. Then you can use other aptly named z-tools to do various operations on notes.

```
$ python zcreate.py --database randomdata.db
Creating new database randomdata.db
```

In the current set of tools, you will *always* need to use the `--database` option to indicate where your index is located. (Future work is going to make this all configurable as a YAML/JSON file, pointing to the database and folder of Zettels.)

If all has gone according to plan, you should see `randomdata.db` in your folder.

```shell
$ ls -l randomdata.db 
-rw-r--r--. 1 gkt gkt 28672 May 25 11:34 randomdata.db
```

## Importing Zettels

Now that we have the ZDB ready, the next step is to import the dataset.

```shell
$ python zimport.py --database randomdata.db --zettel-dir ./data
```

This will generate a lot of output. In the normal case, the file being imported shows up. But if there are errors, these will appear directly below the filename.

Here is some (successful) output that was generated. Not all 1000 files are shown for conciseness.

```shell
directive-laps-custodians-daytime-competition-cloths-choice-resource-puddles.yaml:
solids-meridians-alignment-distresses-bunch-eliminator-patches-bauds.yaml:
suggestion-tubing-secretaries-love-allowance-armaments-bias-passengers-detection-refurbishment.yaml:
assaults-shadow-lapses-headsets-furnace.yaml:
rotation-propulsions-sessions-contract.yaml:
capacity-spade-development-nozzles-pattern-references-area-trial-dot-administration.yaml:
resident-field-rubber-vent-yield-schoolhouses-instruments.yaml:
threats-firefighting-parks-abuses-jugs-toothpick-stakes-locations-fines-davit.yaml:
brother-beliefs-families-fellow-sand.yaml:
farads-analog-lake-pass.yaml:
injuries-delays-freezes-gravity-closure-adviser-basin-hills-cone-diameter.yaml:
modem-terrain-grade-fence-trims-offsets.yaml:
tuesday-color-date-factories-berth-escapes-pail-tactic-analog-bypasses.yaml:
cane-millions-mineral-integrity.yaml:
weave-portions-relief-clip-acceptance-vibrations-percentages-post-spiral.yaml:
insertion-sewer-echoes.yaml:
deliveries-modules-sexes-bet-grinders-nothing-microphones-tenths-cheeks-introductions.yaml:
asterisks-feather-veteran-dealers.yaml:
looks-presumptions-sleeves.yaml:
ammunition-gases-raise-perforation.yaml:
pitches-programmer-jumper-whirls.yaml:
roar-inclines-disk-inches-polishes-year-fabrication-float-streaks-editor.yaml:
touches-management-father-offers-decoders-starboard-sentries-wind-parts.yaml:
methods-articles-acceptances-cone-fumes-bucket-amplifiers-bilge-attachments.yaml:
repairs-assemblies-keys-ores-workload-piles-verses-headset-groups.yaml:
berths-stationery-blade.yaml:
yaws-strikers-departures-presence-horizons.yaml:
accusation-bends-fare-tears-nylon-bushel-preservers-chains-fluid.yaml:
tug-cupful-hardship-rinses-taste-counter-computers.yaml:
gangways-wall-truck-damage-news.yaml:
artilleries-futures-tactics-factories.yaml:
democracies-locations-breath-ratings-volts-sources-bends-vices-duty-strikers.yaml:
bomb-smash-prefix-efforts.yaml:
```

Ok, so assuming that was successful, your ZDB file should be larger than it was previously:

```shell
$ ls -l *.db
-rw-r--r--. 1 gkt gkt  11329536 May 25 11:38 randomdata.db
```

And it is. The previous size was 28672 (bytes).

## Querying

The `zfind.py` tool allows you to perform conjunctive queries on the various fields. You can query anything you like, but it must be a valid word or set of words separated by whitespace. Because this is sqlite3, you can do some limited non-matching (with NOT) or alternatives (with OR). But our plan is to to make a human-friendly set of options for doing same. Words should be kept in lowercase to avoid conflicts with AND, OR, and NOT and other built-in SQL operators.

```shell
$ python zfind.py --help
usage: zfind.py [-h] [--database DATABASE] [--find-filename FIND_FILENAME]
                [--exclude-filename EXCLUDE_FILENAME] [--show-filename]
                [--find-title FIND_TITLE] [--exclude-title EXCLUDE_TITLE]
                [--show-title] [--find-tags FIND_TAGS]
                [--exclude-tags EXCLUDE_TAGS] [--show-tags]
                [--find-mentions FIND_MENTIONS]
                [--exclude-mentions EXCLUDE_MENTIONS] [--show-mentions]
                [--find-outline FIND_OUTLINE]
                [--exclude-outline EXCLUDE_OUTLINE] [--show-outline]
                [--find-cite FIND_CITE] [--exclude-cite EXCLUDE_CITE]
                [--show-cite] [--find-dates FIND_DATES]
                [--exclude-dates EXCLUDE_DATES] [--show-dates]
                [--find-summary FIND_SUMMARY]
                [--exclude-summary EXCLUDE_SUMMARY] [--show-summary]
                [--find-text FIND_TEXT] [--exclude-text EXCLUDE_TEXT]
                [--show-text] [--find-bibkey FIND_BIBKEY]
                [--exclude-bibkey EXCLUDE_BIBKEY] [--show-bibkey]
                [--find-bibtex FIND_BIBTEX] [--exclude-bibtex EXCLUDE_BIBTEX]
                [--show-bibtex] [--find-ris FIND_RIS]
                [--exclude-ris EXCLUDE_RIS] [--show-ris]
                [--find-inline FIND_INLINE] [--exclude-inline EXCLUDE_INLINE]
                [--show-inline] [--find-note FIND_NOTE]
                [--exclude-note EXCLUDE_NOTE] [--show-note]
                [--find-url FIND_URL] [--exclude-url EXCLUDE_URL] [--show-url]
                [--count]

```

While this looks intimidating at first, there are in fact only a few options. All of the options were generated from the known Zettel fields. So you don't even need to memorize them.

There are essentially 3 options:
- `--find-<FIELD>` is used to find text in a certain Zettel's YAML field
- `--show-<FIELD>` is used to show the <FIELD> when outputting the matching Zettels
- `--exclude-<FIELD>` is used to find text that does not appear in a Zettel's YAML field

So we do have support for not matching text but it cannot be done in OR-style queries yet. 

We'll do a few examples:

Find all documents containing _temperature_ in the *text* field. Show the *title* field and the number of documents that matched.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --show-title --count

title:
liter tars distortions stones shock

----------------------------------------

title:
supermarkets patter narcotics rewards stand channel checker decision morning

----------------------------------------

title:
pennant hardcopy excuse hoists interface jams returns water presentation

----------------------------------------

title:
boom prerequisite net drydocks specialization ships odds custodian kilogram

----------------------------------------

title:
moons fork formats methodology steel fan twigs heads

----------------------------------------

59 Zettels matched search
(zenv) [gkt@wilddog zettelgeist]$ ^Cthon zfind.py --database randomdata.db --find-text temperature --sho
w-title --count$ python zfind.py --database randomdata.db --find-text temperature --show-title --count
```

Again, we have omitted some results for conciseness.

Now take a look at some of the results. Since _methodology_ appears in one of them, let's do a search to restrict the results further by searching *title* for _methodology_.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --count
1 Zettels matched search
```

Now that we found a Zettel of interest (well, it's not that interesting compared to our real notes, but...) we can project some addition fields of interest:

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --show-mentions --show-tags --count
mentions:
Raul,Candace,Petar,Shawnette,Darren,Camryn,Brett,Kailey

tags:
dock,reach,itineraries

----------------------------------------

1 Zettels matched search
```

The output you see here is slightly different than the source Zettel (note) in YAML, because we _flatten_ the lists and text for full-text searching purposes. Future work will pull up everything from the actual Zettel, mainly for pretty printing purposes.

As you can see above, we were able to project different columns than what was actually matched.

So this is where we stand with our tools right now. We'll be updating the docs as work progresses but this is already proving useful for organizing our notes. Feel free to follow our project for the latest developments. We also welcome Issues in the Issue Tracker.




ZettelGeist is only a few days old at the time of writing and is thus a work in progress. We're certainly excited about the direction in which the work is heading but at the same time don't want to commit to the interfaces you see here. At least until release (expected mid-summer) you should assume that many aspects of the interface and internals might change.

Owing to the nature of our work, where we are often keeping some proprietary materials in actual Zettels (that is, our notes), we cannot provide actual data files for you at this time. You most certainly can write your own notes based on literature you might be reviewing for your own scholarly project but we cannot provide any of our data sets (yet).

Luckily, we have a script that can *generate* some test data for you. The instructions here assume you have done a checkout or download of the ZettelGeist system and installed any needed dependencies. That is covered on our Installation page (or will be soon).

## Generate some Zettels

Let's start by creating some data so we can take the tool for a spin. We'll generate enough data so the random words we are using in our searches will work! Keep in mind that the answers you get to queries might vary from what you see here.

```shell
$ python generate_random_zettels.py 1000
Generating 1000 docs. Please wait.
...100
...200
...300
...400
...500
...600
...700
...800
...900
...1000
```

This will create a folder, `data`, in the same directory. (The random generation tool is not quite as configurable as our other tools--yet. So there are no options to change the location where this is written.)

To make sure you got some actual data:

```shell
$ ls -l data | wc -l
1001
```
You're more than welcome to look at what gets generated in this folder. We are generating random filenames with random contents in ZettelGeist format.

As an example, here is one of the randomly generated notes that appears in my folder:

```yaml
$ cat overtime-invoice-cents-aggravation-gun-stamp-fractures-exhausts.yaml 

bibkey: opinion preservers tick lights partners basis pit diamonds plow
bibtex: convulsions radar return feeders ticket circuitry
cite: circuits semaphore clearances straw additions
dates: television possessions colleges catalogs overflow news major taps
inline: conjunction harness blurs bands signature purposes sash minutes plug
mentions: [Zac, Annabella, Cooper, Noreen, Roy, Mada, Hector, Jodi, Owen, Brandi]
note: tars chimney tear interval sailors
outline: root tanks majority vendors ornament zip stall
ris: operation bites microphones latitudes laboratory typewriter son fiction languages
summary: deaths sunday receiver formulas beginners police blindfolds deposits dots
  tub canvas sir sum multitask buzzer retrieval blur surface reinforcement threat
  advantage speeds stars overalls danger display sentence swells prerequisite scrap
  alphabets centimeters dots tray doorstep losses park ditches frigates turnarounds
  emitters binder handlers lighters poison curve fruits nozzle inlet runway counts
  training discards cashier azimuths cure restraints twist drunkeness combs ammonia
  apples rock tourniquet lookout discrepancy symptoms schoolrooms crack significance
  formations probabilities sharpeners drivers twos knives breasts plan agreements
  conjunctions loran depositions thyristors tones income personalities hatches alternate
  drawings disks wash recipient congress regulators auditor arch leak tapers levers
  breaks pennant hardcopies hardcopies executions ringing structures
tags: [top, puddle, vessels]
text: precision sleeves qualifiers hoists schoolrooms knot rig friend daybreak forests
  approval drivers nozzles boost marines shape interface farad date house puffs breasts
  badges blows science specialization talk control employee test chances silk guns
  patients confusions sleeve cargoes rifle overload pilot donor elections knees solution
  glides preventions sons superstructures lumps list establishment filler detachment
  pavement trials slot refunds dynamometer lifeboats superlatives reason securities
  injection listings thresholds resistances input eliminator body governments rescuer
  erasers cruiser acronym qualifiers sod thimbles diagnosis disgust soils convulsions
  altimeter airplane similarity strokes digestion desires future snow shaves vines
  web microphone foam tuesdays company launchers pennant coder convention console
  limbs springs cylinders records litres ball construction perforators
title: ring waterlines muscles priority turbine communities
url: planes blindfold topping secretary centerline seams discrimination
```

So it is just a bunch of key value pairs. In some cases, we use lists as the values, especially in the case of items like mentions and tags, which are intended to have lists of names or words, respectively. 

## Create the ZDB (Zettel Database)

Anyway, enough about random note generation. It is just giving you some test data so you can learn about using the rest of our tools. We'll start by creating the Zettel Database, which is a bit of a misnomer, since we are mainly using databases to drive full-text search on an arbitrary number of fields. Then you can use other aptly named z-tools to do various operations on notes.

```
$ python zcreate.py --database randomdata.db
Creating new database randomdata.db
```

In the current set of tools, you will *always* need to use the `--database` option to indicate where your index is located. (Future work is going to make this all configurable as a YAML/JSON file, pointing to the database and folder of Zettels.)

If all has gone according to plan, you should see `randomdata.db` in your folder.

```shell
$ ls -l randomdata.db 
-rw-r--r--. 1 gkt gkt 28672 May 25 11:34 randomdata.db
```

## Importing Zettels

Now that we have the ZDB ready, the next step is to import the dataset.

```shell
$ python zimport.py --database randomdata.db --zettel-dir ./data
```

This will generate a lot of output. In the normal case, the file being imported shows up. But if there are errors, these will appear directly below the filename.

Here is some (successful) output that was generated. Not all 1000 files are shown for conciseness.

```shell
directive-laps-custodians-daytime-competition-cloths-choice-resource-puddles.yaml:
solids-meridians-alignment-distresses-bunch-eliminator-patches-bauds.yaml:
suggestion-tubing-secretaries-love-allowance-armaments-bias-passengers-detection-refurbishment.yaml:
assaults-shadow-lapses-headsets-furnace.yaml:
rotation-propulsions-sessions-contract.yaml:
capacity-spade-development-nozzles-pattern-references-area-trial-dot-administration.yaml:
resident-field-rubber-vent-yield-schoolhouses-instruments.yaml:
threats-firefighting-parks-abuses-jugs-toothpick-stakes-locations-fines-davit.yaml:
brother-beliefs-families-fellow-sand.yaml:
farads-analog-lake-pass.yaml:
injuries-delays-freezes-gravity-closure-adviser-basin-hills-cone-diameter.yaml:
modem-terrain-grade-fence-trims-offsets.yaml:
tuesday-color-date-factories-berth-escapes-pail-tactic-analog-bypasses.yaml:
cane-millions-mineral-integrity.yaml:
weave-portions-relief-clip-acceptance-vibrations-percentages-post-spiral.yaml:
insertion-sewer-echoes.yaml:
deliveries-modules-sexes-bet-grinders-nothing-microphones-tenths-cheeks-introductions.yaml:
asterisks-feather-veteran-dealers.yaml:
looks-presumptions-sleeves.yaml:
ammunition-gases-raise-perforation.yaml:
pitches-programmer-jumper-whirls.yaml:
roar-inclines-disk-inches-polishes-year-fabrication-float-streaks-editor.yaml:
touches-management-father-offers-decoders-starboard-sentries-wind-parts.yaml:
methods-articles-acceptances-cone-fumes-bucket-amplifiers-bilge-attachments.yaml:
repairs-assemblies-keys-ores-workload-piles-verses-headset-groups.yaml:
berths-stationery-blade.yaml:
yaws-strikers-departures-presence-horizons.yaml:
accusation-bends-fare-tears-nylon-bushel-preservers-chains-fluid.yaml:
tug-cupful-hardship-rinses-taste-counter-computers.yaml:
gangways-wall-truck-damage-news.yaml:
artilleries-futures-tactics-factories.yaml:
democracies-locations-breath-ratings-volts-sources-bends-vices-duty-strikers.yaml:
bomb-smash-prefix-efforts.yaml:
```

Ok, so assuming that was successful, your ZDB file should be larger than it was previously:

```shell
$ ls -l *.db
-rw-r--r--. 1 gkt gkt  11329536 May 25 11:38 randomdata.db
```

And it is. The previous size was 28672 (bytes).

## Querying

The `zfind.py` tool allows you to perform conjunctive queries on the various fields. You can query anything you like, but it must be a valid word or set of words separated by whitespace. Because this is sqlite3, you can do some limited non-matching (with NOT) or alternatives (with OR). But our plan is to to make a human-friendly set of options for doing same. Words should be kept in lowercase to avoid conflicts with AND, OR, and NOT and other built-in SQL operators.

```shell
$ python zfind.py --help
usage: zfind.py [-h] [--database DATABASE] [--find-filename FIND_FILENAME]
                [--exclude-filename EXCLUDE_FILENAME] [--show-filename]
                [--find-title FIND_TITLE] [--exclude-title EXCLUDE_TITLE]
                [--show-title] [--find-tags FIND_TAGS]
                [--exclude-tags EXCLUDE_TAGS] [--show-tags]
                [--find-mentions FIND_MENTIONS]
                [--exclude-mentions EXCLUDE_MENTIONS] [--show-mentions]
                [--find-outline FIND_OUTLINE]
                [--exclude-outline EXCLUDE_OUTLINE] [--show-outline]
                [--find-cite FIND_CITE] [--exclude-cite EXCLUDE_CITE]
                [--show-cite] [--find-dates FIND_DATES]
                [--exclude-dates EXCLUDE_DATES] [--show-dates]
                [--find-summary FIND_SUMMARY]
                [--exclude-summary EXCLUDE_SUMMARY] [--show-summary]
                [--find-text FIND_TEXT] [--exclude-text EXCLUDE_TEXT]
                [--show-text] [--find-bibkey FIND_BIBKEY]
                [--exclude-bibkey EXCLUDE_BIBKEY] [--show-bibkey]
                [--find-bibtex FIND_BIBTEX] [--exclude-bibtex EXCLUDE_BIBTEX]
                [--show-bibtex] [--find-ris FIND_RIS]
                [--exclude-ris EXCLUDE_RIS] [--show-ris]
                [--find-inline FIND_INLINE] [--exclude-inline EXCLUDE_INLINE]
                [--show-inline] [--find-note FIND_NOTE]
                [--exclude-note EXCLUDE_NOTE] [--show-note]
                [--find-url FIND_URL] [--exclude-url EXCLUDE_URL] [--show-url]
                [--count]

```

While this looks intimidating at first, there are in fact only a few options. All of the options were generated from the known Zettel fields. So you don't even need to memorize them.

There are essentially 3 options:
- `--find-<FIELD>` is used to find text in a certain Zettel's YAML field
- `--show-<FIELD>` is used to show the <FIELD> when outputting the matching Zettels
- `--exclude-<FIELD>` is used to find text that does not appear in a Zettel's YAML field

So we do have support for not matching text but it cannot be done in OR-style queries yet. 

We'll do a few examples:

Find all documents containing _temperature_ in the *text* field. Show the *title* field and the number of documents that matched.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --show-title --count

title:
liter tars distortions stones shock

----------------------------------------

title:
supermarkets patter narcotics rewards stand channel checker decision morning

----------------------------------------

title:
pennant hardcopy excuse hoists interface jams returns water presentation

----------------------------------------

title:
boom prerequisite net drydocks specialization ships odds custodian kilogram

----------------------------------------

title:
moons fork formats methodology steel fan twigs heads

----------------------------------------

59 Zettels matched search
(zenv) [gkt@wilddog zettelgeist]$ ^Cthon zfind.py --database randomdata.db --find-text temperature --sho
w-title --count$ python zfind.py --database randomdata.db --find-text temperature --show-title --count
```

Again, we have omitted some results for conciseness.

Now take a look at some of the results. Since _methodology_ appears in one of them, let's do a search to restrict the results further by searching *title* for _methodology_.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --count
1 Zettels matched search
```

Now that we found a Zettel of interest (well, it's not that interesting compared to our real notes, but...) we can project some addition fields of interest:

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --show-mentions --show-tags --count
mentions:
Raul,Candace,Petar,Shawnette,Darren,Camryn,Brett,Kailey

tags:
dock,reach,itineraries

----------------------------------------

1 Zettels matched search
```

The output you see here is slightly different than the source Zettel (note) in YAML, because we _flatten_ the lists and text for full-text searching purposes. Future work will pull up everything from the actual Zettel, mainly for pretty printing purposes.

As you can see above, we were able to project different columns than what was actually matched.

So this is where we stand with our tools right now. We'll be updating the docs as work progresses but this is already proving useful for organizing our notes. Feel free to follow our project for the latest developments. We also welcome Issues in the Issue Tracker.




ZettelGeist is only a few days old at the time of writing and is thus a work in progress. We're certainly excited about the direction in which the work is heading but at the same time don't want to commit to the interfaces you see here. At least until release (expected mid-summer) you should assume that many aspects of the interface and internals might change.

Owing to the nature of our work, where we are often keeping some proprietary materials in actual Zettels (that is, our notes), we cannot provide actual data files for you at this time. You most certainly can write your own notes based on literature you might be reviewing for your own scholarly project but we cannot provide any of our data sets (yet).

Luckily, we have a script that can *generate* some test data for you. The instructions here assume you have done a checkout or download of the ZettelGeist system and installed any needed dependencies. That is covered on our Installation page (or will be soon).

## Generate some Zettels

Let's start by creating some data so we can take the tool for a spin. We'll generate enough data so the random words we are using in our searches will work! Keep in mind that the answers you get to queries might vary from what you see here.

```shell
$ python generate_random_zettels.py 1000
Generating 1000 docs. Please wait.
...100
...200
...300
...400
...500
...600
...700
...800
...900
...1000
```

This will create a folder, `data`, in the same directory. (The random generation tool is not quite as configurable as our other tools--yet. So there are no options to change the location where this is written.)

To make sure you got some actual data:

```shell
$ ls -l data | wc -l
1001
```
You're more than welcome to look at what gets generated in this folder. We are generating random filenames with random contents in ZettelGeist format.

As an example, here is one of the randomly generated notes that appears in my folder:

```yaml
$ cat overtime-invoice-cents-aggravation-gun-stamp-fractures-exhausts.yaml 

bibkey: opinion preservers tick lights partners basis pit diamonds plow
bibtex: convulsions radar return feeders ticket circuitry
cite: circuits semaphore clearances straw additions
dates: television possessions colleges catalogs overflow news major taps
inline: conjunction harness blurs bands signature purposes sash minutes plug
mentions: [Zac, Annabella, Cooper, Noreen, Roy, Mada, Hector, Jodi, Owen, Brandi]
note: tars chimney tear interval sailors
outline: root tanks majority vendors ornament zip stall
ris: operation bites microphones latitudes laboratory typewriter son fiction languages
summary: deaths sunday receiver formulas beginners police blindfolds deposits dots
  tub canvas sir sum multitask buzzer retrieval blur surface reinforcement threat
  advantage speeds stars overalls danger display sentence swells prerequisite scrap
  alphabets centimeters dots tray doorstep losses park ditches frigates turnarounds
  emitters binder handlers lighters poison curve fruits nozzle inlet runway counts
  training discards cashier azimuths cure restraints twist drunkeness combs ammonia
  apples rock tourniquet lookout discrepancy symptoms schoolrooms crack significance
  formations probabilities sharpeners drivers twos knives breasts plan agreements
  conjunctions loran depositions thyristors tones income personalities hatches alternate
  drawings disks wash recipient congress regulators auditor arch leak tapers levers
  breaks pennant hardcopies hardcopies executions ringing structures
tags: [top, puddle, vessels]
text: precision sleeves qualifiers hoists schoolrooms knot rig friend daybreak forests
  approval drivers nozzles boost marines shape interface farad date house puffs breasts
  badges blows science specialization talk control employee test chances silk guns
  patients confusions sleeve cargoes rifle overload pilot donor elections knees solution
  glides preventions sons superstructures lumps list establishment filler detachment
  pavement trials slot refunds dynamometer lifeboats superlatives reason securities
  injection listings thresholds resistances input eliminator body governments rescuer
  erasers cruiser acronym qualifiers sod thimbles diagnosis disgust soils convulsions
  altimeter airplane similarity strokes digestion desires future snow shaves vines
  web microphone foam tuesdays company launchers pennant coder convention console
  limbs springs cylinders records litres ball construction perforators
title: ring waterlines muscles priority turbine communities
url: planes blindfold topping secretary centerline seams discrimination
```

So it is just a bunch of key value pairs. In some cases, we use lists as the values, especially in the case of items like mentions and tags, which are intended to have lists of names or words, respectively. 

## Create the ZDB (Zettel Database)

Anyway, enough about random note generation. It is just giving you some test data so you can learn about using the rest of our tools. We'll start by creating the Zettel Database, which is a bit of a misnomer, since we are mainly using databases to drive full-text search on an arbitrary number of fields. Then you can use other aptly named z-tools to do various operations on notes.

```
$ python zcreate.py --database randomdata.db
Creating new database randomdata.db
```

In the current set of tools, you will *always* need to use the `--database` option to indicate where your index is located. (Future work is going to make this all configurable as a YAML/JSON file, pointing to the database and folder of Zettels.)

If all has gone according to plan, you should see `randomdata.db` in your folder.

```shell
$ ls -l randomdata.db 
-rw-r--r--. 1 gkt gkt 28672 May 25 11:34 randomdata.db
```

## Importing Zettels

Now that we have the ZDB ready, the next step is to import the dataset.

```shell
$ python zimport.py --database randomdata.db --zettel-dir ./data
```

This will generate a lot of output. In the normal case, the file being imported shows up. But if there are errors, these will appear directly below the filename.

Here is some (successful) output that was generated. Not all 1000 files are shown for conciseness.

```shell
directive-laps-custodians-daytime-competition-cloths-choice-resource-puddles.yaml:
solids-meridians-alignment-distresses-bunch-eliminator-patches-bauds.yaml:
suggestion-tubing-secretaries-love-allowance-armaments-bias-passengers-detection-refurbishment.yaml:
assaults-shadow-lapses-headsets-furnace.yaml:
rotation-propulsions-sessions-contract.yaml:
capacity-spade-development-nozzles-pattern-references-area-trial-dot-administration.yaml:
resident-field-rubber-vent-yield-schoolhouses-instruments.yaml:
threats-firefighting-parks-abuses-jugs-toothpick-stakes-locations-fines-davit.yaml:
brother-beliefs-families-fellow-sand.yaml:
farads-analog-lake-pass.yaml:
injuries-delays-freezes-gravity-closure-adviser-basin-hills-cone-diameter.yaml:
modem-terrain-grade-fence-trims-offsets.yaml:
tuesday-color-date-factories-berth-escapes-pail-tactic-analog-bypasses.yaml:
cane-millions-mineral-integrity.yaml:
weave-portions-relief-clip-acceptance-vibrations-percentages-post-spiral.yaml:
insertion-sewer-echoes.yaml:
deliveries-modules-sexes-bet-grinders-nothing-microphones-tenths-cheeks-introductions.yaml:
asterisks-feather-veteran-dealers.yaml:
looks-presumptions-sleeves.yaml:
ammunition-gases-raise-perforation.yaml:
pitches-programmer-jumper-whirls.yaml:
roar-inclines-disk-inches-polishes-year-fabrication-float-streaks-editor.yaml:
touches-management-father-offers-decoders-starboard-sentries-wind-parts.yaml:
methods-articles-acceptances-cone-fumes-bucket-amplifiers-bilge-attachments.yaml:
repairs-assemblies-keys-ores-workload-piles-verses-headset-groups.yaml:
berths-stationery-blade.yaml:
yaws-strikers-departures-presence-horizons.yaml:
accusation-bends-fare-tears-nylon-bushel-preservers-chains-fluid.yaml:
tug-cupful-hardship-rinses-taste-counter-computers.yaml:
gangways-wall-truck-damage-news.yaml:
artilleries-futures-tactics-factories.yaml:
democracies-locations-breath-ratings-volts-sources-bends-vices-duty-strikers.yaml:
bomb-smash-prefix-efforts.yaml:
```

Ok, so assuming that was successful, your ZDB file should be larger than it was previously:

```shell
$ ls -l *.db
-rw-r--r--. 1 gkt gkt  11329536 May 25 11:38 randomdata.db
```

And it is. The previous size was 28672 (bytes).

## Querying

The `zfind.py` tool allows you to perform conjunctive queries on the various fields. You can query anything you like, but it must be a valid word or set of words separated by whitespace. Because this is sqlite3, you can do some limited non-matching (with NOT) or alternatives (with OR). But our plan is to to make a human-friendly set of options for doing same. Words should be kept in lowercase to avoid conflicts with AND, OR, and NOT and other built-in SQL operators.

```shell
$ python zfind.py --help
usage: zfind.py [-h] [--database DATABASE] [--find-filename FIND_FILENAME]
                [--exclude-filename EXCLUDE_FILENAME] [--show-filename]
                [--find-title FIND_TITLE] [--exclude-title EXCLUDE_TITLE]
                [--show-title] [--find-tags FIND_TAGS]
                [--exclude-tags EXCLUDE_TAGS] [--show-tags]
                [--find-mentions FIND_MENTIONS]
                [--exclude-mentions EXCLUDE_MENTIONS] [--show-mentions]
                [--find-outline FIND_OUTLINE]
                [--exclude-outline EXCLUDE_OUTLINE] [--show-outline]
                [--find-cite FIND_CITE] [--exclude-cite EXCLUDE_CITE]
                [--show-cite] [--find-dates FIND_DATES]
                [--exclude-dates EXCLUDE_DATES] [--show-dates]
                [--find-summary FIND_SUMMARY]
                [--exclude-summary EXCLUDE_SUMMARY] [--show-summary]
                [--find-text FIND_TEXT] [--exclude-text EXCLUDE_TEXT]
                [--show-text] [--find-bibkey FIND_BIBKEY]
                [--exclude-bibkey EXCLUDE_BIBKEY] [--show-bibkey]
                [--find-bibtex FIND_BIBTEX] [--exclude-bibtex EXCLUDE_BIBTEX]
                [--show-bibtex] [--find-ris FIND_RIS]
                [--exclude-ris EXCLUDE_RIS] [--show-ris]
                [--find-inline FIND_INLINE] [--exclude-inline EXCLUDE_INLINE]
                [--show-inline] [--find-note FIND_NOTE]
                [--exclude-note EXCLUDE_NOTE] [--show-note]
                [--find-url FIND_URL] [--exclude-url EXCLUDE_URL] [--show-url]
                [--count]

```

While this looks intimidating at first, there are in fact only a few options. All of the options were generated from the known Zettel fields. So you don't even need to memorize them.

There are essentially 3 options:
- `--find-<FIELD>` is used to find text in a certain Zettel's YAML field
- `--show-<FIELD>` is used to show the <FIELD> when outputting the matching Zettels
- `--exclude-<FIELD>` is used to find text that does not appear in a Zettel's YAML field

So we do have support for not matching text but it cannot be done in OR-style queries yet. 

We'll do a few examples:

Find all documents containing _temperature_ in the *text* field. Show the *title* field and the number of documents that matched.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --show-title --count

title:
liter tars distortions stones shock

----------------------------------------

title:
supermarkets patter narcotics rewards stand channel checker decision morning

----------------------------------------

title:
pennant hardcopy excuse hoists interface jams returns water presentation

----------------------------------------

title:
boom prerequisite net drydocks specialization ships odds custodian kilogram

----------------------------------------

title:
moons fork formats methodology steel fan twigs heads

----------------------------------------

59 Zettels matched search
(zenv) [gkt@wilddog zettelgeist]$ ^Cthon zfind.py --database randomdata.db --find-text temperature --sho
w-title --count$ python zfind.py --database randomdata.db --find-text temperature --show-title --count
```

Again, we have omitted some results for conciseness.

Now take a look at some of the results. Since _methodology_ appears in one of them, let's do a search to restrict the results further by searching *title* for _methodology_.

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --count
1 Zettels matched search
```

Now that we found a Zettel of interest (well, it's not that interesting compared to our real notes, but...) we can project some addition fields of interest:

```shell
$ python zfind.py --database randomdata.db --find-text temperature --find-title methodology --show-mentions --show-tags --count
mentions:
Raul,Candace,Petar,Shawnette,Darren,Camryn,Brett,Kailey

tags:
dock,reach,itineraries

----------------------------------------

1 Zettels matched search
```

The output you see here is slightly different than the source Zettel (note) in YAML, because we _flatten_ the lists and text for full-text searching purposes. Future work will pull up everything from the actual Zettel, mainly for pretty printing purposes.

As you can see above, we were able to project different columns than what was actually matched.

So this is where we stand with our tools right now. We'll be updating the docs as work progresses but this is already proving useful for organizing our notes. Feel free to follow our project for the latest developments. We also welcome Issues in the Issue Tracker.

