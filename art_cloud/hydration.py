"""A set of functions for generating and parsing XML for python objects which are decorated by a HydrationMeta class:

	class HydrationMeta:
		attributes = ['id', 'name', 'slug', 'opened', 'closed', 'wiki_name']
		ref_attributes = ['power_pane']
		ref_attributes = [('site','name)]
		nodes = ['groups', 'artists', 'notes', 'photos']
		element_name = 'fantastico'
"""
from types import ListType, DictType
from xml.dom.minidom import getDOMImplementation
import xml.dom.minidom as minidom

from django.utils.encoding import smart_unicode
from django.utils.xmlutils import SimplerXMLGenerator
from django.contrib.auth.models import User

hydration_meta_name = 'HydrationMeta'
hydration_attributes_name = 'attributes' # simple attributes on the element
hydration_reference_attributes_name  = 'ref_attributes' # names of members whose ids should be set as attributes
hydration_reference_by_attributes_name  = 'ref_by_attributes' # tuples of <member name, member attribute> who should be set as attribute, for example [('site', 'name')]
hydration_nodes_name = 'nodes' # members which should be dehydrated and included as children
hydration_text_node_name = 'text_node' # member which should be used as the text node
hydration_element_name = 'element_name' # what the element should be named, defaults to __class__.__name__.lower()

hydration_list_name = 'list'

class HydrationError(Exception): pass

class XMLHydration:
	"""This is an XML serializer.  There are many like it.  This one is mine."""
	
	def dehydrate_to_list_doc(self, input_list, start=None, end=None, list_name=None):
		if start == None: start = 0
		if end == None:
			end = len(input_list)
		else:
			end = min(end, len(input_list))
		if list_name is None: list_name = hydration_list_name
		doc = getDOMImplementation().createDocument(None, list_name, None)
		doc.documentElement.setAttribute('start', str(start))
		doc.documentElement.setAttribute('end', str(end))
		doc.documentElement.setAttribute('total-length', str(len(input_list)))
		for source in input_list[start:end]:
			doc.documentElement.appendChild(self.dehydrate_to_doc(source).documentElement)
		return doc

	def dehydrate_to_list(self, input_list, start=None, end=None, list_name=None):
		return self.dehydrate_to_list_doc(input_list, start, end, list_name).toprettyxml()
		
	def dehydrate(self, source):
		return self.dehydrate_to_doc(source).toprettyxml()

	def hydrate(self, source, data):
		"""Right now this doesn't do much by way of actually hydrating"""
		doc = minidom.parseString(data)
		#print "Parsed %s" % doc.toprettyxml()
		for attribute in doc.documentElement.attributes.keys():
			setattr(source, attribute, doc.documentElement.getAttribute(attribute))
		return source

	def get_element_name(self, source):
		if hasattr(source, hydration_meta_name): 
			meta = getattr(source, hydration_meta_name)
			if hasattr(meta, hydration_element_name): return getattr(meta, hydration_element_name)
		return smart_unicode(source.__class__.__name__.lower())

	def dehydrate_to_doc(self, source):
		element_name = self.get_element_name(source)
		#print '%s: %s' % (source, element_name)
		doc = getDOMImplementation().createDocument(None, element_name, None)
		
		if not hasattr(source, hydration_meta_name):
			if isinstance(source, DictType):
				for (key, value) in source.items():
					value_element = doc.createElement('item')
					value_element.setAttribute('key', key)
					value_element.setAttribute('value', value)
					doc.documentElement.appendChild(value_element)
			else:
				text = smart_unicode(source)
				if len(text.strip()) == 0: return None
				doc.documentElement.appendChild(doc.createTextNode(text))
			return doc
			
		meta = getattr(source, hydration_meta_name)
		if hasattr(meta, hydration_attributes_name):
			attributes = getattr(meta, hydration_attributes_name)
			for attribute in attributes:
				value = getattr(source, attribute)
				if value is None: continue
				if isinstance(value, ListType):
					if len(value) == 0: continue
					value_string = '%s' % value
					value_string = value_string[1:len(value_string) - 1]
					doc.documentElement.setAttribute(attribute, value_string)
				else:
					value_text = smart_unicode(value)
					if len(value_text.strip()) == 0: continue
					doc.documentElement.setAttribute(attribute, value_text)
		
		if hasattr(meta, hydration_reference_attributes_name):
			attributes = getattr(meta, hydration_reference_attributes_name)
			for attribute in attributes:
				value = getattr(source, attribute)
				if value is None: continue
				if hasattr(value, 'id'):
					pk = getattr(value, 'id')
				elif hasattr(value, 'pk'):
					pk = getattr(value, 'pk')
				else:
					raise HydrationError('reference attribute %s has no id or pk attribute' % value)
				doc.documentElement.setAttribute(attribute, smart_unicode(pk))

		if hasattr(meta, hydration_reference_by_attributes_name):
			attributes = getattr(meta, hydration_reference_by_attributes_name)
			for attribute, key in attributes:
				value = getattr(source, attribute)
				if value is None: continue
				if hasattr(value, key):
					pk = getattr(value, key)
				else:
					raise HydrationError('reference by attribute (%s,%s) has no key attribute' % (value, key))
				doc.documentElement.setAttribute(attribute, smart_unicode(pk))
		
		if hasattr(meta, hydration_nodes_name):
			nodes = getattr(meta, hydration_nodes_name)
			for node in nodes:
				data = getattr(source, node)
				if data is None: continue
				if hasattr(data, 'all'):
					if data.all().count() == 0: continue
					element = doc.createElement(node)
					for datum in data.all():
						datum_doc = self.dehydrate_to_doc(datum)
						if datum_doc: element.appendChild(datum_doc.documentElement)
					doc.documentElement.appendChild(element)
				elif isinstance(data, ListType):
					if len(data) == 0: continue
					element = doc.createElement(node)
					for datum in data:
						datum_doc = self.dehydrate_to_doc(datum)
						if datum_doc: element.appendChild(datum_doc.documentElement)
					doc.documentElement.appendChild(element)
				elif isinstance(data, DictType):
					if len(data) == 0: continue
					element = doc.createElement(node)
					for (key, value) in data.items():
						value_element = doc.createElement('item')
						value_element.setAttribute('key', key)
						value_element.setAttribute('value', value)
						element.appendChild(value_element)
					doc.documentElement.appendChild(element)
				elif hasattr(data, hydration_meta_name):
					doc.documentElement.appendChild(self.dehydrate_to_doc(data).documentElement)
				else:
					element = doc.createElement(node)
					data_string = smart_unicode(data)
					if not data_string or len(data_string.strip()) == 0: continue
					element.appendChild(doc.createTextNode(data_string))
					doc.documentElement.appendChild(element)
		
		if hasattr(meta, hydration_text_node_name):
			name = getattr(meta, hydration_text_node_name)
			value = getattr(source, name)
			if value is not None:
				doc.documentElement.appendChild(doc.createTextNode(smart_unicode(value)))

		return doc

