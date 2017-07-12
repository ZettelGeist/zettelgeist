from zettel import Zettel

z = Zettel()
z.set_field('title', 'Title')
z.set_field('tags', "tag1")
z.append_field('tags', "tag2")
z.append_field('tags', "tag3")
z.load_field('text', 'ps.text')
print(z.get_yaml())
