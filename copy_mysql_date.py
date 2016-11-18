import MySQLdb

from posts.categoryModels import Category
from posts.models import Post

def addCategory(parent_id, name):
    print("ADD category '{}' to {}".format(name, parent_id))
    cat = Category.objects.create(name=name, parent_id=parent_id)
    print("Finish category '{}' to {} new id= {}".format(name, parent_id, cat.id))
    return cat.id

def addPost(title, content, tags, id_category):
    p = Post()
    p.title = title
    p.content = content
    p.category_id = id_category
    p.author_id = 1
    p.status = 'published'
    p.save()
    [p.tags.add(x) for x in tags.split(',')]

def getData(query, *arg):
    data = []
    try:
        db = MySQLdb.connect('ip', 'lom', 'lom', 'LOM')
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query, arg)
        data = cur.fetchallDict()

    except MySQLdb.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if cur:
            cur.close()
            if db:
                db.close()
                return data


def get_new_parent_id(old_id, map):
    for m in map:
        if m['old_id'] == old_id:
            return m['id']

categories = getData('select * from types_list')
posts = getData('select * from VIEW_WAITING')

map_cat = []

for cat in categories[1:]:
    printed = """
    ##################

    Category: {},
    old_id:   {}
    new_id:   {}
    parent_id {}
    old_p_id  {}
    """
    name = cat['type']
    id_parent = None if cat['id_parent'] == 1 else get_new_parent_id(cat['id_parent'], map_cat)
    old_id = cat['id_type']
    id = addCategory(id_parent, name)
    print(printed.format(name, old_id, id, id_parent, cat['id_parent']))
    map_cat.append({'id': id, 'name': name, 'old_id': old_id})
    print({'id': id, 'name': name, 'old_id': old_id})

for post in posts:
    title = post['name']
    content = post['description'].replace('<tt>', '```py').replace('</tt>', '```')
    content = content.replace('<span color="gray"><small><i>', '').replace('</i></small></span>', '')
    tags = post['key_list']
    id_category = get_new_parent_id(post['id_type'], map_cat)
    printed = """
    ##################

    posts:    {},
    tags:     {}
    id_cat    {}
    """
    print(printed.format(title,tags,id_category))
    addPost(title, content, tags, id_category)
