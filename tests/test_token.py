# -*- coding: utf-8 -*-

from unittest import TestCase
from bnfparsing.token import Token

NUM = 5
MASTER = 'master'
CHILD = 'child'

class TokenTestSuite(TestCase):

    def test_token_creation(self):
        """ Test the __init__ method. """
        token = Token(token_type=MASTER, text=MASTER)
        self.assertEqual(token.token_type, MASTER, 
            msg='token_type not intialised properly'
            )
        self.assertEqual(token.text, MASTER, 
            msg='text not initialised properly'
            )

    def test_child_addition(self):
        """ Test addition of children and links between the two. """
        master = Token(MASTER)
        child = Token(CHILD)
        master.add(child)
        self.assertEqual(master.children[0], child,
            msg='child not properly added to master'
            )
        self.assertEqual(child.parent, master, 
            msg='master not added as parent'
            )

    def test_child_indicator(self):
        """ Test the has_under method. """
        master = Token(MASTER)
        self.assertFalse(master.has_under(), 
            msg='failed for empty token'
            )
        child = Token(CHILD)
        master.add(child)
        self.assertTrue(master.has_under(),
            msg='failed for token with children'
            )

    def test_child_removal(self):
        """ Test removal of children. """
        master = Token(MASTER)
        child = Token(CHILD)
        master.add(child)
        master.remove(child)
        self.assertFalse(master.has_under(), msg='child removal failed')
        self.assertIsNone(child.parent, msg='parent removal failed')

    def test_value_literal(self):
        """ Test the value method of literals. """
        token = Token(text=MASTER)
        self.assertEqual(token.value(), MASTER,
            msg='value method failed for literal'
            )

    def test_value_master(self):
        """ Test the value method of tokens with children. """
        master = Token(MASTER)
        string = ''
        for index in range(NUM):
            master.add(Token(text=str(index)))
            string += str(index)
        self.assertEqual(master.value(), string,
            msg='value method failed for token with children'
            )

    def test_len(self):
        """ Test the __len__ method of tokens. """
        master = Token(text=MASTER)
        self.assertEqual(len(master), len(MASTER),
            msg='__len__ method failed'
            )

    def test_iteration_children(self):
        """ Test the iter_under method, iterating over children. """
        master = Token()
        for index in range(NUM):
            master.add(Token(index, str(index)))
        index = 0
        for child in master.children:
            self.assertEqual(child.text, str(index),
                msg='iteration over children failed'
                )
            index += 1
    
    def test_bool(self):
        """ Test __bool__ method. """
        token = Token()
        self.assertFalse(token, msg='__bool__ failed for empty token')
        token = Token(MASTER)
        self.assertTrue(token, msg='__bool__ failed for token with type')
        token = Token(text=MASTER)
        self.assertTrue(token, msg='__bool__ failed for token with text')
    
    def test_equal(self):
        """ Test __eq__ method. """
        token = Token(text=MASTER)
        child = Token(text=CHILD)
        self.assertTrue(token == token, msg='__eq__ failed for token')
        self.assertTrue(token == MASTER, msg='__eq__ failed for string')
        self.assertFalse(token == child, 
            msg='__eq__ gave false positive for token'
            )
        self.assertFalse(token == CHILD, 
            msg='__eq__ gave false postive for string'
            )

    def test_has_under_no_args(self):
        """ Test the has_under method without arguments. """
        token = Token()
        self.assertFalse(token.has_under(),
            msg='has_under failed for empty token'
            )
        token.add(Token())
        self.assertTrue(token.has_under(),
            msg='has_under failed for non-empty token'
            )

    def test_has_under_with_tag(self):
        """ Test the has_under method with a tag name. """
        token = Token()
        token.add(Token(token_type=CHILD))
        self.assertTrue(token.has_under(CHILD), 
            msg='failed to identify existing token'
            )
        self.assertFalse(token.has_under(MASTER),
            msg='falsely found non-existent token'
            )

    def test_tag(self):
        """ Test tag creation and addition. """
        token = Token(MASTER)
        self.assertEqual(token.tags, {MASTER}, 
            msg='did not include token type tag in new token'
            )
        token.tag(CHILD)
        self.assertTrue(CHILD in token.tags, msg='tag addition failed')
        token = Token(MASTER, tags=[CHILD])
        self.assertEqual(token.tags, {MASTER, CHILD},
            msg='tag addition from __init__ failed'
            )