from django.db.models.fields.files import ImageFieldFile
class UserHydrationMeta:
	"""Sets up hydration for the Django auth User model"""
	attributes = ['id', 'username']
User.HydrationMeta = UserHydrationMeta

class ImageHydrationMeta:
	"""Sets up hydration for Django's image field"""
	element_name = 'image'
	attributes = ['name', 'width', 'height']
ImageFieldFile.HydrationMeta = ImageHydrationMeta

import piston.emitters
class HydrationEmitter(piston.emitters.Emitter):
	""" Piston Emitter for our custom XML serialized format. """
	def render(self, request, format='xml'):
		from django.db.models.query import QuerySet
		if isinstance(self.data, QuerySet):
			return dehydrate_to_list_xml(self.data)
		return dehydrate_to_xml(self.data)
piston.emitters.Emitter.register('xml', HydrationEmitter, 'text/xml; charset=utf-8')

class StringAsXMLEmitter(piston.emitters.Emitter):
	""" Piston Emitter for strings which should just be passed as XML. """
	def render(self, request, format='string2xml'):
		return self.data
piston.emitters.Emitter.register('string2xml', StringAsXMLEmitter, 'text/xml; charset=utf-8')

def dehydrate_to_list_xml(input_list, start=None, end=None, xml_header=True, list_name=None):
	if xml_header: return XMLHydration().dehydrate_to_list(input_list, start, end, list_name)
	return XMLHydration().dehydrate_to_list_doc(input_list, start, end, list_name).documentElement.toprettyxml()
	
def dehydrate_to_xml(source, xml_header=True):
	if xml_header: return XMLHydration().dehydrate(source)
	return XMLHydration().dehydrate_to_doc(source).documentElement.toprettyxml()
	
def hydrate_from_xml(source, data):
	return XMLHydration().hydrate(source, data)