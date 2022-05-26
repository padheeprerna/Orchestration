# CONFIDENTIAL COMPUTER CODE AND INFORMATION
# COPYRIGHT (C) VMware, INC. ALL RIGHTS RESERVED.
# REPRODUCTION BY ANY MEANS EXPRESSLY FORBIDDEN WITHOUT THE WRITTEN
# PERMISSION OF THE OWNER.
#
# LOGGER MODULE
# ----------------------------------------------------------------------------

# STANDARD LIBRARIES

import os
import time
import logging


class Logger(object):

    """
        Parse Json Input
    """

    def __init__(self, log_file):
        """
            Constructor
        """

        self.logger = logging.getLogger('security_automation')
        self.logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages

        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers

        formatter = \
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                              )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add the handlers to logger

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    # set logger header

        self.record('line')
        self.record('header')
        self.record('line')

    def record(self, mode, msg=None):
        """
            log record
        """

        if mode == 'debug':
            self.logger.debug(msg)
        if mode == 'info':
            self.logger.debug(msg)
        if mode == 'warn':
            self.logger.warn(msg)
        if mode == 'error':
            self.logger.error(msg)
        if mode == 'critical':
            self.logger.critical(msg)

    # For formatting log file

        if mode == 'line':
            self.logger.debug('-' * 101)
        if mode == 'dotted':
            self.logger.debug(' - -' * 25)
        if mode == 'newline':
            self.logger.debug(' ')
        if mode == 'header':
            self.logger.debug(' ' * 35
                              + 'Security Analysis Execution Log' + ' '
                              * 35)

    def __del__(self):
        """
            Destructor
        """

        self.record('line')
