from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor, ListIndentProcessor
from markdown.util import etree
import re

class MyHashHeaderProcessor(BlockProcessor):
	""" Process Hash Headers. """

	# Detect a header at start of any line in block
	RE = re.compile(r'(^|\n)(?P<level>#{1,6})(?P<header>.*?)#*(\n|$)')

	def __init__(self, parser, num_root):
	    #super(MyBlockParser, self).__init__(parser)
	    BlockProcessor.__init__(self, parser)
	    self.num_current = num_root
	    self.num_root_depth = len(num_root)

	def test(self, parent, block):
	    return bool(self.RE.search(block))

	def update_num_current(self, depth):
		
		d = self.num_root_depth + depth - 1
		
		if len(self.num_current) == d:
			self.num_current[-1] += 1
			return
		
		while len(self.num_current) != d:
		
			if len(self.num_current) < d:
				self.num_current.append(0)
				
			elif len(self.num_current) > d:
				self.num_current.pop()
			
			self.num_current[-1] += 1
		
	def run(self, parent, blocks):
		block = blocks.pop(0)
		m = self.RE.search(block)
		if m:
			before = block[:m.start()]  # All lines before header
			after = block[m.end():]     # All lines after header
			if before:
				# As the header was not the first line of the block and the
				# lines before the header must be parsed first,
				# recursively parse this lines as a block.
				self.parser.parseBlocks(parent, [before])
			
			# my addition
			level = len(m.group('level'))
			self.update_num_current(level)
			s = '.'.join(str(i) for i in self.num_current)
			s_id = '_'.join(str(i) for i in self.num_current)
			
			# Create header using named groups from RE
			h = etree.SubElement(parent, 'h{}'.format(level))
			h.text = s + ' ' + m.group('header').strip()
			h.attrib['id'] = s_id
			
			if after:
				# Insert remaining lines as first block for future parsing.
				blocks.insert(0, after)
		else:  # pragma: no cover
			# This should never happen, but just in case...
			logger.warn("We've got a problem header: %r" % block)

class MyBlockParser(BlockProcessor):
	
	RE = re.compile('^([#]+)[ ]+([^\n]*)')
	
	def __init__(self, parser, num_root):
		#super(MyBlockParser, self).__init__(parser)
		BlockProcessor.__init__(self, parser)
		self.num_current = num_root
		self.num_root_depth = len(num_root)
	
	def test(self, parent, block):
		print 'test',repr(block)
		return bool(self.RE.search(block))
		

		
	
		
	def run(self, parent, blocks):
		#print
		#print 'run', repr(blocks)
		
		raw_block = blocks.pop(0)
		
		m = self.RE.search(raw_block)
		
		print 'rest',repr(raw_block[m.end():])
		
		#print m.groups()
		print 'group 1',repr(m.group(1)), repr(m.group(2))
		
		depth = len(m.group(1))
		
		self.update_num_current(depth)
		
		print 'num_current', self.num_current
		
		tag = 'h{}'.format(depth)
		
		print 'tag',tag
		
		h = etree.SubElement(parent, tag)
		h.text = '.'.join(str(i) for i in self.num_current)
		h.text += ' ' + m.group(2)
		
		h.attrib['id'] = '_'.join(str(i) for i in self.num_current)
		
		'''
				
		#print 'm', m.start(), m.end()
		
		div = etree.SubElement(parent, 'div')
		div.attrib['class'] = 'question'
		#print div.attrib
		
		self.parser.parseBlocks(div, [raw_block[m.end():]])
		#blocks.insert(0, raw_block[m.end():])
		'''
		return False

class MyExtension(Extension):
    def __init__(self, num_root):
	self.num_root = num_root
	print 'num_root', num_root
		
    def extendMarkdown(self, md, md_globals):
	md.parser.blockprocessors['hashheader'] = MyHashHeaderProcessor(md.parser, self.num_root)

