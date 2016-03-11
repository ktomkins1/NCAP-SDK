# -*- coding: utf-8 -*-

"""
.. module:: ncaplite
   :platform: Unix, Windows
   :synopsis: This is just a stub module while we're framing the project out.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""




def my_stub():
    """This is just a stub function

    Args:
       none

    Returns:
       int.  The return code::

          1 -- Success!

    A way you might use me is

    >>> my_stub()
    0
    """
    return 1


class MyPublicClass(object):
    """We use this as a public class example class.

    You never call this class before calling :func:`mystub`.

    .. note::

       An example of intersphinx is this: you **cannot** use :mod:`pickle` on this class.

    """

    def __init__(self, foo, bar='baz'):
        """A really simple class.

        Args:
           foo (str): We all know what foo does.

        Kwargs:
           bar (str): Really, same as foo.

        """
        self._foo = foo
        self._bar = bar

    def get_foobar(self, foo, bar=True):
        """This gets the foobar

        This really should have a full function definition, but I am too lazy.

        >>> print get_foobar(10, 20)
        30
        >>> print get_foobar('a', 'b')
        ab

        Isn't that what you want?

        """
        return foo + bar

    def _get_baz(self, baz=None):
        """A private function to get baz.

        This really should have a full function definition, but I am too lazy.

        """
        return baz
