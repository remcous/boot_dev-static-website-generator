class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        output = ""
        for k,v in self.props.items():
            output += f" {k}=\"{v}\""
        return output
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        output = ""
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html() if self.props is not None else ''}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None,  props=None):
        super().__init__(tag=tag, props=props, children=children)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node must have a tag")
        if self.children is None:
            raise ValueError("Parent Node must have a Child node")
        output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            output += child.to_html()
        output += f"</{self.tag}>"
        return output
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"