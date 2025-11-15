#!../myenv/bin/python3

import markdown

#Markdown Converter 
class MdConverter(markdown.core.Markdown):
    
    def convert_to_tree(self, source: str) -> str:
        """
        Convert a Markdown string to an xml.etree.Element

        The markdown converter is an overloaded function
        
        Arguments:
            source: Markdown formatted text as Unicode or ASCII string.

        Returns:
            An xml.etree.Element
        """

        # Fix up the source text
        if not source.strip():
            return ''  # a blank Unicode string

        try:
            source = str(source)
        except UnicodeDecodeError as e:  # pragma: no cover
            # Customize error message while maintaining original traceback
            e.reason += '. -- Note: Markdown only accepts Unicode input!'
            raise

        # Split into lines and run the line preprocessors.
        self.lines = source.split("\n")
        for prep in self.preprocessors:
            self.lines = prep.run(self.lines)

        # Parse the high-level elements.
        root = self.parser.parseDocument(self.lines).getroot()

        # Run the tree-processors
        for treeprocessor in self.treeprocessors:
            newRoot = treeprocessor.run(root)
            if newRoot is not None:
                root = newRoot

        return root
