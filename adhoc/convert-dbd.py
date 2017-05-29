import yaml
import os
import sys

dir = sys.argv[1]
files = os.listdir(dir)

def process(filename):
   print("Processing %s" % filename)
   (base, ext) = os.path.splitext(filename)
   ICONV='iconv -f iso8859-1 -t utf-8 "%(base)s%(ext)s" > "%(base)s.utf8%(ext)s"' % vars()
   print("Running",ICONV)
   os.system(ICONV)
   filename = "%(base)s.utf8%(ext)s" % vars()
   #os.system(ICONV)
   lines = []
   with open(filename) as infile:
      id = infile.readline()
      print("Doc ID %s" % id)
      lines.append( ('id', id) )
      for line in infile:
         kwline = line.strip()
         if len(kwline) == 0:
            continue
         if kwline.startswith('#""'):
            lines.append( ('bibkey', kwline[3:]))
         elif kwline.startswith('#'):
            lines.append( ('tag', kwline[1:]))
         else:
            lines.append( ('text', line) )

   doc = { 'id': "", 'tags': [], 'bibkey' : [], 'text' : [] }
   for (code, text) in lines:
      if code == 'id':
         doc['id'] = text.strip()
      elif code == 'tag':
         doc['tags'].append(text.strip())
      elif code == 'bibkey':
         doc['bibkey'].append(text.strip())
      elif code == 'text':
         doc['text'].append(text)

   doc['text'] = "\n".join(doc['text'])

   (basename, extension) = os.path.splitext(filename)
   outfilename = basename + '.yaml'
   with open(outfilename, "w") as outfile:
     outfile.write(doc['id'] + '\n')
     outfile.write('---\n')
     del(doc['id'])
     outfile.write(yaml.dump(doc))


for f in files:
   if f.endswith('.md'):
     if not f.endswith('.utf8.md'):
       process( os.path.join(dir, f) )
     else:
       print("Skipping generated UTF-8 file", f)


