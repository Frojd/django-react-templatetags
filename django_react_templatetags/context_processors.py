#!/usr/bin/env python
# -*- coding: utf-8 -*-


def react_context_processor(request):
    """Expose a global list of react components to be processed"""
    print("react_context_processor is no longer required.")

    return {
        'REACT_COMPONENTS': [],
    }
