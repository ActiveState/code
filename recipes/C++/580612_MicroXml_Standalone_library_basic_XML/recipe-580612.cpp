/*
MicroXml provides stand-alone support for the basic, most-used features
of XML -- tags, attributes, and element values. That's all. It produces
a DOM tree of XML nodes.

MicroXml does not support DTDs, CDATAs and other advanced XML features. 
It stores the XML declaration but doesn't use it.

However, within these limitations, MicroXml is easy to use and allows 
far simpler debugging of XML results than when using a full-featured 
XML library. With XmlDoc::to_string() one can round-trip the XML for 
fast eyeball checking.

This module contains main() which will parse a sample XML string into
a DOM tree, then write the DOM tree out as XML text.

Jack Trainor 2015
*/

#include <iostream>
#include <string>
#include <cstdio>
#include <deque>
#include <vector>
#include <map>

typedef unsigned int uint;

static const int	NO_TAG = 0;
static const int	START_TAG = 1;
static const int	END_TAG = 2;
static const int	EMPTY_TAG = 3;
static const int	COMMENT_TAG = 4;
static const int	DECL_TAG = 5;
static const int	DOCTYPE_TAG = 6;

bool strEq(const std::string& s1,  const std::string& s2);
int getTagType(const std::string& xml);
bool charInString(const char c, const std::string& s);
void compressReturns(std::string& s);

////////////////////////////////////////////////////////////////////////////////
class XBuffer
{
public:
	const std::string&	text;
	int					index;
	int					len;

	XBuffer(const std::string& text, int index=0);
	virtual ~XBuffer(void);

	virtual bool atEnd();
	virtual void incIndex();
	virtual char getChar();
	virtual char getNextChar();
	virtual void skipSpace();
	virtual void skipChars(const std::string& chars);
	virtual bool getCharsToDelimiter(const std::string& delimiters, 
								std::string& chars, bool inclDelimiter=false);
};

////////////////////////////////////////////////////////////////////////////////
class XmlNode
{
public:
	std::string							tag;
	std::string							text;
	std::map<std::string, std::string>	attributes;
	std::vector<XmlNode*>				children;
	XmlNode*							parent;

	XmlNode(const std::string& tag, const std::string& text,
			const std::map<std::string, std::string>& attributes, XmlNode* parent);
	virtual ~XmlNode(void);

	virtual void addChild(XmlNode* node);
	virtual void appendText(const std::string& text);
	virtual void toString(std::string& s);
};

////////////////////////////////////////////////////////////////////////////////
class XmlDocument
{
public:
	std::deque<XmlNode*>	stack;
	XmlNode*				root;

	XmlDocument(void);
	virtual ~XmlDocument(void);

	virtual void pushNode(XmlNode* node);
	virtual XmlNode* popNode();
	virtual XmlNode* getCurNode();

	virtual void startElement(const std::string& name, 
					const std::map<std::string, std::string>& attributes);
	virtual void characters(const std::string& chars);
	virtual void endElement(const std::string& name);

	virtual void getNameAttrsFromTag(std::string& xml, std::string& name, 
					std::map<std::string,std::string>& attrs);

	virtual void lex(const std::string& xml, std::vector<std::string>& chunks);
	virtual XmlNode* parse(const std::string& xml, bool stripEmptyChars=true);

	virtual void handleError(const std::string& msg);
//	virtual void test();
};

//==============================================================================
// Utils
//==============================================================================
void trim(std::string &str){
    int i = 0;
	int len = str.size();
	while (isspace(str[i]) != 0)
        i++;
    str = str.substr(i, str.length() - i);

    i = str.size()-1;
	len = str.size();
	while (len > 0 && i >= 0 && isspace(str[i]) != 0)
        i--;

	if (len > 0 && i >= 0) {
		str = str.substr(0, i + 1);
	}
}

void replace(std::string &str, char oldC, char newC) {
	for (uint i = 0; i < str.size(); i++) {
		char c = str[i];
		if (c == oldC) {
			str[i] = newC;
		}
	}
}

bool strEq(const std::string& s1,  const std::string& s2) {
	return (s1.compare(s2) == 0);
}

bool charInString(const char c, const std::string& s) {
	size_t pos = s.find(c);
	return (pos != std::string::npos);
}

void compressReturns(std::string& xml) {
	XBuffer xbuf(xml, 0);
	std::string sOut;
	while (!xbuf.atEnd()) {
		std::string chars;
		xbuf.getCharsToDelimiter("\n", chars, true);
		sOut.append(chars);
		xbuf.skipChars("\n");
	}
	xml.clear();
	xml.append(sOut);
}

int getTagType(const std::string& xml) {
	int len = xml.size();
	if (xml[0] == '<' && xml[len-1] == '>') {
		if ((xml.find("<?xml") == 0) && (xml[len-2] == '?')) {
			return DECL_TAG;
		} else if (xml.find("<!DOCTYPE") == 0) {
			return DOCTYPE_TAG;
		} else if ((xml.find("<!--") == 0) && (xml[len-2] == '-') && (xml[len-3] == '-')) {
			return COMMENT_TAG;
		} else if ((xml[1] != '/') && (xml[len-2] != '/')) {
			return START_TAG;
		} else if ((xml[1] != '/') && (xml[len-2] == '/')) {
			return EMPTY_TAG;
		} else if ((xml[1] == '/') && (xml[len-2] != '/')) {
			return END_TAG;
		}
	}
	return NO_TAG;
}

