import markdown
from markdown_extension_numbering import MyExtension

r = '# sec\n\n# sec\n\n## subsec\n\n# sec\n\n## subsec\n\n'

s = markdown.markdown(r, extensions=[MyExtension([1,1])])

print 'result'
print s


