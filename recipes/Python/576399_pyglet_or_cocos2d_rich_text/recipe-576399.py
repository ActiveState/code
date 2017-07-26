class PygletRichLabel(pyglet.text.DocumentLabel):
    '''Rich text label.
    '''
    def __init__(self, text='', 
                 font_name=None, font_size=None, bold=False, italic=False,
                 color=None,
                 x=0, y=0, width=None, height=None, 
                 anchor_x='left', anchor_y='baseline',
                 halign='left',
                 multiline=False, dpi=None, batch=None, group=None):
        '''Create a rich text label.

        :Parameters:
            `text` : str
                Pyglet attributed (rich) text to display.
            `font_name` : str or list
                Font family name(s).  If more than one name is given, the
                first matching name is used.
            `font_size` : float
                Font size, in points.
            `bold` : bool
                Bold font style.
            `italic` : bool
                Italic font style.
            `color` : (int, int, int, int) or None
                Font colour, as RGBA components in range [0, 255].
                None to use font colors defined by text attributes.
            `x` : int
                X coordinate of the label.
            `y` : int
                Y coordinate of the label.
            `width` : int
                Width of the label in pixels, or None
            `height` : int
                Height of the label in pixels, or None
            `anchor_x` : str
                Anchor point of the X coordinate: one of ``"left"``,
                ``"center"`` or ``"right"``.
            `anchor_y` : str
                Anchor point of the Y coordinate: one of ``"bottom"``,
                ``"baseline"``, ``"center"`` or ``"top"``.
            `halign` : str
                Horizontal alignment of text on a line, only applies if
                a width is supplied. One of ``"left"``, ``"center"``
                or ``"right"``.
            `multiline` : bool
                If True, the label will be word-wrapped and accept newline
                characters.  You must also set the width of the label.
            `dpi` : float
                Resolution of the fonts in this layout.  Defaults to 96.
            `batch` : `Batch`
                Optional graphics batch to add the label to.
            `group` : `Group`
                Optional graphics group to use.

        '''

        text = '{color (255, 255, 255, 255)}' + text
        document = pyglet.text.decode_attributed(text)
        super(PygletRichLabel, self).__init__(document, x, y, width, height, 
                                    anchor_x, anchor_y,
                                    multiline, dpi, batch, group)
        style = dict(halign=halign)

        if font_name:
            style['font_name'] = font_name
        if font_size:
            style['font_size'] = font_size
        if bold:
            style['bold'] = bold
        if italic:
            style['italic'] = italic
        if color:
            style['color'] = color
             
        self.document.set_style(0, len(self.document.text), style)

class RichLabel(cocos.text.TextElement):
    '''CocosNode RichLabel element. It is a wrapper of a custom Pyglet Rich Label 
    using rich text attributes with the benefits of being of a CocosNode
    '''
    klass = PygletRichLabel