//==============================================================================
// XBuffer
//==============================================================================
XBuffer::XBuffer(const std::string& text, int index) :
		text(text), index(index), len(text.length()) {
}

XBuffer::~XBuffer(void) {
}

bool XBuffer::atEnd() {
	return (index >= len);
}

void XBuffer::incIndex() {
	if (!atEnd()) {
		index += 1;
	}
}

char XBuffer::getChar() {
	if (!atEnd()) {
		return text.at(index);
	}
	return 0;
}    

char XBuffer::getNextChar() {
    incIndex();
    return getChar();
}
                
void XBuffer::skipSpace() {
	while (!atEnd()) {
		int c = getChar();
		if (isspace(c)) {
			incIndex();
		} else {
			break;
		}
	}
}

void XBuffer::skipChars(const std::string& chars) {
	while (!atEnd()) {
		int c = getChar();
		if (charInString(c, chars)) {
			incIndex();
		} else {
			break;
		}
	}
}

bool XBuffer::getCharsToDelimiter(const std::string& delimiters, 
								std::string& chars, bool inclDelimiter) {
    chars.clear();
    bool foundDelimiter = false;
	while (!atEnd() && !foundDelimiter) {
        char c = getChar();
		size_t found = delimiters.find(c);
		foundDelimiter = (found != std::string::npos);
		if (!foundDelimiter || (foundDelimiter && inclDelimiter)) {
            chars.append(1, c);
            incIndex();
		}
	}
	return foundDelimiter;
}
			
//==============================================================================
// XmlNode
//==============================================================================
XmlNode::XmlNode(const std::string& tag, const std::string& text,
				 const std::map<std::string, std::string>& attributes, XmlNode* parent=NULL) :
			tag(tag), text(text), attributes(attributes), parent(parent) {
	if (parent) {
		parent->addChild(this);
	}
}

XmlNode::~XmlNode(void) {
	for (std::vector<XmlNode*>::iterator it=children.begin(); it!=children.end(); ++it) {
		XmlNode* node = *it;
		delete node;
	}
}

void XmlNode::addChild(XmlNode* node) {
	children.push_back(node);
	node->parent = this;
}

void XmlNode::appendText(const std::string& text_) {
	text.append(text_);
}

void XmlNode::toString(std::string& s) {
	std::string attrsStr;
	for (std::map<std::string,std::string>::iterator it=attributes.begin(); it!=attributes.end(); ++it) {
		if (attrsStr.size() != 0) {
			attrsStr.append(" ");
		}
		attrsStr.append(it->first + "=\"" + it->second + "\"");
	}

	if (children.size() > 0 || text.size() > 0) {
		if (attrsStr.size() > 0) {
			s.append("\n<" + tag + " " + attrsStr + ">");
		} else {
			s.append("\n<" + tag + ">");
		}

		s.append("\n<" + tag + ">");
		s.append(text);
		for (std::vector<XmlNode*>::iterator it=children.begin(); it!=children.end(); ++it) {
			std::string nodeString;
			XmlNode* node = *it;
			node->toString(nodeString);
			s.append(nodeString);
		}
		s.append("</" + tag + ">\n");
	} else {
		if (attrsStr.size() > 0) {
			attrsStr.insert(0, " ");
		}
		s.append("<" + tag + attrsStr + "/>\n");
	}
	compressReturns(s);
}

//==============================================================================
// XmlDocument
//==============================================================================
XmlDocument::XmlDocument(void) : root(NULL) {
}

XmlDocument::~XmlDocument(void) {
	delete root;
}

void XmlDocument::handleError(const std::string& msg) {
	std::cout << msg << std::endl;	
}


void XmlDocument::pushNode(XmlNode* node) {
    stack.push_back(node);
}

XmlNode* XmlDocument::popNode() {
    XmlNode* node = getCurNode();
	if (node) {
		stack.pop_back();
	} else {
		std::string msg = "XmlDocument::popNode stack empty.";
		handleError(msg);
	}
    return node;
}

XmlNode* XmlDocument::getCurNode() {
	XmlNode* node = NULL;
	int nodeCount = stack.size();
	if (nodeCount > 0) {
		node = stack[nodeCount-1];
	}
	return node;
}

void XmlDocument::startElement(const std::string& name, const std::map<std::string, std::string>& attributes) {
	std::cout << "startElement: [" + name + "]" << std::endl;
	XmlNode* node = new XmlNode(name, "", attributes);    
	if (!root) {
		root = node;
	}
	XmlNode* curNode = getCurNode();
	if (curNode) {
		curNode->addChild(node);
	}
	pushNode(node);
}

