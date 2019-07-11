.. ev-reduce documentation master file, created by
   sphinx-quickstart on Thu Jul 11 17:29:18 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ev-reduce's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Description
-----------

The framework is a flexible tool to define event sources, handlers of events,
and produce an action from a handler

    1. Event source emits an event. Event = `(type, event_data)`
    2. All reducers that listen to event `type` got called and passed `(event, global_data)`.
    3. The reducers map events to an action based on current data. they also modify data and return `(action, data)`
    4. The action is `(label, action_data)`. It is passed to every action handler.

Testing
-------

run ``python setup.py test`` for testing


Module docs
-----------

.. autoclass:: evv3.SyncModel
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
