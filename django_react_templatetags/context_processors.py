#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings


def react_context_processor(request):
    """Expose a global list of react components to be processed"""
    warnings.warn(
        "react_context_processor is no longer required.", DeprecationWarning
    )

    return {
        'REACT_COMPONENTS': [],
    }