void XmlDocument::characters(const std::string& chars) {
	XmlNode* curNode = getCurNode();
	if (curNode) {
		curNode->appendText(chars);
	}
}

void XmlDocument::endElement(const std::string& name) {
	std::cout << "endElement: [" + name + "]" << std::endl;
	XmlNode* node = popNode();

	if (node && (node->tag.compare(name) != 0)) {
		std::string msg = "XmlDocument::end_element: tag [";
		msg.append(name + "] not matching node [");
		msg.append(node->tag + "]");
		handleError(msg);
	}
}

void XmlDocument::getNameAttrsFromTag(std::string& xml, std::string& name, 
									  std::map<std::string,std::string>& attrs) {
	replace(xml, '\'', '"');
	XBuffer xbuf(xml);
	xbuf.incIndex();
	xbuf.skipSpace();
	xbuf.getCharsToDelimiter("' />", name);
	char c = xbuf.getChar();
	while (true) {
		if (c == ' ') {
			xbuf.skipSpace();
			std::string attrName;
			xbuf.getCharsToDelimiter("=", attrName);
			c = xbuf.getNextChar();
			if (c == '"') {
				xbuf.incIndex();
				std::string attrVal;
				xbuf.getCharsToDelimiter("\"", attrVal);
				c = xbuf.getChar();
				if (c == '"') {
					attrs[attrName] = attrVal;
					xbuf.incIndex();
				} else {
					std::string msg = "XmlDoc::get_name_attrs_from_tag [";
					msg.append(xml + "] reached end of buffer too soon.");
					handleError(msg);
				}
				c = xbuf.getChar();
			}
		} else {
			break;
		}
	}
}

void XmlDocument::lex(const std::string& xml, std::vector<std::string>& chunks) {
	// Divide xml into raw items delimited by '<' and '>' pair or not so delimited.
	std::string chars;
	XBuffer xbuf(xml);
	while (!xbuf.atEnd()) {
		bool found = xbuf.getCharsToDelimiter("<", chars);
		bool charsEmpty = (chars.size() == 0);
		bool charsReturn = (chars.compare("\n") == 0);
		if (found && !charsEmpty && !charsReturn) {
			chunks.push_back(chars);
		}

		if (!xbuf.atEnd()) {
			bool found = xbuf.getCharsToDelimiter(">", chars, true);
			bool charsEmpty = (chars.size() == 0);
			if (found && !charsEmpty) {
 				chunks.push_back(chars);
			}
		}
	}
}

XmlNode* XmlDocument::parse(const std::string& xml, bool stripEmptyChars) {
	std::vector<std::string> chunks;
	lex(xml, chunks);
	if (chunks.size() > 0) {
		for (unsigned int i = 0; i < chunks.size(); i++) {
			std::string name;
			std::map<std::string, std::string> attrs;
			std::string chunk = chunks[i];
			int tagType = getTagType(chunk);
			switch (tagType) {
				case START_TAG:
					getNameAttrsFromTag(chunk, name, attrs);
					startElement(name, attrs);
					break;
				case END_TAG:
					name = chunk.substr(2, chunk.size()-3);
					endElement(name);
					break;
				case EMPTY_TAG:
					getNameAttrsFromTag(chunk, name, attrs);
					startElement(name, attrs);
					endElement(name);
					break;
				case COMMENT_TAG:
					break;
				case DECL_TAG:
					break;
				case DOCTYPE_TAG:
					break;
				default:
					if (stripEmptyChars == true) {
						trim(chunk);
					}
					characters(chunk);
			}
		}
	}
	return root;
}

////////////////////////////////////////////////////////////////////////////////
const std::string XML = "<catalog> \
   <book id= \"bk101 \"> \
      <author>gambardella, matthew</author> \
      <title>xml developer \'s guide</title> \
      <genre>computer</genre> \
      <price>44.95</price> \
      <publish_date>2000-10-01</publish_date> \
      <description>an in-depth look at creating applications \
with xml.</description> \
   </book> \
   <book id= \"bk102 \"> \
      <author>ralls, kim</author> \
      <title>midnight rain</title> \
      <genre>fantasy</genre> \
      <price>5.95</price> \
      <publish_date>2000-12-16</publish_date> \
      <description>a former architect battles corporate zombies, \
an evil sorceress, and her own childhood to become queen \
of the world.</description> \
   </book> \
   <book id= \"bk103 \"> \
      <author>corets, eva</author> \
      <title>maeve ascendant</title> \
      <genre>fantasy</genre> \
      <price>5.95</price> \
      <publish_date>2000-11-17</publish_date> \
      <description>after the collapse of a nanotechnology \
 society in england, the young survivors lay the \
foundation for a new society.</description> \
   </book> \
</catalog> \
";

void test() {
	XmlDocument xdoc;
	xdoc.parse(XML);
	std::string s;
	xdoc.root->toString(s);
	std::cout << s << std::endl;
}

int main(int argc, char *argv[]) {
	std::cout << "MicroXml Recipe." << std::endl;
	test();
	std::cout << "Press RETURN." << std::endl;
	std::cin.get();
	return 0;
}
